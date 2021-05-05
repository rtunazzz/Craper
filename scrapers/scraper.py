from models import Footpatrol, Size, JDSports, TheHipStore,  Solebox, Snipes, Onygo, site
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
    def __init__(self, site_name: str, start_pid: int = 1, stop_pid: int = -1) -> None:

        # Make sure site is supported
        supported_sites = map(lambda site: site.lower(), SITES.keys())
        if site_name.lower() not in supported_sites:
            raise ValueError(f"Scaper for '{site_name}' is not supported.")
        
        self.name = site_name
        self.site = SITES[site_name.lower()]()

        # Get the absotule path of the current file and initialize a database
        # in the project's root/data folder
        self._absolute_path = Path(__file__).parent.absolute()
        data_folder_path = f"{self._absolute_path}/data"
        if not path.exists(data_folder_path):
            makedirs(data_folder_path)       
 
        self.db = DatabaseWrapper(f"{data_folder_path}/{site_name}.db")

        if start_pid < 1:
            raise ValueError(f'The start_pid has to be greater or equal to 1.')
        elif stop_pid < -1:
            raise ValueError(f'The stop_pid has to be greater or equal to -1.')

        self.pid_generator = self.site.pid_stream(start_pid, stop_pid)

if __name__ == '__main__':
    s = Scraper('footpatrol')
    print(s.name)
    print(next(s.pid_generator))