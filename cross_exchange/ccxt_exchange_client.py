import ccxt.async_support as ccxt
from typing import Optional, Dict, Any
from cross_exchange.abstracts.abstract_exchange_client import AbstractExchangeClient

class CCXTExchangeClient(AbstractExchangeClient):

  def __init__(
    self,
    exchange_id: str,
    api_key: Optional[str] = None,
    api_secret: Optional[str] = None,
  ) -> None:
    self._exchange_id: str = exchange_id
    exchange_class: Any = getattr(ccxt, exchange_id, None)
    if not exchange_class:
      raise ValueError(f'Unsupported exchange: {exchange_id}')

    self._exchange_config: Dict[str, Any] = {
      'enableRateLimit': True,
      'options': {'defaultType': 'swap'},
      'apiKey': api_key or '',
      'secret': api_secret or '',
    }
    self._exchange_client: ccxt.Exchange = exchange_class(self._exchange_config)

  @property
  def id(self) -> str:
    return self._exchange_id

  @property
  def exchange_config(self) -> Dict[str, Any]:
    return self._exchange_config

  async def load_markets(self) -> None:
    await self._exchange_client.load_markets()

  async def close(self) -> None:
    await self._exchange_client.close()


