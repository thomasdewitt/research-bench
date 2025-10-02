#!/usr/bin/env python3
"""
Compute solutions for all test variants and save answer keys.
"""
import numpy as np
import pandas as pd
import objscale
import os
import glob


def compute_all_solutions(variant_data_dir = "test/data"):
    """
    Compute solutions using test/ variant only.
    Copies answer key to all other variants.
    """
    print("="*60)
    print(f"Computing solutions from {variant_data_dir}")
    print("="*60)

    
    if not os.path.exists(variant_data_dir):
        raise ValueError(f"{variant_data_dir} does not exist!")

    # Find all case directories in test/data
    case_dirs = sorted(glob.glob(os.path.join(variant_data_dir, "case_*")))

    results = []
    for case_dir in case_dirs:
        case_name = os.path.basename(case_dir)

        # Load all arrays for this case
        array_files = sorted(glob.glob(os.path.join(case_dir, "array_*.npy")))
        binary_arrays = [np.load(f) for f in array_files]

        print(f"  {case_name}: {len(binary_arrays)} arrays", end=" ")

        # Determine if scaling (case_4 is non-scaling)
        is_scaling = (case_name != "case_4")

        if is_scaling:
            (exponent, error) = objscale.finite_array_powerlaw_exponent(
                binary_arrays, 'area', return_counts=False
            )
            print(f"τ={exponent:.3f}±{error:.3f} ✓")
        else:
            exponent = np.nan
            print(f"Non-scaling ✗")

        results.append({
            'case': case_name,
            'is_scaling': is_scaling,
            'exponent': exponent
        })

    # Create answer key dataframe
    answer_key_df = pd.DataFrame(results)

    # Save answer key
    answer_key_df.to_csv("answer_key.csv", index=False)

    print("\n" + "="*60)
    print("✓ Solutions computed!")
    print("="*60)


if __name__ == '__main__':
    compute_all_solutions(variant_data_dir = "test/data")
    # compute_all_solutions(variant_data_dir = "test_sparse/data")

