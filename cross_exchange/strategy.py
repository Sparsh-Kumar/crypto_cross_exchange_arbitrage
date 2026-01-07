from typing import Dict, Any
from collections import deque
from cross_exchange.models import StrategyConfig
from cross_exchange.logger import logger

class CrossExchangeArbitrageStrategy:

  def __init__(
    self,
    config: StrategyConfig | None = None,
  ) -> None:
    if not config:
      raise ValueError('Strategy config is required.')
    self._config: StrategyConfig = config
    self._mid_price_sync_limit: int = 2000
    self._mid_prices: Dict[str, deque] = {}

  @property
  def config(self) -> StrategyConfig:
    return self._config

  def _calculate_mid_price(self, orderbook: Any | None = None) -> float:
    best_bid = orderbook['bids'][0][0]
    best_ask = orderbook['asks'][0][0]
    mid_price = (best_bid + best_ask) / 2
    return mid_price

  def arbitrage(self, orderbooks: Dict[str, Any] | None = None) -> None:

    is_enough_data_collected: bool = True

    if not orderbooks or self.config.exchange_a not in orderbooks or self.config.exchange_b not in orderbooks:
      return

    for exchange, orderbook in orderbooks.items():
      mid_price = self._calculate_mid_price(orderbook)
      if exchange not in self._mid_prices:
        self._mid_prices[exchange] = deque(maxlen=self._mid_price_sync_limit)
      self._mid_prices[exchange].append(mid_price)


    for _, midprices in self._mid_prices.items():
      if len(midprices) < self._mid_price_sync_limit:
        is_enough_data_collected = False

    if not is_enough_data_collected:
      logger.info(f'Synced exchange A - {len(self._mid_prices[self.config.exchange_a])}, exchange B - {len(self._mid_prices[self.config.exchange_b])}')
      return

    print(orderbooks)
