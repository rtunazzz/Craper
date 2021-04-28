from typing import Union
from models.site import Site

class Mesh(Site):
    """Class representing Mesh sites

    Args:
        None
    
    Static Attributes:
        host: str
            Hostname of the website

    Static Methods:
        image_url(pid)
        image_uri(pid)
        format_pid(pid)
    
    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """

    @property
    @staticmethod
    def host() -> str:
        return 'i1.adis.ws'
    
    @staticmethod
    def format_pid(pid: Union[str, int]) -> str:
        return f'{int(pid):06}'

class Footpatrol(Mesh):
    """Class representing footpatrol.com

    Args:
        None
    
    Static Attributes:
        host: str
            Hostname of the website

    Static Methods:
        image_url(pid)
        image_uri(pid)
        format_pid(pid)
    
    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """

    @staticmethod
    def image_url(pid: Union[str, int]) -> str:
        return f'http://i1.adis.ws/i/jpl/fp_{int(pid):06}_a'
    
    @staticmethod
    def image_uri(pid: Union[str, int]) -> str:
        return f'/i/jpl/fp_{int(pid):06}_a'

class Size(Mesh):
    """Class representing size.co.uk

    Args:
        None
    
    Static Attributes:
        host: str
            Hostname of the website

    Static Methods:
        image_url(pid)
        image_uri(pid)
        format_pid(pid)
    
    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """

    @staticmethod
    def image_url(pid: Union[str, int]) -> str:
        return f'http://i1.adis.ws/i/jpl/sz_{int(pid):06}_a'
    
    @staticmethod
    def image_uri(pid: Union[str, int]) -> str:
        return f'/i/jpl/sz_{int(pid):06}_a'

class JDSports(Mesh):
    """Class representing jdsports.co.uk

    Args:
        None
    
    Static Attributes:
        host: str
            Hostname of the website

    Static Methods:
        image_url(pid)
        image_uri(pid)
        format_pid(pid)
    
    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """

    @staticmethod
    def image_url(pid: Union[str, int]) -> str:
        return f'http://i1.adis.ws/i/jpl/jd_{int(pid):06}_a'
    
    @staticmethod
    def image_uri(pid: Union[str, int]) -> str:
        return f'/i/jpl/jd_{int(pid):06}_a'

class TheHipStore(Mesh):
    """Class representing thehipstore.co.uk

    Args:
        None
    
    Static Attributes:
        host: str
            Hostname of the website

    Static Methods:
        image_url(pid)
        image_uri(pid)
        format_pid(pid)
    
    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """
    
    @staticmethod
    def image_url(pid: Union[str, int]) -> str:
        return f'http://i1.adis.ws/i/jpl/hp_{int(pid):06}_a'
    
    @staticmethod
    def image_uri(pid: Union[str, int]) -> str:
        return f'/i/jpl/hp_{int(pid):06}_a'
