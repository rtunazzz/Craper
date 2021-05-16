from typing import Union

from craper.models.demandware.shared import Demandware

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

    host = 'www.onygo.com'
    # @property
    # @staticmethod
    # def host() -> str:
    #     return 'www.onygo.com'

    @staticmethod
    def parse_pid(pid: Union[str, int]) -> int:
        # removeprefix only works on Python 3.9+ !!!
        return int(str(pid).removeprefix('000157'))

    @staticmethod
    def image_url(pid: Union[str, int]) -> str:
        return f'https://www.onygo.com/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-ong-master-de/default/dw4cb104b1/{Onygo.parse_pid(pid)}_P.jpg?sw=3000&sh=3000&sm=fit&sfrm=png'
    
    @staticmethod
    def image_uri(pid: Union[str, int]) -> str:
        return f'/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-ong-master-de/default/dw4cb104b1/{Onygo.parse_pid(pid)}_P.jpg?sw=3000&sh=3000&sm=fit&sfrm=png'
    
    @staticmethod
    def format_pid(pid: Union[str, int]) -> str:
        return f'000157{int(pid):08}'
