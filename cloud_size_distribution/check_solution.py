"""
Validation script for cloud size distribution task.
"""
import pandas as pd
import numpy as np
import sys


def check_solution(submitted_path, reference_path, tolerance=1e-6):
    """
    Check submitted solution against reference.

    Parameters
    ----------
    submitted_path : str
        Path to submitted solution CSV
    reference_path : str
        Path to reference solution CSV
    tolerance : float
        Numerical tolerance for comparison

    Returns
    -------
    bool
        True if solution passes all checks
    """
    try:
        # Load both solutions
        submitted = pd.read_csv(submitted_path)
        reference = pd.read_csv(reference_path)

        # Check columns exist
        required_cols = ['size', 'count']
        if not all(col in submitted.columns for col in required_cols):
            print(f"ERROR: Missing required columns. Expected {required_cols}")
            return False

        # Sort both by size for comparison
        submitted = submitted.sort_values('size').reset_index(drop=True)
        reference = reference.sort_values('size').reset_index(drop=True)

        # Check same sizes present
        if not np.array_equal(submitted['size'].values, reference['size'].values):
            print("ERROR: Size values don't match reference")
            return False

        # Check counts match within tolerance
        if not np.allclose(submitted['count'].values, reference['count'].values,
                          rtol=tolerance, atol=tolerance):
            print("ERROR: Count values don't match reference within tolerance")
            max_diff = np.max(np.abs(submitted['count'].values - reference['count'].values))
            print(f"Maximum difference: {max_diff}")
            return False

        print("✓ Solution passed all checks!")
        return True

    except Exception as e:
        print(f"ERROR: {e}")
        return False


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python check_solution.py <submitted.csv> <reference.csv>")
        sys.exit(1)

    submitted_path = sys.argv[1]
    reference_path = sys.argv[2]

    passed = check_solution(submitted_path, reference_path)
    sys.exit(0 if passed else 1)
