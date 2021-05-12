from typing import Callable, Iterator, Union
from scrapers.models.site import Site
from math import log10

class Demandware(Site):
    """Abstract class representing a Demandware site

    Args:
        None
    
    Static Attributes:
        max_pid_digits: int
            Maximum number of digits a product ID can have

    Static Methods:
        pid_stream(start, stop)
    
    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """

    max_pid_digits = 7
    # @property
    # @staticmethod
    # def max_pid_digits() -> int:
    #     return 7
    
    @staticmethod
    def pid_stream(start: int = 1, stop: int = -1) -> Iterator[int]:
        curr_pid = start
        # print(f'Starting stream from {start} to {stop}')

        # Checks if the PID provided is within the range provided in the method parameters
        in_range : Callable[[int], bool] = lambda pid: (pid <= stop) if (stop != -1) else True
        # print(f'in_range is {in_range(curr_pid)}')

        # Checks if the number of digits in the PID provided is smaller or equal to the maximum provided
        max_pid_reached : Callable[[int], bool] = lambda pid: (int(log10(pid)) + 1) > Demandware.max_pid_digits
        # print(f'max_pid_reached is {max_pid_reached(curr_pid)}')
        
        while(in_range(curr_pid) and not max_pid_reached(curr_pid)):
            yield curr_pid
            curr_pid += 1

class Solebox(Demandware):
    """Class representing Solebox

    Args:
        None
    
    Static Attributes:
        max_pid_digits: int
            Maximum number of digits a product ID can have
        host: str
            Hostname of the website

    Static Methods:
        image_url(pid)
        image_uri(pid)
        format_pid(pid)
        pid_stream(start, stop)
    
    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """

    host = 'www.solebox.com'
    # @property
    # @staticmethod
    # def host() -> str:
    #     return 'www.solebox.com'

    @staticmethod
    def image_url(pid: Union[str, int]) -> str:
        return f'https://www.solebox.com/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-solebox-master-de/default/dw1220ea0d/{int(pid)}_PS.jpg?sw=3000&sh=3000&sm=fit&sfrm=png'
    
    @staticmethod
    def image_uri(pid: Union[str, int]) -> str:
        return f'/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-solebox-master-de/default/dw1220ea0d/{int(pid)}_PS.jpg?sw=3000&sh=3000&sm=fit&sfrm=png'
    
    @staticmethod
    def format_pid(pid: Union[str, int]) -> str:
        return f'0{int(pid):07}'

class Snipes(Demandware):
    """Class representing Snipes

    Args:
        None
    
    Static Attributes:
        max_pid_digits: int
            Maximum number of digits a product ID can have
        host: str
            Hostname of the website

    Static Methods:
        image_url(pid)
        image_uri(pid)
        format_pid(pid)
        pid_stream(start, stop)
    
    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """

    host = 'www.snipes.com'
    # @property
    # @staticmethod
    # def host() -> str:
    #     return 'www.snipes.com'

    @staticmethod
    def image_url(pid: Union[str, int]) -> str:
        return f'https://www.snipes.com/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-snse-master-eu/default/dw538cba39/{int(pid)}_PS.jpg?sw=3000&sh=3000&sm=fit&sfrm=png'
    
    @staticmethod
    def image_uri(pid: Union[str, int]) -> str:
        return f'/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-snse-master-eu/default/dw538cba39/{int(pid)}_PS.jpg?sw=3000&sh=3000&sm=fit&sfrm=png'
    
    @staticmethod
    def format_pid(pid: Union[str, int]) -> str:
        return f'0001380{int(pid):07}'

class Onygo(Demandware):
    """Class representing Onygo

    Args:
        None
    
    Static Attributes:
        max_pid_digits: int
            Maximum number of digits a product ID can have
        host: str
            Hostname of the website

    Static Methods:
        image_url(pid)
        image_uri(pid)
        format_pid(pid)
        pid_stream(start, stop)
    
    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """

    host = 'www.onygo.com'
    # @property
    # @staticmethod
    # def host() -> str:
    #     return 'www.onygo.com'

    @staticmethod
    def image_url(pid: Union[str, int]) -> str:
        return f'https://www.onygo.com/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-ong-master-de/default/dw4cb104b1/{int(pid)}_PS.jpg?sw=3000&sh=3000&sm=fit&sfrm=png'
    
    @staticmethod
    def image_uri(pid: Union[str, int]) -> str:
        return f'/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-ong-master-de/default/dw4cb104b1/{int(pid)}_PS.jpg?sw=3000&sh=3000&sm=fit&sfrm=png'
    
    @staticmethod
    def format_pid(pid: Union[str, int]) -> str:
        return f'0001570{int(pid):07}'
