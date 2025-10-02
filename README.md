# Research Bench

A personal benchmark suite for evaluating AI agents on atmospheric science and computational research tasks.

## Structure

Each task is organized in its own directory with the following structure:

```
task_name/
├── test/
│   ├── data/           # Input data files for the task
│   ├── solution.csv    # Expected solution/output
│   └── prompt.txt      # Task description and instructions
├── reference_implementation.py  # Reference solution
└── check_solution.py   # Validation script
```

## Tasks

### cloud_size_distribution
Analysis of cloud object size distributions from binary mask data.

## Usage

1. Read `task_name/test/prompt.txt` for task description
2. Implement solution using data in `task_name/test/data/`
3. Validate solution against expected output using `check_solution.py`
