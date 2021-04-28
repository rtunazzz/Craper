from .models.snipes import Snipes

SITES = {
    'footpatrol': Snipes,
    'size': Snipes,
    'jdsports': Snipes,
    'thehipstore': Snipes,
    'solebox': Snipes,
    'snipes': Snipes,
    'onygo': Snipes,
}

class Scraper:
    def __init__(self, site_name: str) -> None:
        supported_sites = map(lambda site: site.lower(), SITES.keys())
        if site_name.lower() not in supported_sites:
            raise ValueError(f"Scaper for '{site_name}' is not supported.")
        
        self.name = site_name
        self.site = SITES[site_name.lower()]
