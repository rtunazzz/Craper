<p align="center"><img width=80% src="https://i.imgur.com/zGXvGvf.png"></p>

# Craper
A collection of product scrapers for various websites.

### Supported sites
> Support for more websites yet to come.
 - Footpatrol
 - Size
 - JDSports EU
 - TheHipStore
 - Solebox
 - Snipes
 - Onygo


### Usage

#### Command
> Make sure to [install](#Installation) and [configure](#Configuration) the command before running.

```bash
# Show the usage info
craper -h

# Start a Footpatrol scraper
craper footpatrol

# Start 10 Footpatrol scrapers, each scraping 100 product IDs
craper footpatrol -t10 -n100

# Start one scraper with proxies, starting from pid 01925412
craper solebox -pt 1 -s 01925412
```

#### Python script
You may also run the scraper as a Python script. If you would rather not install the package, you can just clone this repo and run `python3 -m craper`.

![Example of the running command.](https://i.imgur.com/dI4g1Vq.png)

### Installation
After cloning this repository, run:
```bash
python3 -m pip install -r requirements.txt
```

### Configuration
