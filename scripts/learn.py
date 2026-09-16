#!/usr/bin/env python3
"""
Learning loop — analisa outcomes + update weights.
Dijalankan via cron setiap hari.

Usage:
    python3 scripts/learn.py
    python3 scripts/learn.py --min-samples 10
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.brain import brain


def main():
    parser = argparse.ArgumentParser(description='Learning loop')
    parser.add_argument('--min-samples', type=int, default=5,
                       help='Minimal samples per aspek')
    args = parser.parse_args()
    
    print(f"🧠 Learning from outcomes (min_samples={args.min_samples})...")
    
    result = brain.learn_from_outcomes(min_samples=args.min_samples)
    
    print(f"\nTotal decisions: {result.get('total_decisions', 0)}")
    print(f"Evaluated: {result.get('evaluated_decisions', 0)}")
    print(f"Aspek with accuracy: {result.get('aspek_with_accuracy', 0)}")
    print(f"Updated: {result.get('updated', False)}")
    
    if result.get('accuracy'):
        print(f"\n=== Top 10 Accuracy ===")
        sorted_acc = sorted(result['accuracy'].items(), key=lambda x: -x[1]['accuracy'])
        for aspect, stats in sorted_acc[:10]:
            print(f"  {aspect:20} {stats['accuracy']:.3f} ({stats['wins']}/{stats['samples']})")
    
    if result.get('weights'):
        print(f"\n=== Top 10 Weights ===")
        sorted_w = sorted(result['weights'].items(), key=lambda x: -x[1])
        for aspect, weight in sorted_w[:10]:
            print(f"  {aspect:20} {weight:.4f}")
    
    print(f"\n✅ Done")


if __name__ == '__main__':
    main()
