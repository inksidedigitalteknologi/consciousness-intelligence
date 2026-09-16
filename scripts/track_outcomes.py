#!/usr/bin/env python3
"""
Track outcomes untuk semua decision.
Dijalankan via cron setiap hari.

Usage:
    python3 scripts/track_outcomes.py
    python3 scripts/track_outcomes.py --days 1
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.brain import brain


def main():
    parser = argparse.ArgumentParser(description='Track decision outcomes')
    parser.add_argument('--days', type=int, default=0, choices=[0, 1, 7, 30],
                       help='Days to evaluate (0 = all: 1, 7, 30)')
    args = parser.parse_args()
    
    print(f"🔄 Tracking outcomes...")
    
    if args.days == 0:
        # Evaluate semua
        for days in [1, 7, 30]:
            print(f"\n=== Evaluating {days}d outcomes ===")
            result = brain.evaluate_pending_decisions(days=days)
            print(f"  Evaluated: {result.get('evaluated', 0)}")
            print(f"  Success: {result.get('success', 0)}")
            print(f"  Failed: {result.get('failed', 0)}")
    else:
        print(f"\n=== Evaluating {args.days}d outcomes ===")
        result = brain.evaluate_pending_decisions(days=args.days)
        print(f"  Evaluated: {result.get('evaluated', 0)}")
        print(f"  Success: {result.get('success', 0)}")
        print(f"  Failed: {result.get('failed', 0)}")
    
    # Stats
    print(f"\n=== Stats ===")
    stats = brain.get_decision_stats()
    print(f"  Total decisions: {stats.get('total', 0)}")
    print(f"  Evaluated: {stats.get('evaluated', 0)}")
    print(f"  Wins: {stats.get('wins_30d', 0)}")
    print(f"  Losses: {stats.get('losses_30d', 0)}")
    if stats.get('win_rate'):
        print(f"  Win rate: {stats.get('win_rate'):.1f}%")
    else:
        print(f"  Win rate: N/A (belum ada evaluasi)")
    
    print(f"\n✅ Done")


if __name__ == '__main__':
    main()
