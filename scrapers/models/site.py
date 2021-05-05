from abc import ABC, abstractmethod, abstractproperty
from typing import Generator, Iterator, Union

class Site(ABC):
    """Abstract class representing a website

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

    @property
    @abstractmethod
    def max_pid_digits(self = None) -> int:
        """Represents the maximum number of digits a product ID can have"""
        raise ValueError("The max_pid_digits attribute is not defined on the child class.")

    @property
    @abstractmethod
    def host(self = None) -> str:
        """Represents a hostname"""
        raise ValueError("The host attribute is not defined on the child class.")


    @staticmethod
    @abstractmethod
    def image_url(pid: Union[str, int]) -> str:
        """Returns an URL of an image, picturing the product specified by the product ID (pid)

        Args:
            pid (Union[str, int]): ID of the product to get the image for
        """
        raise ValueError("The image_url method is not defined on the child class.")
    
    @staticmethod
    @abstractmethod
    def image_uri(pid: Union[str, int]) -> str:
        """Returns an URI of an image, picturing the product specified by the product ID (pid)

        Args:
            pid (Union[str, int]): ID of the product to get the image for
        """
        raise ValueError("The image_uri method is not defined on the child class.")
    
    @staticmethod
    @abstractmethod
    def format_pid(pid: Union[str, int]) -> str:
        """Formats the product ID (pid) provided into the expected formatting

        Args:
            pid (Union[str, int]): Product ID to format

        Returns:
            str: Formatted product ID
        """
        raise ValueError("The format_pid method is not defined on the child class.")
   
    @staticmethod
    @abstractmethod
    def pid_stream(start: int = 1, stop: int = -1) -> Iterator[int]:
        """Creates a stream which generates PIDs

        Args:
            start (int, optional): The beginning of the stream. Defaults to 1.
            stop (int, optional): The end of the stream. Defaults to -1, which means it generate PIDs to infinity.

        Returns:
            Iterator[int]: An iterator which will yiled PIDs.
        """
        raise ValueError("The pid_stream method is not defined on the child class.")
