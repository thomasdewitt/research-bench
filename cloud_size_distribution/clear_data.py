#!/usr/bin/env python3
"""
Clear all generated test data directories.
"""
import os
import shutil


def clear_all_data():
    """
    Remove all data directories from all test variants.
    """
    variants = ['test', 'test_hint', 'test_sparse', 'test_sparse_hint']

    print("="*60)
    print("Clearing all test data directories")
    print("="*60)

    for variant_dir in variants:
        data_dir = os.path.join(variant_dir, "data")
        if os.path.exists(data_dir):
            print(f"  Removing {data_dir}...")
            shutil.rmtree(data_dir)
        else:
            print(f"  {data_dir} does not exist (skipping)")

    print("\n✓ All data directories cleared!")


if __name__ == '__main__':
    clear_all_data()
