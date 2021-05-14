#!/usr/bin/env python3

from argparse import ArgumentParser
from craper.scraper import Scraper
from sys import exit, path
import os

parser = ArgumentParser(description='cScraper - new product scraper')

parser.add_argument('site', metavar='<SITE_NAME>', type=str, help='Name of the site to scrape')

parser.add_argument('-t', '--threads', metavar='<number>', type=int, default=10, help='Number of threads to run')
parser.add_argument('-n', '--perthread', metavar='<number>', type=int, help='Number of PIDs per thread')
parser.add_argument('-s', '--start', metavar='<pid>', type=str, default='1', help='Product ID to start from')
parser.add_argument('-e', '--end', metavar='<pid>', type=str, default='-1', help='Product ID to end at')
parser.add_argument('-d', '--delay', metavar='<number>', type=int, default=1, help='Delay which slows down the script (to prevent bans)')
parser.add_argument('-p', '--proxies', action='store_true', help='Use proxies')
parser.add_argument('--db', metavar='<path>', type=str, default=None, help='Absolute path to a database to store the PIDs')
parser.add_argument('--debug', action='store_true', help='Turns on debugging mode, logs more info.')

args = parser.parse_args()

def main():
    if args.db != None and args.db.startswith('.'):
        print("ERROR: Wrong path provided. Make sure you provide an ABSOLUTE path.")
        return

    try:
        s = Scraper(
            site_name=args.site,
            start_pid=args.start,   
            stop_pid=args.end,
            use_proxies=args.proxies,
            debug=args.debug,
            delay=args.delay,
            db_path=args.db,
        )

        if args.perthread is not None:
            s.scrape(
                num_threads=args.threads,
                pids_per_thread=args.perthread,
            )
        else:
            s.scrape(num_threads=args.threads)
    except KeyboardInterrupt:
        exit(1)

if __name__ == '__main__':
    main()
