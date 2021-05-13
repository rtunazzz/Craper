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

### Configuration
1. Clone this repository
```bash
$   git clone https://github.com/rtunazzz/Craper
```
2. Create required files
```bash
$   ./bin/config.sh
```
3. Add your webhooks, footer & color preferences into the `craper/config/config.json` file.
4. (*Optional*) Add proxies to the `craper/config/proxies.txt` file
> If you're struggling with setting up these configuration files, I recommend checking out [these](./craper/config/examples.md) examples!

### Installation
> Make sure to have everything [configured](###Configuration) before installing.

```bash
$   python3 setup.py install
```

Then you can go ahead and start using the command:
```bash
    # Show the usage info
$   craper -h

    # Start a Footpatrol scraper
$   craper footpatrol

    # Start 10 Footpatrol scrapers, each scraping 100 product IDs
$   craper footpatrol -t10 -n100

    # Start one scraper with proxies, starting from pid 01925412
$   craper solebox -pt 1 -s 01925412
```

#### Python script
You may also run the scraper as a Python script. If you would rather not install the package, you can just clone this repo and run `python3 -m craper`.

![Example of the running command.](https://i.imgur.com/dI4g1Vq.png)
