# Research Bench

Thomas's personal AI benchmark with difficult questions relating to his research.

## Structure

```
task_name/
├── test/                    # Main test variant
│   ├── data/               # Test data
│   ├── prompt.txt          # Task description
│   └── solution.csv        # Agent writes solution here
├── test_hint/              # With hints variant
├── test_sparse/            # Limited data variant
├── test_sparse_hint/       # Limited data + hints variant
├── answer_key.csv          # Ground truth solutions
├── check_solution.py       # Validation script
└── reference_implementation.py
```

Note: cloud_size_distribution is not a great test