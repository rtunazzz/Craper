#!/usr/local/bin/python3

from json import loads
from math import ceil
from os import makedirs, path
from pathlib import Path
from queue import Queue
from random import choice as rand_choice
from threading import Condition, Lock, Thread, current_thread
# TODO add a conditional variable for sending pids

from time import sleep
from typing import Dict, List, Union

from requests import exceptions, head, post

from craper.db.db import DatabaseWrapper
from craper.models import *
from craper.utils import load_proxies, TermColors as c

SITES = {
    'footpatrol': Footpatrol,
    'size': Size,
    'jdsports': JDSports,
    'thehipstore': TheHipStore,
    'solebox': Solebox,
    'snipes': Snipes,
    'onygo': Onygo,
    'courir': Courir,
}

class Scraper:
    """Scraper class, implementing a scraper for one of the supported websites.

    Supported websites:
        Footpatrol,
        Size,
        JDSports,
        TheHipStore,
        Solebox,
        Snipes,
        Onygo,
        Courir

    Args:
        site_name
        start_pid
        stop_pid
        use_proxies
        debug
        delay
        db_path

    Methods:
        get_proxy()
        check_pid(pid)
        send_all()
        scrape(num_threads, pids_per_thread)
    
    Raises:
        ValueError
            When the scraper input is malformed in any way
        FileNotFoundError
            When a required file(s) is missing
    """
    def __init__(
        self,
        site_name: str,
        start_pid: Union[int, str] = 1,
        stop_pid: Union[int, str] = -1,
        use_proxies: bool = False,
        debug: bool = False,
        delay: int = 1,
        db_path: str = None,
    ) -> None:
        """Initializes a new Scraper instance.

        Args:
            site_name (str): Name of the site we're scraping
            start_pid (Union[int, str], optional): PID the scraper starts with. Defaults to 1.
            stop_pid (Union[int, str], optional): PID the scraper starts with. Defaults to -1.
            use_proxies (bool, optional): Whether or not to use proxies. Defaults to False.
            debug (bool, optional): Prints additional messages to the console when set to True. Defaults to False.
            delay (int, optional): Delay inbetween requests in each thread. Defaults to 1.
            db_path (str, optional): Path to a database where to save found PIDs. Defaults to None.

        Raises:
            FileNotFoundError: When the config.json file isn't found in the config folder
            ValueError: When a scraper for a non-supported site is initalized
            ValueError: When the `start_pid` is lower than 1
            ValueError: When the `stop_pid` is lower than -1
            ValueError: When there are no webhooks set in the config.json file
            ValueError: When a webhook isn't found for the site provided
            ValueError: When a webhook is empty
        """

        print(c.bold + f"ℹ️  [{site_name.upper()}] Initializing a scraper" + c.reset)
        print(f"ℹ️  [{site_name.upper()}] Starting from PID {start_pid} and ending {'never' if int(stop_pid) == -1 else f'at {stop_pid}'}")
        print(f"ℹ️  [{site_name.upper()}] {'Using proxies' if use_proxies else 'Not using proxies'} on a {delay}s delay.")

        self.running_threads: List[Thread] = []
        self.debug = debug
        self.delay = delay
        
        self.db_lock = Lock()
        self.curr_lock = Lock()
        self.print_lock = Lock()
        
        self.cnt_lock = Lock()
        self._pids_checked = 0

        self.send_queue = Queue()

        # Get the absotule path of the current file
        self._absolute_path = Path(__file__).parent.absolute()
        data_folder_path = f"{self._absolute_path}/data"
        
        # create a data/ folder if it doesn't exist
        if not path.exists(data_folder_path):
            makedirs(data_folder_path)
        
        config_path = f"{self._absolute_path}/config/config.json"
        if not path.exists(config_path):
            raise FileNotFoundError(f"File 'config.json' not found in: {self._absolute_path}/config")
        
        proxies_path = f'{self._absolute_path}/config/proxies.txt'
        
        # Make sure the site is supported
        supported_sites = map(lambda site: site.lower(), SITES.keys())
        if site_name.lower() not in supported_sites:
            raise ValueError(f"Scaper for '{site_name}' is not supported.")
        
        self.name = site_name
        self.site = SITES[site_name.lower()]()

        self.start_pid = self.site.parse_pid(start_pid)
        self.stop_pid = self.site.parse_pid(stop_pid)
        if self.debug: 
            print(f"🧰 [{site_name.upper()}] Parsed '{start_pid}' into '{self.site.parse_pid(start_pid)}'")
            print(f"🧰 [{site_name.upper()}] Parsed '{stop_pid}' into '{self.site.parse_pid(stop_pid)}'")

        if self.start_pid < 1:
            raise ValueError(f'The start_pid has to be greater or equal to 1.')
        elif self.stop_pid < -1:
            raise ValueError(f'The stop_pid has to be greater or equal to -1.')

        # Load in config
        with open(config_path) as config_f:
            self.config = loads(config_f.read())

        if 'webhooks' not in self.config:
            raise ValueError(f"No 'webhooks' attribute found in the config.json file.")

        # Make sure a webhook is specified
        webhook_config = self.config['webhooks']
        if self.name not in webhook_config:
            # check if there's a webhook for rest
            if "rest" in webhook_config:
                self.webhook: str = webhook_config["rest"]
                print(c.red + f"🎛  [{self.name.upper()}] Webhook for '{self.name}' not found - using the 'rest' webhook." + c.reset)
            else:
                raise ValueError(f"No webhook (nor a 'rest' webhook) specified for site {self.name}")
        else:
            print(f"🗣  [{self.name.upper()}] Using the '{self.name}' webhook.")
            self.webhook: str = webhook_config[self.name]

        if self.webhook.strip() == '':
            raise ValueError(f"Webhook is empty!")

        self.embed_hex = int(self.config['embed']['color'].replace('#', ''), 16) if ('embed' in self.config and 'color' in self.config['embed']) else 0xFFADA2
        self.footer_text = self.config['embed']['footer']['text'] if ('embed' in self.config and 'footer' in self.config['embed'] and 'text' in self.config['embed']['footer']) else "@rtunazzz"
        
        self.useragents: List[str] = self.config['useragents'] if 'useragents' in self.config else ["github.com/rtunazzz/pid-scrapers"]
        
        # load in proxies if needed
        self.proxies = load_proxies(proxies_path) if use_proxies else []
        print(f"🔗 [{self.name.upper()}] Using {len(self.proxies)} proxies.")
    
        # Initialize our database in the project's root/data folder
        if db_path != None:
            db_path = path.expanduser(db_path)
            db_folder_path = '/'.join(db_path.split('/')[:-1])
            if not path.exists(db_folder_path):
                makedirs(db_folder_path)

            print(f"🪣  [{self.name.upper()}] Using the database '{db_path}'")
            self.db = DatabaseWrapper(db_path)
        else: 
            print(f"🪣  [{self.name.upper()}] Using the (default) database '{data_folder_path}/pids.db'")
            self.db = DatabaseWrapper(f"{data_folder_path}/pids.db")

        # Make sure we have a table for the current site created
        self.db.create_table_safe(site_name.lower())
        
        # Load in the current pids (from previous scraping sessions)
        self.current_pids = self.db.get_pids_int(site_name)
        self._failed_pids: List[int] = []

        self.pid_generator = self.site.pid_stream(self.start_pid, self.stop_pid)

        self._build_webhook = lambda pid: self.site.build_webhook(self.embed_hex, self.name, self.footer_text, pid)

    def __del__(self) -> None:
        if not self.debug: return

        if len(self._failed_pids) > 0:
            print(c.bold + f"[{self.name.upper()}] Failed to check the follwing PIDs:" + c.reset)
            for pid in self._failed_pids:
                print(f'{self.site.format_pid(pid)}')

    def get_proxy(self) -> Dict:
        """Gets a random proxy from the proxies loaded.

        Returns:
            Dict: Proxy object
        """
        if len(self.proxies) > 1:
            return rand_choice(self.proxies)
        return {}

    def check_pid(self, pid: int) -> bool:
        """Checks whether or not the `pid` provided exists.

        Args:
            pid (int): PID to check

        Returns:
            bool: Whether or not the PID is loaded
        """
        with self.curr_lock:
            # check if the pid isn't already loaded
            if pid in self.current_pids:
                return True

        # generate the image URL
        url = self.site.image_url(pid)

        try:
            if self.debug: 
                print(f"🧰 [{self.name.upper()}] [{current_thread().name}] Checking {url}")
            # send a head request to check if the resource exists
            r = head(url, proxies=self.get_proxy(), headers={"User-Agent": rand_choice(self.useragents)})

            if r.status_code == 200:
                # 200 = loaded
                # pid exists, save it
                with self.print_lock:
                    print(c.green + f'👀 [{self.name.upper()}] [{current_thread().name}] Found a new pid {pid} ({self.site.format_pid(pid)})' + c.reset)
                self.current_pids.append(pid)
                self.send_queue.put(pid)
                with self.cnt_lock:
                    self._pids_checked += 1
                return True
            elif r.status_code == 404:
                # 404 = not loaded
                with self.cnt_lock:
                    self._pids_checked += 1
                return False
            elif r.status_code == 403:
                print(c.orange + f'⛔️ [{self.name.upper()}] [{current_thread().name}] IP banned' + c.reset)
            elif r.status_code == 429:
                with self.print_lock:
                    print(c.orange + f'🐌 [{self.name.upper()}] [{current_thread().name}] Ratelimited - Sleeping for 100sec' + c.reset)
                    sleep(self.delay * 100)
            else:
                print(f'🧐 [{self.name.upper()}] [{current_thread().name}] [{r.status_code}] Bad status code for pid {pid} ({self.site.format_pid(pid)})')
        except exceptions.ProxyError as e:
            with self.print_lock:
                print(c.orange + f'🔗 [{self.name.upper()}] [{current_thread().name}] Proxy failed - failed to check pid {pid} ({self.site.format_pid(pid)})' + c.reset)
                if self.debug:
                    print(e)
        except exceptions.ConnectionError:
            with self.print_lock:
                print(c.orange + f'🔗 [{self.name.upper()}] [{current_thread().name}] Failed to connect - failed to check pid {pid} ({self.site.format_pid(pid)})' + c.reset)
        
        self._failed_pids.append(pid)
        return False

    def _send_pid(self, pid: int) -> None:
        """Sends a webhook for the `pid` passed in.

        Args:
            pid (int): PID to send.
        """
        webhook = self._build_webhook(pid)
        try:
            post(self.webhook + '?wait=true',
                headers = { 'Content-Type': 'application/json' },
                json = webhook
            )
        except Exception as e:
            with self.print_lock:
                print(c.red + f'⛔️ [{self.name.upper()}] [ERROR] Failed to send {pid} ({self.site.format_pid(pid)}): {e}' + c.reset)

    def send_all(self) -> None:
        """Checks if there are any products to save (send) and saves them if there are any.
        """
        if not self.send_queue.empty():
            print(f'🪣  [{self.name.upper()}] Adding new products into the database')

        while(not self.send_queue.empty()):
            pid = self.send_queue.get()    
            self._send_pid(pid)
            sleep(self.delay)
            with self.db_lock:
                print(c.yellow + f'🔌 [{self.name.upper()}] Added {pid} ({self.site.format_pid(pid)}) into the database' + c.reset)
                self.db.add_data(self.name, int(pid), self.site.format_pid(pid), self.site.image_url(pid))

    def _scrape(self, pids: List[int]) -> None:
        """Checks the PIDs passed in as an argument.

        Args:
            pids (List[int]): PIDs to check
        """
        with self.print_lock:
            print(f'🌎 [{self.name.upper()}] [{current_thread().name}] Scraping a total of {c.bold}{len(pids)}{c.reset} pids')
        for pid in pids:
            self.check_pid(pid)
        
        # check which pids were we checking in this method call and which failed
        local_failed_pids = [pid for pid in self._failed_pids if pid in pids]
        if len(local_failed_pids) > 0:
            with self.print_lock:
                print(c.yellow + f'🔁 [{self.name.upper()}] [{current_thread().name}] Retrying to check {c.bold}{len(local_failed_pids)}{c.reset}{c.yellow} (failed) pids' + c.reset)
            for pid in local_failed_pids:
                self.check_pid(pid)

    def scrape(self, num_threads: int, pids_per_thread: int = 100) -> None:
        """Starts `num_threads` workers, each scraping `pids_per_thread` provided.

        Args:
            num_threads (int): Number of threads to start
            pids_per_thread (int, optional): Number of PIDs to scrape per thread. Defaults to 100.
        """
        num_pids_each = pids_per_thread

        if self.stop_pid != -1:
            num_pids_each = ceil((self.stop_pid - self.start_pid) / num_threads)

        # create a list with all threads, generate a pid list to check for each of them
        i = 1
        for _ in range(num_threads):
            pids_todo = []
            for _ in range(num_pids_each):
                try:
                    pids_todo.append(next(self.pid_generator))
                # StopIteration exception is raised when there are no next elements
                except StopIteration:
                    continue
            
            if len(pids_todo) > 1:
                t = Thread(
                    name=f'{i:03}',
                    target=self._scrape,
                    args=(pids_todo,)
                )
                self.running_threads.append(t)
                i += 1

        print(c.yellow + f'🚧 [{self.name.upper()}] Starting {len(self.running_threads)} workers (each checking {num_pids_each} products)' + c.reset)
        
        # start all threads
        for t in self.running_threads:
            t.start()

            # sleep for a small amount just to slow down the spam a little
            sleep(self.delay)
            
            # in case we're starting a larger number of threads,
            # start the sender earlier (every 5 threads),
            # so we don't have to wait too long for all pids to send in the end
            if len(self.running_threads) > 20 and len(self.running_threads) % 5 == 0:
                self.send_all()

        # Keep checking for new pids in queue and sending them as soon as there are
        # workers alive
        while(any([t.is_alive() for t in self.running_threads])):
            self.send_all()
            sleep(10)

        # wait for all threads to end
        map(lambda t: t.join(), self.running_threads)
        print(c.orange + f'🚧 [{self.name.upper()}] All workers finished' + c.reset)

        print(f'💾 [{self.name.upper()}] Saving the rest of the PIDs, please wait')
        self.send_all()
        print('-------------------------------------------------------------')
        
        # TODO self._pids_checked not accurate due to threading overrides
        print(c.green + f'✅ [{self.name.upper()}] {c.bold}Scraping done!{c.reset}{c.green} Successfully checked ~{c.bold}{self._pids_checked}{c.reset}{c.green} pids.' + c.reset)

