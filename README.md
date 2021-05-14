<p align="center"><img width=80% src="https://i.imgur.com/zGXvGvf.png"></p>

# Craper
> A collection of product scrapers for various websites.

Scrapes new products, sends them through a Discord webhook and saves them into a database.

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
There is two ways you can install this. Either as a global command, which will be always available from your terminal or just as a Python script.
> Make sure to have everything [set up](###Setup) properly before installing.

#### As a command
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

#### Python script
You may also run the scraper as a Python script. If you would rather not install the package, you can just clone this repo and run `python3 -m craper`.

<br></br>

## Example
```bash
craper size -t10 -n5 -s 10
```
![Example of the running command.](https://i.imgur.com/jA374SD.png)

## FAQ
#### I am getting an error saying something like `file not found`/ `file doesn't exist`
You likely either didn't clone this repository or didn't change the active directory of your terminal to this repo. Check out [this](https://projectdestroyer.com/2018/01/run-scripts-github/) article from Project Destroyer and follow the steps mentioned.


------
Made by [__rtuna__](https://twitter.com/rtunazzz).
