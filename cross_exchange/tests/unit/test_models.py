import pytest
from cross_exchange.models import FundingRate, TradeConfig, StrategyConfig


class TestFundingRate:

  def test_create_funding_rate(self):
    rate = FundingRate(exchange="binance", symbol="BTC/USDT:USDT", rate=0.0001)
    assert rate.exchange == "binance"
    assert rate.symbol == "BTC/USDT:USDT"
    assert rate.rate == 0.0001


class TestTradeConfig:

  def test_default_values(self):
    config = TradeConfig(
      exchange_a="binance",
      exchange_b="bybit",
      position_size=100.0
    )
    assert config.paper_trading is True
    assert config.leverage == 1


