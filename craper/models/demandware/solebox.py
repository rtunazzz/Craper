from typing import Union

from craper.models.demandware.shared import Demandware

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

    host = 'www.solebox.com'
    # @property
    # @staticmethod
    # def host() -> str:
    #     return 'www.solebox.com'

    @staticmethod
    def parse_pid(pid: Union[str, int]) -> int:
        return int(pid)

    @staticmethod
    def image_url(pid: Union[str, int]) -> str:
        return f'https://{Solebox.host}{Solebox.image_uri(pid)}'
    
    @staticmethod
    def image_uri(pid: Union[str, int]) -> str:
        return f'/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-solebox-master-de/default/dw1220ea0d/{Solebox.parse_pid(pid)}_PS.jpg?sw=3000&sh=3000&sm=fit&sfrm=png'
    
    @staticmethod
    def format_pid(pid: Union[str, int]) -> str:
        return f'{Solebox.parse_pid(pid):08}'
