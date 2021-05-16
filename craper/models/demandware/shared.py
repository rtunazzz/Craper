from math import log10
from typing import Callable, Iterator, Union

from craper.models.site import Site

class Demandware(Site):
    """Abstract class representing a Demandware site

    Args:
        None
    
    Static Attributes:
        max_pid_digits: int
            Maximum number of digits a product ID can have

    Static Methods:
        parse_pid(pid)
        pid_stream(start, stop)

    Methods:
        build_embed(color, author_name, footer_text, pid)

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
    def parse_pid(pid: Union[str, int]) -> int:
        return int(pid)
    
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
