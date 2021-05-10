#!/usr/bin/python3

from typing import List
from models import Footpatrol, Size, JDSports, TheHipStore,  Solebox, Snipes, Onygo, site
from db.db import DatabaseWrapper
from pathlib import Path
from os import path, makedirs
from queue import Queue
from threading import Lock, Thread, current_thread
from requests import post, head
from time import sleep
from math import ceil

SITES = {
    'footpatrol': Footpatrol,
    'size': Size,
    'jdsports': JDSports,
    'thehipstore': TheHipStore,
    'solebox': Solebox,
    'snipes': Snipes,
    'onygo': Onygo,
}

class Scraper:
    def __init__(self, site_name: str, webhook: str, start_pid: int = 1, stop_pid: int = -1) -> None:
        self.running_threads: List[Thread] = []

        self.db_lock = Lock()
        self.curr_lock = Lock()

        self.webhook = webhook
        self.send_queue = Queue()

        # Make sure the site is supported
        supported_sites = map(lambda site: site.lower(), SITES.keys())
        if site_name.lower() not in supported_sites:
            raise ValueError(f"Scaper for '{site_name}' is not supported.")
        
        if start_pid < 1:
            raise ValueError(f'The start_pid has to be greater or equal to 1.')
        elif stop_pid < -1:
            raise ValueError(f'The stop_pid has to be greater or equal to -1.')

        self.name = site_name
        self.site = SITES[site_name.lower()]()

        # Get the absotule path of the current file and initialize a database
        # in the project's root/data folder
        self._absolute_path = Path(__file__).parent.absolute()
        data_folder_path = f"{self._absolute_path}/data"
        if not path.exists(data_folder_path):
            makedirs(data_folder_path)       
    
        # Initialize our database
        self.db = DatabaseWrapper(f"{data_folder_path}/pids.db")
        
        # Make sure we have a table for the current site created
        self.db.create_table_safe(site_name.lower())
        
        # Load in the current pids (from previous scraping sessions)
        self.current_pids = self.db.get_pids_int(site_name)

        self.start_pid = start_pid
        self.stop_pid = stop_pid

        self.pid_generator = self.site.pid_stream(start_pid, stop_pid)

    def check_pid(self, pid):
        with self.curr_lock:
            # check if the pid isn't already loaded
            if pid in self.current_pids:
                return True

        # generate the image URL
        url = self.site.image_url(pid)

        # send a head request to check if the resource exists
        r = head(url)

        if r.status_code == 200:
            print(f'[{self.name.upper()}] Found a new pid {pid} ({self.site.format_pid(pid)})')
            # pid exists, save it
            self.current_pids.append(pid)
            self.send_queue.put(pid)
            return True
        
        return False

    def _build_embed(self, pid: int):
        return {
            "description": f'```{self.site.format_pid(pid)}```',
            "color": 0XFFADA2,
            "image": {
                "url": self.site.image_url(pid),
            },
            "author": {
                "name": self.name,
            },
            "footer": {
                "text": "@rtunazzz",
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
            print(f'[{self.name.upper()}] [ERROR] Failed to send {pid} ({self.site.format_pid(pid)}): {e}')

    def send_all(self):
        if not self.send_queue.empty():
            print(f'[{self.name.upper()}] Adding new products into the database.')

        while(not self.send_queue.empty()):
            pid = self.send_queue.get()    
            self._send_pid(pid)
            sleep(2)
            with self.db_lock:
                print(f'[{self.name.upper()}] Added {pid} ({self.site.format_pid(pid)}) into the database.')
                self.db.add_data(self.name, int(pid), self.site.format_pid(pid), self.site.image_url(pid))
            

    def _scrape(self, pids: List[int]) -> None:
        print(f'[{self.name.upper()}] [{current_thread().name}] Scraping a total of {len(pids)} pids')
        for pid in pids:
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

        # Keep checking for new pids in queue and sending them as soon as there are
        # workers alive
        while(any([t.is_alive() for t in self.running_threads])):
            self.send_all()
            sleep(10)

        # wait for all threads to end
        map(lambda t: t.join(), self.running_threads)
        print(f'[{self.name.upper()}] All workers finished')
        
        self.send_all()


if __name__ == '__main__':
    s = Scraper(
        'solebox',
        'https://discord.com/api/webhooks/XXXX',
        1931630
    )
    s.scrape(1)
