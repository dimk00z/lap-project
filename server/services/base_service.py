from abc import ABCMeta, abstractmethod
from typing import Any, Callable

from loguru import logger


class BaseService(metaclass=ABCMeta):
    @logger.catch(reraise=True)
    def __call__(self) -> Any:
        """Service entrypoint."""

        logger.debug(
            "Service {name} called with args: {args}",
            name=self.__class__.__name__,
            args=getattr(self, "__dict__") or getattr(self, "__slots__", None),
        )
        self.validate()
        return self.act()

    def get_validators(self) -> list[Callable]:
        """Get a list of validators."""
        return []

    def validate(self) -> None:
        """Validate input variables."""
        validators = self.get_validators()
        for validator in validators:
            validator()

    @abstractmethod
    def act(self) -> Any:
        """Do main service logic."""
        raise NotImplementedError(
            "Please implement in the service class",
        )
