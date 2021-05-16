<p align="center"><img width=80% src="https://i.imgur.com/zGXvGvf.png"></p>

# Craper
> A collection of product scrapers for various websites.

## What does this do?
This script can scrape product images from various websites (listed below) by their product IDs. Those product IDs then can be used to get early links/ early PIDs for each website.

When the command is ran, it looks for new products, saves any new ones into a database and sends you a Discord webhook for each new product found.

<br></br>

# Supported sites
> Support for more websites yet to come.

| Website name  | Command parameter | Website URL                     |
| ------------- | ----------------- | ------------------------------- |
| Footpatrol    | `footpatrol`      | https://www.footpatrol.com/     |
| Size          | `size`            | https://www.size.co.uk/         |
| JDSports (EU) | `jdsports`        | https://www.jdsports.co.uk/     |
| TheHipStore   | `thehipstore`     | https://www.thehipstore.co.uk/  |
| Solebox       | `solebox`         | https://solebox.com/            |
| Snipes        | `snipes`          | https://snipes.com/             |
| Onygo         | `onygo`           | https://onygo.com/              |

<br></br>

## Setup
> Python 3.9+ is required!

1. Clone this repository
```bash
git clone https://github.com/rtunazzz/Craper
```
2. Create required files
```bash
./bin/config.sh
```
3. Add your webhooks, footer & color preferences into the `craper/config/config.json` file.
4. (*Optional*) Add proxies to the `craper/config/proxies.txt` file
> If you're struggling with setting up these configuration files, I recommend checking out [these](./craper/config/examples.md) examples!

### Note
Proxy usage is not required but recommended for websites that ban often, such as Solebox, Snipes or Onygo.

<br></br>

## Installation
> Make sure to have everything [set up](###Setup) properly before installing.

```bash
python3 setup.py install
```

Then you can go ahead and start using the command:
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

<br></br>

## Example
```bash
craper size -t10 -n5 -s 10
```
![Example of the running command.](https://i.imgur.com/jA374SD.png)

------
Made by [__rtuna__](https://twitter.com/rtunazzz).
