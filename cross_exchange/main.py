import os
import asyncio
from typing import Dict, List
from cross_exchange.models import TradeConfig, StrategyConfig
from cross_exchange.exchange_manager import ExchangeManager
from cross_exchange.trader import Trader
from cross_exchange.strategy import CrossExchangeArbitrageStrategy
from dotenv import load_dotenv

load_dotenv()

DEFAULT_CONFIG: TradeConfig = TradeConfig(
  exchange_a=os.getenv('CROSS_EXCHANGE_EXCHANGE_A', 'binance'),
  exchange_b=os.getenv('CROSS_EXCHANGE_EXCHANGE_B', 'bybit'),
  position_size=float(os.getenv('CROSS_EXCHANGE_POSITION_SIZE', '1000.0')),
  taker_fee_a=float(os.getenv('CROSS_EXCHANGE_TAKER_FEE_A', '0.00055')),
  taker_fee_b=float(os.getenv('CROSS_EXCHANGE_TAKER_FEE_B', '0.00055')),
  safety_buffer=float(os.getenv('CROSS_EXCHANGE_SAFETY_BUFFER', '0.0001')),
  leverage=int(os.getenv('CROSS_EXCHANGE_LEVERAGE', '1')),
  margin_mode=os.getenv('CROSS_EXCHANGE_MARGIN_MODE', 'isolated'),
  paper_trading=os.getenv('CROSS_EXCHANGE_PAPER_TRADING', 'true').lower() == 'true',
  max_positions=int(os.getenv('CROSS_EXCHANGE_MAX_POSITIONS', '0')),
  symbol_to_trade=os.getenv('CROSS_EXCHANGE_SYMBOL_TO_TRADE', 'BTC/USDT:USDT')
)

def _get_api_keys() -> Dict[str, Dict[str, str]]:
  exchange_ids: List[str] = ['binance', 'bybit']
  credentials: Dict[str, Dict[str, str]] = {}
  for exchange_id in exchange_ids:
    api_key: str = os.getenv(f'{exchange_id.upper()}_API_KEY', '')
    api_secret: str = os.getenv(f'{exchange_id.upper()}_API_SECRET', '')
    if api_key and api_secret:
      credentials[exchange_id] = {'key': api_key, 'secret': api_secret}
  return credentials

async def run_strategy(config: TradeConfig = DEFAULT_CONFIG) -> None:
  credentials: Dict[str, Dict[str, str]] = _get_api_keys() if not config.paper_trading else {}
  exchange_manager: ExchangeManager = ExchangeManager(config)
  await exchange_manager.init_exchanges(
    exchange_ids=[config.exchange_a, config.exchange_b],
    credentials=credentials,
  )

  strategy_config: StrategyConfig = StrategyConfig(
    exchange_a=config.exchange_a,
    exchange_b=config.exchange_b,
    position_size=config.position_size,
    taker_fee_a=config.taker_fee_a,
    taker_fee_b=config.taker_fee_b,
    safety_buffer=config.safety_buffer,
    leverage=config.leverage,
    margin_mode=config.margin_mode,
    paper_trading=config.paper_trading,
    max_positions=config.max_positions,
    min_spread_threshold=((config.taker_fee_a + config.taker_fee_b) * 2 + config.safety_buffer) * 100,
    symbol_to_trade=config.symbol_to_trade
  )

  trader: Trader = Trader(
    exchange_manager,
    CrossExchangeArbitrageStrategy(strategy_config),
    strategy_config
  )
  await trader.run()

if __name__ == '__main__':
  asyncio.run(run_strategy())

