#!/usr/bin/env python3
"""
Generate test data for cloud size distribution power-law exponent task.

Creates test cases with randomly selected Hurst exponents.
Each case contains binary arrays thresholded at 50th percentile.
"""
import numpy as np
import scaleinvariance
import os
from scipy.ndimage import gaussian_filter


def generate_all_variants(arrays_per_case_full=3, arrays_per_case_sparse=3, seed=42):
    """
    Generate all test variants at once.

    Parameters
    ----------
    num_cases_full : int
        Number of test cases for full data variants (test, test_hint)
    num_cases_sparse : int
        Number of test cases for sparse variants (test_sparse, test_sparse_hint)
    seed : int
        Random seed for reproducibility
    """
    np.random.seed(seed)

    array_size = 512

    # Define variants: directory name, number of arrays per case
    variants = [
        ("test", arrays_per_case_full),
        ("test_hint", arrays_per_case_full),
        ("test_sparse", arrays_per_case_sparse),
        ("test_sparse_hint", arrays_per_case_sparse),
    ]

    num_cases = 5

    H_values = np.random.uniform(0, .5, num_cases)


    print(f"H values: {H_values}")
    print(f"Array size: {array_size}x{array_size}")

    for case_idx in range(num_cases):
        H = H_values[case_idx]
        case_name = f"case_{case_idx + 1}"

        print(f"\n{case_name}: H = {H:.3f}")

        # Generate all arrays for this case
        all_arrays = []
        for array_idx in range(arrays_per_case_full):
            # Generate fBm field (make aperiodic by taking subset)
            field = scaleinvariance.acausal_fBm_2D(array_size*2, H)[:array_size, :array_size]

            # For case 4, apply Gaussian smoothing to break scale invariance
            if case_idx == 3:
                field = gaussian_filter(field, sigma=300)
                if array_idx == 0:
                    print(f"  Non-scaling case (Gaussian σ=300)")

            # Threshold at 50th percentile to create binary mask
            threshold = np.percentile(field, 50)
            binary = (field > threshold).astype(int)
            all_arrays.append(binary)

        # Save to each variant that needs this case
        for variant_dir, num_arrays_needed in variants:

            case_dir = os.path.join(variant_dir, "data", case_name)
            os.makedirs(case_dir, exist_ok=True)

            for array_idx in range(arrays_per_case_full):
                if array_idx >= num_arrays_needed: continue
                filename = f"array_{array_idx:03d}.npy"
                filepath = os.path.join(case_dir, filename)
                np.save(filepath, all_arrays[array_idx])

        print(f"  Saved to applicable variants")


if __name__ == '__main__':

    num_arrays_full = 300
    num_arrays_sparse = 10
    seed = 42

    print("="*60)
    print("Generating test data for cloud_size_distribution task")
    print("="*60)

    generate_all_variants(
        num_arrays_full,
        num_arrays_sparse,
        seed=seed
    )

    print("\n" + "="*60)
    print("✓ Data generation complete!")
    print("="*60)
