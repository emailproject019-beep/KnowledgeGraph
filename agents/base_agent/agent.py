import abc
import logging
from typing import Any, Dict


class BaseAgent(abc.ABC):
    """
    Base class for all agents.

    Provides:
    - Config handling
    - Logger
    - Standard lifecycle: load() -> run() -> shutdown()
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.logger = self._init_logger()

    def _init_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.__class__.__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    @abc.abstractmethod
    def load(self) -> None:
        """Load models, clients, queues, etc."""
        raise NotImplementedError

    @abc.abstractmethod
    def run(self) -> None:
        """Main loop."""
        raise NotImplementedError

    def shutdown(self) -> None:
        """Cleanup resources."""
        self.logger.info("Shutting down agent.")
