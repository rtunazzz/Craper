#!/usr/bin/python3

from math import ceil
from os import makedirs, path
from pathlib import Path
from queue import Queue
from threading import Lock, Thread, current_thread
from time import sleep
from typing import List, Union
from json import loads

from requests import head, post, exceptions
from random import choice as rand_choice

from db.db import DatabaseWrapper
from models import *

SITES = {
    'footpatrol': Footpatrol,
    'size': Size,
    'jdsports': JDSports,
    'thehipstore': TheHipStore,
    'solebox': Solebox,
    'snipes': Snipes,
    'onygo': Onygo,
}

def load_proxies(filename: str = 'proxies.txt', separator: str = '\n') -> list:
        """Reads proxies from a file and parses them to be ready to use with Python's `requests` library

        Args:
            filename (str, optional): Name of the file (.txt) where are the proxies located. Defaults to 'proxies.txt'.
            separator (str, optional): Separator by which is each proxy separated. Defaults to '\\n'
            
        Returns:
            formatted_proxy_list {list [dict]}: List of dictionaries, that are formatted and ready-to-use with Python
        """

        with open(filename, "r") as f:
            file_contents = f.read()
            file_contents = file_contents.split(separator)

        formatted_proxy_list = []
        try:
            try:
                # Userpass
                for i in range(0, len(file_contents)):
                    if ":" in file_contents[i]:
                        tmp = file_contents[i]
                        tmp = tmp.split(":")
                        proxies = {
                            "http": "http://" + tmp[2] + ":" + tmp[3] + "@" + tmp[0] + ":" + tmp[1] + "/",
                            "https": "http://" + tmp[2] + ":" + tmp[3] + "@" + tmp[0] + ":" + tmp[1] + "/",
                        }
                        formatted_proxy_list.append(proxies)
            except:
                # IP auth
                for n in range(0, len(file_contents)):
                    if ":" in file_contents[n]:
                        temp = file_contents[n]
                        proxies = {"http": "http://" + temp, "https": "http://" + temp}
                        formatted_proxy_list.append(proxies)
        except:
            return []
        return formatted_proxy_list


