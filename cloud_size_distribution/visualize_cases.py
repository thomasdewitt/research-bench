#!/usr/bin/env python3
"""
Visualize one example array from each test case with its power-law distribution.

Creates a figure showing binary arrays and their corresponding size distributions.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import objscale
import os
import glob


def visualize_cases(data_dir="test/data", answer_key_path="answer_key.csv",
                    output_path="case_visualizations.png"):
    """
    Create visualization of test cases - one array per case.

    Parameters
    ----------
    data_dir : str
        Directory containing case subdirectories
    answer_key_path : str
        Path to answer key CSV
    output_path : str
        Path to save visualization
    """
    # Load answer key
    answer_key = pd.read_csv(answer_key_path)
    num_cases = len(answer_key)

    print(f"Visualizing {num_cases} test cases...")

    # Create figure with one column: just the binary arrays
    fig, axes = plt.subplots(1, num_cases, figsize=(3 * num_cases, 3))
    if num_cases == 1:
        axes = [axes]

    for idx, row in answer_key.iterrows():
        case_name = row['case']
        is_scaling = row['is_scaling']
        exponent = row['exponent']

        case_dir = os.path.join(data_dir, case_name)

        # Load first array from this case
        first_array_path = os.path.join(case_dir, "array_000.npy")
        binary_array = np.load(first_array_path)

        print(f"  {case_name}: loaded array shape {binary_array.shape}")

        # Show binary array
        ax = axes[idx]
        ax.imshow(binary_array, cmap='gray_r', interpolation='nearest')

        # Title with case info
        if is_scaling:
            title = f"{case_name}\nτ={exponent:.3f}"
        else:
            title = f"{case_name}\nNon-scaling"

        ax.set_title(title, fontsize=10)
        ax.axis('off')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    else:
        data_dir = "test/data"

    if len(sys.argv) > 2:
        answer_key_path = sys.argv[2]
    else:
        answer_key_path = "answer_key.csv"

    if len(sys.argv) > 3:
        output_path = sys.argv[3]
    else:
        output_path = "case_visualizations.png"

    print("Creating visualization of test cases...")
    visualize_cases(data_dir, answer_key_path, output_path)
    print("✓ Done!")
