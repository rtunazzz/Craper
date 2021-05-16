from typing import Union

from craper.models.demandware.shared import Demandware

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

    host = 'www.snipes.com'
    # @property
    # @staticmethod
    # def host() -> str:
    #     return 'www.snipes.com'
    
    @staticmethod
    def parse_pid(pid: Union[str, int]) -> int:
        # removeprefix only works on Python 3.9+ !!!
        return int(str(pid).removeprefix('000138'))

    @staticmethod
    def image_url(pid: Union[str, int]) -> str:
        return f'https://{Snipes.host}{Snipes.image_uri(pid)}'
    
    @staticmethod
    def image_uri(pid: Union[str, int]) -> str:
        return f'/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-snse-master-eu/default/dw538cba39/{Snipes.parse_pid(pid)}_P.jpg?sw=3000&sh=3000&sm=fit&sfrm=png'
    
    @staticmethod
    def format_pid(pid: Union[str, int]) -> str:
        return f'000138{int(pid):08}'
