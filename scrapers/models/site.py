from abc import ABC, abstractmethod, abstractproperty
from typing import Union

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
    
    Raises:
        ValueError
            When required method(s) / attributes are not implemented
    """

    @property
    @staticmethod
    @abstractmethod
    def max_pid_digits() -> int:
        """Represents the maximum number of digits a product ID can have"""
        raise ValueError("The max_pid_digits attribute is not defined on the child class.")

    @property
    @staticmethod
    @abstractmethod
    def host() -> str:
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
