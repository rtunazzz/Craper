from typing import Callable, Iterator, Union
from craper.models.site import Site
from math import log10

class Mesh(Site):
    """Abstract Class representing a Mesh site

    Args:
        None
    
    Static Attributes:
        max_pid_digits: int
            Maximum number of digits a product ID can have
        host: str
            Hostname of the website

    Static Methods:
        parse_pid(pid)
        format_pid(pid)
        pid_stream(start, stop)
    
    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """

    max_pid_digits = 6
    # @property
    # @staticmethod
    # def max_pid_digits() -> int:
    #     return 6

    host = 'i1.adis.ws'
    # @property
    # @staticmethod
    # def host() -> str:
    #     return 'i1.adis.ws'
    
    @staticmethod
    def parse_pid(pid: Union[str, int]) -> int:
        return int(pid)

    @staticmethod
    def format_pid(pid: Union[str, int]) -> str:
        return f'{int(pid):06}'
    
    @staticmethod
    def pid_stream(start: int = 1, stop: int = -1) -> Iterator[int]:
        curr_pid = start
        # print(f'Starting stream from {start} to {stop}')

        # Checks if the PID provided is within the range provided in the method parameters
        in_range : Callable[[int], bool] = lambda pid: (pid <= stop) if (stop != -1) else True
        # print(f'in_range is {in_range(curr_pid)}')

        # Checks if the number of digits in the PID provided is smaller or equal to the maximum provided
        max_pid_reached : Callable[[int], bool] = lambda pid: (int(log10(pid)) + 1) > Mesh.max_pid_digits
        # print(f'max_pid_reached is {max_pid_reached(curr_pid)}')
        
        while(in_range(curr_pid) and not max_pid_reached(curr_pid)):
            yield curr_pid
            curr_pid += 1

class Footpatrol(Mesh):
    """Class representing footpatrol.com

    Args:
        None
    
    Static Attributes:
        max_pid_digits: int
            Maximum number of digits a product ID can have
        host: str
            Hostname of the website

    Static Methods:
        parse_pid(pid)
        image_url(pid)
        image_uri(pid)
        format_pid(pid)
        pid_stream(start, stop)
    
    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """

    @staticmethod
    def parse_pid(pid: Union[str, int]) -> int:
        return int(str(pid).replace('_footpatrolcom', ''))

    @staticmethod
    def format_pid(pid: Union[str, int]) -> str:
        return f'{Footpatrol.parse_pid(pid):06}_footpatrolcom'

    @staticmethod
    def image_url(pid: Union[str, int]) -> str:
        return f'http://i1.adis.ws/i/jpl/fp_{Footpatrol.parse_pid(pid):06}_a'
    
    @staticmethod
    def image_uri(pid: Union[str, int]) -> str:
        return f'/i/jpl/fp_{Footpatrol.parse_pid(pid):06}_a'

class Size(Mesh):
    """Class representing size.co.uk

    Args:
        None
    
    Static Attributes:
        max_pid_digits: int
            Maximum number of digits a product ID can have
        host: str
            Hostname of the website

    Static Methods:
        parse_pid(pid)
        image_url(pid)
        image_uri(pid)
        format_pid(pid)
        pid_stream(start, stop)
    
    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """

    @staticmethod
    def image_url(pid: Union[str, int]) -> str:
        return f'http://i1.adis.ws/i/jpl/sz_{Size.parse_pid(pid):06}_a'
    
    @staticmethod
    def image_uri(pid: Union[str, int]) -> str:
        return f'/i/jpl/sz_{Size.parse_pid(pid):06}_a'

class JDSports(Mesh):
    """Class representing jdsports.co.uk

    Args:
        None
    
    Static Attributes:
        max_pid_digits: int
            Maximum number of digits a product ID can have
        host: str
            Hostname of the website

    Static Methods:
        parse_pid(pid)
        image_url(pid)
        image_uri(pid)
        format_pid(pid)
        pid_stream(start, stop)
    
    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """

    @staticmethod
    def image_url(pid: Union[str, int]) -> str:
        return f'http://i1.adis.ws/i/jpl/jd_{JDSports.parse_pid(pid):06}_a'
    
    @staticmethod
    def image_uri(pid: Union[str, int]) -> str:
        return f'/i/jpl/jd_{JDSports.parse_pid(pid):06}_a'

class TheHipStore(Mesh):
    """Class representing thehipstore.co.uk

    Args:
        None
    
    Static Attributes:
        max_pid_digits: int
            Maximum number of digits a product ID can have
        host: str
            Hostname of the website

    Static Methods:
        parse_pid(pid)
        image_url(pid)
        image_uri(pid)
        format_pid(pid)
        pid_stream(start, stop)
    
    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """
    
    @staticmethod
    def image_url(pid: Union[str, int]) -> str:
        return f'http://i1.adis.ws/i/jpl/hp_{TheHipStore.parse_pid(pid):06}_a'
    
    @staticmethod
    def image_uri(pid: Union[str, int]) -> str:
        return f'/i/jpl/hp_{TheHipStore.parse_pid(pid):06}_a'
