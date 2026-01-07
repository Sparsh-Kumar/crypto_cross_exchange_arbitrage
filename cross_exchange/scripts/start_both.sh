cd "$(dirname "$0")/../.." || exit 1

if [ -d "venv" ]; then
  source venv/bin/activate
fi

echo "Starting Funding Rate Arbitrage Bot..."
python -m cross_exchange.main

