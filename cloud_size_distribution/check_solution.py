"""
Validation script for cloud size distribution power-law exponent task.
"""
import pandas as pd
import numpy as np
import sys


def check_solution(submitted_path, answer_key_path, exponent_tolerance=0.03):
    """
    Check submitted solution against answer key for all cases.

    Parameters
    ----------
    submitted_path : str
        Path to submitted solution CSV
    answer_key_path : str
        Path to answer key CSV with all cases
    exponent_tolerance : float
        Absolute tolerance for exponent comparison (default: 0.03)

    Returns
    -------
    bool
        True if solution passes all checks
    """
    try:
        # Load submitted solution and answer key
        submitted = pd.read_csv(submitted_path)
        answer_key = pd.read_csv(answer_key_path)

        # Check columns exist in submitted
        required_cols = ['case', 'is_scaling', 'exponent']
        if not all(col in submitted.columns for col in required_cols):
            print(f"ERROR: Missing required columns. Expected {required_cols}")
            print(f"Found columns: {list(submitted.columns)}")
            return False

        # Check same cases present
        submitted_cases = set(submitted['case'].values)
        reference_cases = set(answer_key['case'].values)
        if submitted_cases != reference_cases:
            print(f"ERROR: Case mismatch")
            print(f"  Submitted: {sorted(submitted_cases)}")
            print(f"  Reference: {sorted(reference_cases)}")
            return False

        # Check each case
        all_passed = True
        for _, ref_row in answer_key.iterrows():
            case_name = ref_row['case']
            sub_row = submitted[submitted['case'] == case_name].iloc[0]

            # Extract values
            submitted_scaling = sub_row['is_scaling']
            reference_scaling = ref_row['is_scaling']
            submitted_exponent = sub_row['exponent']
            reference_exponent = ref_row['exponent']

            # Convert is_scaling to boolean if needed
            if isinstance(submitted_scaling, str):
                submitted_scaling = submitted_scaling.lower() in ['true', '1', 'yes']
            if isinstance(reference_scaling, str):
                reference_scaling = reference_scaling.lower() in ['true', '1', 'yes']

            submitted_scaling = bool(submitted_scaling)
            reference_scaling = bool(reference_scaling)

            # Check is_scaling matches
            if submitted_scaling != reference_scaling:
                print(f"✗ {case_name}: is_scaling mismatch (submitted={submitted_scaling}, expected={reference_scaling})")
                all_passed = False
                continue

            # Only check exponent if both are scaling
            if reference_scaling:
                exponent_diff = abs(submitted_exponent - reference_exponent)
                if exponent_diff > exponent_tolerance:
                    print(f"✗ {case_name}: exponent={submitted_exponent:.4f} (expected={reference_exponent:.4f}, diff={exponent_diff:.4f})")
                    all_passed = False
                else:
                    print(f"✓ {case_name}: exponent={submitted_exponent:.4f}")
            else:
                print(f"✓ {case_name}: non-scaling")

        if all_passed:
            print("\n✓ All cases passed!")
        else:
            print("\n✗ Some cases failed")

        return all_passed

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python check_solution.py <submitted.csv> <answer_key.csv>")
        print("Example: python check_solution.py test/solution.csv answer_key.csv")
        sys.exit(1)

    submitted_path = sys.argv[1]
    answer_key_path = sys.argv[2]

    passed = check_solution(submitted_path, answer_key_path)
    sys.exit(0 if passed else 1)
