from abc import ABC, abstractmethod

class AbstractExchangeClient(ABC):

  @property
  @abstractmethod
  def id(self) -> str:
    pass

  @abstractmethod
  async def load_markets(self) -> None:
    pass

  @abstractmethod
  async def close(self) -> None:
    pass
