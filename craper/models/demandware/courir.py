from typing import Union

from craper.models.demandware.shared import Demandware

class Courir(Demandware):
    """Class representing Courir

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
    
    Methods:
        build_embed(color, author_name, footer_text, pid)

    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """

    host = 'www.courir.com'
    # @property
    # @staticmethod
    # def host() -> str:
    #     return 'www.courir.com'

    @staticmethod
    def parse_pid(pid: Union[str, int]) -> int:
        # removeprefix only works on Python 3.9+ !!!
        return int(str(pid).removeprefix('00'))

    @staticmethod
    def image_url(pid: Union[str, int]) -> str:
        return f'https://{Courir.host}{Courir.image_uri(pid)}'
    
    @staticmethod
    def image_uri(pid: Union[str, int]) -> str:
        return f'/on/demandware.static/-/Sites-master-catalog-courir/default/dw227c85ea/images/hi-res/{Courir.parse_pid(pid):09}_101.png'
    
    @staticmethod
    def format_pid(pid: Union[str, int]) -> str:
        return f'{int(pid)}'
