import asyncio
import ccxt.pro as ccxt_pro
from typing import Dict, Callable, Any
from copy import deepcopy
from cross_exchange.exchange_manager import ExchangeManager
from cross_exchange.strategy import CrossExchangeArbitrageStrategy
from cross_exchange.models import StrategyConfig
from cross_exchange.logger import logger

class Trader:
  def __init__(
    self,
    exchange_manager: ExchangeManager,
    strategy: CrossExchangeArbitrageStrategy,
    strategy_config: StrategyConfig,
  ) -> None:
    self._exchange_manager: ExchangeManager = exchange_manager
    self._strategy: CrossExchangeArbitrageStrategy = strategy
    self._strategy_config: StrategyConfig = strategy_config
    self._orderbook: Dict[str, Any] = {}
    self._orderbook_lock = asyncio.Lock()
    self._compute_running = False

  async def _watch_orderbook(
    self,
    exchange: ccxt_pro.Exchange,
    exchange_name: str,
    symbol: str,
    limit: int = 50
  ) -> None:
    while True:
      try:
        orderbook = await exchange.watch_order_book(symbol, limit)
        async with self._orderbook_lock:
          self._orderbook[exchange_name] = orderbook
      except Exception as e:
        logger.error(f"[{exchange_name}] Error watching orderbook: {e}")
        await asyncio.sleep(1)

  async def _compute(self, arbitrage_function: Callable) -> None:
    while True:
      if self._compute_running:
        await asyncio.sleep(0.1)
        continue
      
      async with self._orderbook_lock:
        if not self._orderbook:
          await asyncio.sleep(0.1)
          continue
        orderbook_snapshot = deepcopy(self._orderbook)
      
      self._compute_running = True
      try:
        await asyncio.to_thread(arbitrage_function, orderbook_snapshot)
      finally:
        self._compute_running = False
      
      await asyncio.sleep(0.1)

  async def run(self) -> None:
    try:
      exchange_a_pro = self._exchange_manager.get_ccxt_pro_client(self._strategy_config.exchange_a)
      exchange_b_pro = self._exchange_manager.get_ccxt_pro_client(self._strategy_config.exchange_b)
      
      if not exchange_a_pro or not exchange_b_pro:
        logger.error("Failed to create ccxt.pro clients")
        return
      
      await asyncio.gather(
        self._watch_orderbook(exchange_a_pro, self._strategy_config.exchange_a, self._strategy_config.symbol_to_trade),
        self._watch_orderbook(exchange_b_pro, self._strategy_config.exchange_b, self._strategy_config.symbol_to_trade),
        self._compute(self._strategy.arbitrage),
        return_exceptions=True
      )
    except Exception as e:
      logger.error(f"Error in trader run: {e}")
    finally:
      await self._exchange_manager.close_exchanges()