class Scraper:
    def __init__(self, site_name: str, start_pid: Union[int, str] = 1, stop_pid: Union[int, str] = -1, use_proxies: bool = False) -> None:
        self.running_threads: List[Thread] = []

        self.db_lock = Lock()
        self.curr_lock = Lock()
        self.print_lock = Lock()

        self.send_queue = Queue()

        # Get the absotule path of the current file
        self._absolute_path = Path(__file__).parent.absolute()
        data_folder_path = f"{self._absolute_path}/data"
        # create a data/ folder if it doesn't exist
        if not path.exists(data_folder_path):
            makedirs(data_folder_path)
        
        config_path = f"{self._absolute_path}/config.json"
        if not path.exists(config_path):
            raise FileNotFoundError(f"File 'config.json' not found in: {self._absolute_path}")
        
        # Make sure the site is supported
        supported_sites = map(lambda site: site.lower(), SITES.keys())
        if site_name.lower() not in supported_sites:
            raise ValueError(f"Scaper for '{site_name}' is not supported.")
        
        self.start_pid = int(start_pid)
        self.stop_pid = int(stop_pid)
        if self.start_pid < 1:
            raise ValueError(f'The start_pid has to be greater or equal to 1.')
        elif self.stop_pid < -1:
            raise ValueError(f'The stop_pid has to be greater or equal to -1.')

        self.name = site_name
        self.site = SITES[site_name.lower()]()

        # Load in config
        config_f = open(config_path).read()
        self.config = loads(config_f)
        
        if 'webhooks' not in self.config:
            raise ValueError(f"No 'webhooks' attribute found in the config.json file.")

        # Make sure a webhook is specified
        webhook_config = self.config['webhooks']
        if self.name not in webhook_config:
            # check if there's a webhook for rest
            if "rest" in webhook_config:
                self.webhook = webhook_config["rest"]
                print(f"[{self.name.upper()}] Webhook for '{self.name}' not found - using the 'rest' webhook.")
            else:
                raise ValueError(f"No webhook (nor a 'rest' webhook) specified for site {self.name}")
        else:
            print(f"[{self.name.upper()}] Using the '{self.name}' webhook.")
            self.webhook = webhook_config[self.name]

        self.embed_hex = int(self.config['embed']['color'].replace('#', ''), 16) if ('embed' in self.config and 'color' in self.config['embed']) else 0xFFADA2
        self.footer_text = self.config['embed']['footer']['text'] if ('embed' in self.config and 'footer' in self.config['embed'] and 'text' in self.config['embed']['footer']) else "@rtunazzz"
        
        # load in proxies if needed
        self.proxies = load_proxies() if use_proxies else []
    
        # Initialize our database in the project's root/data folder
        self.db = DatabaseWrapper(f"{data_folder_path}/pids.db")
        
        # Make sure we have a table for the current site created
        self.db.create_table_safe(site_name.lower())
        
        # Load in the current pids (from previous scraping sessions)
        self.current_pids = self.db.get_pids_int(site_name)
        self._failed_pids: List[int] = []

        self.pid_generator = self.site.pid_stream(self.start_pid, self.stop_pid)

    def __del__(self) -> None:
        if len(self._failed_pids) > 0:
            print(f"[{self.name.upper()}] Failed to check the follwing PIDs:")
            for pid in self._failed_pids:
                print(f'{self.site.format_pid(pid)}')

    def get_proxy(self):
        if len(self.proxies) > 1:
            return rand_choice(self.proxies)
        return {}

    def check_pid(self, pid):
        with self.curr_lock:
            # check if the pid isn't already loaded
            if pid in self.current_pids:
                return True

        # generate the image URL
        url = self.site.image_url(pid)

        try:
            # send a head request to check if the resource exists
            r = head(url, proxies=self.get_proxy())

            if r.status_code == 200:
                # 200 = loaded
                # pid exists, save it
                with self.print_lock:
                    print(f'[{self.name.upper()}] [{current_thread().name}] Found a new pid {pid} ({self.site.format_pid(pid)})')
                self.current_pids.append(pid)
                self.send_queue.put(pid)
                return True
            elif r.status_code == 404:
                # 404 = not loaded
                return False
            elif r.status_code == 403:
                print(f'[{self.name.upper()}] [{current_thread().name}] Proxy banned!')
            elif r.status_code == 429:
                with self.print_lock:
                    print(f'[{self.name.upper()}] [{current_thread().name}] Ratelimited!')
            else:
                print(f'[{self.name.upper()}] [{current_thread().name}] [{r.status_code}] Bad status code.')
        except exceptions.ProxyError as e:
            with self.print_lock:
                print(f'[{self.name.upper()}] [{current_thread().name}] Proxy failed - failed to check pid {pid} ({self.site.format_pid(pid)})')
                print(e)
        except exceptions.ConnectionError:
            with self.print_lock:
                print(f'[{self.name.upper()}] [{current_thread().name}] Failed to connect - failed to check pid {pid} ({self.site.format_pid(pid)})')
        
        self._failed_pids.append(pid)
        return False

    def _build_embed(self, pid: int):
        return {
            "description": f'```{self.site.format_pid(pid)}```',
            "color": self.embed_hex,
            "image": {
                "url": self.site.image_url(pid),
            },
            "author": {
                "name": self.name,
            },
            "footer": {
                "text": self.footer_text, 
            },
        }

    def _send_pid(self, pid: int):
        embed = self._build_embed(pid)
        try:
            post(self.webhook + '?wait=true',
                headers = { 'Content-Type': 'application/json' },
                json = { 'embeds': [embed] }
            )
        except Exception as e:
            with self.print_lock:
                print(f'[{self.name.upper()}] [ERROR] Failed to send {pid} ({self.site.format_pid(pid)}): {e}')

    def send_all(self):
        if not self.send_queue.empty():
            print(f'[{self.name.upper()}] Adding new products into the database')

        while(not self.send_queue.empty()):
            pid = self.send_queue.get()    
            self._send_pid(pid)
            sleep(1)
            with self.db_lock:
                print(f'[{self.name.upper()}] Added {pid} ({self.site.format_pid(pid)}) into the database')
                self.db.add_data(self.name, int(pid), self.site.format_pid(pid), self.site.image_url(pid))
            

    def _scrape(self, pids: List[int]) -> None:
        with self.print_lock:
            print(f'[{self.name.upper()}] [{current_thread().name}] Scraping a total of {len(pids)} pids')
        for pid in pids:
            self.check_pid(pid)
        
        # check which pids were we checking in this method call and which failed
        local_failed_pids = [pid for pid in self._failed_pids if pid in pids]
        if len(local_failed_pids) > 0:
            with self.print_lock:
                print(f'[{self.name.upper()}] [{current_thread().name}] Retrying to check {len(local_failed_pids)} (failed) pids')
            for pid in local_failed_pids:
                self.check_pid(pid)

    def scrape(self, num_threads: int, pids_per_thread: int = 100) -> None:
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
                    name=f'{self.name}{i:02}',
                    target=self._scrape,
                    args=(pids_todo,)
                )
                self.running_threads.append(t)
                i += 1

        print(f'[{self.name.upper()}] Starting {len(self.running_threads)} workers (each checking {num_pids_each} products)')
        
        # start all threads
        for t in self.running_threads:
            t.start()

            # sleep for a small amount just to slow down the spam a little
            sleep(len(self.running_threads) // 10)
            
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
        print(f'[{self.name.upper()}] All workers finished')
        
        print(f'[{self.name.upper()}] Saving the rest of the PIDs, please wait')
        self.send_all()
        print(f'[{self.name.upper()}] Scraping done')


if __name__ == '__main__':
    # for i in range(5):
    #     print('********************************************************')
    #     s = Scraper(
    #         'solebox',
    #         # 1931630
    #         1805000 + (5000 * i)
    #     )
    #     s.scrape(1)

    s = Scraper(
        'solebox',
        # 2009381,
        1944638,
        use_proxies=True
    )
    s.scrape(50)
