import asyncio
from typing import Dict, List, Any, Optional
import ccxt.pro as ccxt_pro
from cross_exchange.models import TradeConfig
from cross_exchange.ccxt_exchange_client import CCXTExchangeClient
from cross_exchange.abstracts.abstract_exchange_client import AbstractExchangeClient

class ExchangeManager:
  def __init__(self, trade_config: TradeConfig | None = None) -> None:
    if not trade_config:
      raise ValueError('Trade config is required.')
    self._trade_config: TradeConfig = trade_config
    self._exchange_clients: Dict[str, AbstractExchangeClient] = {}

  async def init_exchanges(
    self,
    exchange_ids: List[str],
    credentials: Optional[Dict[str, Dict[str, str]]] = None,
  ) -> None:
    credentials = credentials or {}
    for exchange_id in exchange_ids:
      exchange_credentials: Dict[str, str] = credentials.get(exchange_id, {})
      exchange_client: CCXTExchangeClient = CCXTExchangeClient(
        exchange_id=exchange_id,
        api_key=exchange_credentials.get('key') or '',
        api_secret=exchange_credentials.get('secret') or '',
      )
      await exchange_client.load_markets()
      self._exchange_clients[exchange_id] = exchange_client

  async def close_exchanges(self) -> None:
    await asyncio.gather(*[client.close() for client in self._exchange_clients.values()])

  def get_exchange_client(self, exchange_id: str) -> AbstractExchangeClient | None:
    return self._exchange_clients.get(exchange_id)

  def get_ccxt_pro_client(self, exchange_id: str) -> Any | None:
    client = self._exchange_clients.get(exchange_id)
    if not client:
      return None
    return getattr(ccxt_pro, exchange_id)(client.exchange_config)
