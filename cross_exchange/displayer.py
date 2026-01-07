import os
from datetime import datetime
from typing import List
from tabulate import tabulate
from cross_exchange.models import Spread

class Colors:
  RESET = '\033[0m'
  BOLD = '\033[1m'
  DIM = '\033[2m'
  BLACK = '\033[30m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  CYAN = '\033[96m'
  MAGENTA = '\033[95m'
  WHITE = '\033[97m'

class Displayer:
  def _colorize_spread(self, spread: float) -> str:
    if spread >= 0.1:
      return f'{Colors.GREEN}{spread:.4f}{Colors.RESET}'
    elif spread >= 0.05:
      return f'{Colors.YELLOW}{spread:.4f}{Colors.RESET}'
    else:
      return f'{Colors.DIM}{spread:.4f}{Colors.RESET}'

  def _colorize_rate(self, rate: float) -> str:
    if rate > 0:
      return f'{Colors.RED}{rate:.6f}{Colors.RESET}'
    elif rate < 0:
      return f'{Colors.GREEN}{rate:.6f}{Colors.RESET}'
    return f'{rate:.6f}'

  def _format_time_remaining(self, seconds: float) -> str:
    if seconds <= 0:
      return f'{Colors.RED}NOW{Colors.RESET}'
    hours: int = int(seconds // 3600)
    minutes: int = int((seconds % 3600) // 60)
    secs: int = int(seconds % 60)
    if hours > 0:
      return f'{Colors.DIM}{hours}h {minutes}m{Colors.RESET}'
    elif minutes > 0:
      if minutes <= 5:
        return f'{Colors.YELLOW}{minutes}m {secs}s{Colors.RESET}'
      return f'{Colors.DIM}{minutes}m {secs}s{Colors.RESET}'
    else:
      return f'{Colors.GREEN}{secs}s{Colors.RESET}'

  def _format_entry_status(self, is_in_window: bool) -> str:
    if is_in_window:
      return f'{Colors.GREEN}● READY{Colors.RESET}'
    return f'{Colors.DIM}○ WAIT{Colors.RESET}'

  def display_spreads(self, spreads: List[Spread], clean: bool = True) -> None:
    pass

