# New PID Scrapers
A collection of new PID scrapers for various websites.

### Usage
```sh
python3 main.py -h
# Shows the usage info

python3 main.py footpatrol
# Starts a Footpatrol scraper

python3 main.py footpatrol -t10 -n100
# Starts 10 Footpatrol scrapers, each scraping 100 product IDs

python3 main.py solebox -pt 1 -s 01925412
# Starts one scraper for Solebox product IDs
# with proxies, from pid 01925412
```
![Example of the running command.](./cdn/example.png)

### Installation
After cloning this repository, run:
```sh
python3 -m pip install -r requirements.txt
```

### Configuration

## Todo
- [x] Finish readme
- [x] Add terminal colors
- [x] Support commandline arguments
- [ ] Tests
- [ ] ? Script for adding additional sites
