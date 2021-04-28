from models import Footpatrol, Size, JDSports, TheHipStore,  Solebox, Snipes, Onygo
from db.db import DatabaseWrapper
from pathlib import Path
from os import path, makedirs

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
    def __init__(self, site_name: str) -> None:
        supported_sites = map(lambda site: site.lower(), SITES.keys())
        if site_name.lower() not in supported_sites:
            raise ValueError(f"Scaper for '{site_name}' is not supported.")
        
        self.name = site_name
        self.site = SITES[site_name.lower()]

        self._absolute_path = Path(__file__).parent.absolute()
        data_folder_path = f"{self._absolute_path}/data"
        if not path.exists(data_folder_path):
            makedirs(data_folder_path)       
 
        self.db = DatabaseWrapper(f"{data_folder_path}/{site_name}.db")

if __name__ == '__main__':
    s = Scraper('footpatrol')
    print(s.name)