from dataclasses import dataclass

@dataclass
class TradeConfig:
  exchange_a: str
  exchange_b: str
  position_size: float
  taker_fee_a: float = 0.00055
  taker_fee_b: float = 0.00055
  safety_buffer: float = 0.0001
  leverage: int = 1
  margin_mode: str = 'isolated'
  paper_trading: bool = True
  max_positions: int = 0
  symbol_to_trade: str = 'BTC/USDT:USDT'

@dataclass
class StrategyConfig(TradeConfig):
  min_spread_threshold: float = 0.0
