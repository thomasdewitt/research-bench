"""
Reference implementation for cloud size distribution analysis.
"""
import numpy as np
import pandas as pd
import objscale


def compute_cloud_size_distribution(mask_path, output_path):
    """
    Compute cloud object size distribution from binary mask.

    Parameters
    ----------
    mask_path : str
        Path to binary mask (.npy file)
    output_path : str
        Path to save CSV output
    """
    # Load binary mask
    mask = np.load(mask_path)

    # Compute size distribution accounting for finite array effects
    sizes, counts = objscale.finite_array_size_distribution(mask)

    # Create DataFrame and save
    df = pd.DataFrame({
        'size': sizes,
        'count': counts
    })

    df.to_csv(output_path, index=False)

    return df


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print("Usage: python reference_implementation.py <input_mask.npy> <output.csv>")
        sys.exit(1)

    mask_path = sys.argv[1]
    output_path = sys.argv[2]

    compute_cloud_size_distribution(mask_path, output_path)
    print(f"Size distribution saved to {output_path}")
