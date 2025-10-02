# Research Bench

Benchmark suite for evaluating AI coding agents on atmospheric science research tasks.

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

## Docker Setup

Build Docker image from Claude Code devcontainer (includes firewall that allows only api.anthropic.com):
```bash
git clone https://github.com/anthropics/claude-code.git
cd claude-code/.devcontainer
docker build -t claude-code .
cd ../../
```

## Running Tests

### cloud_size_distribution

```bash
# test
docker run -it --rm --cap-add=NET_ADMIN --cap-add=NET_RAW -v $(pwd)/cloud_size_distribution/test:/workspace:rw -w /workspace -e ANTHROPIC_API_KEY claude-code claude --dangerously-skip-permissions "read prompt.txt"

# test_hint
docker run -it --rm --cap-add=NET_ADMIN --cap-add=NET_RAW -v $(pwd)/cloud_size_distribution/test_hint:/workspace:rw -w /workspace -e ANTHROPIC_API_KEY claude-code claude --dangerously-skip-permissions "read prompt.txt"

# test_sparse
docker run -it --rm --cap-add=NET_ADMIN --cap-add=NET_RAW -v $(pwd)/cloud_size_distribution/test_sparse:/workspace:rw -w /workspace -e ANTHROPIC_API_KEY claude-code claude --dangerously-skip-permissions "read prompt.txt"

# test_sparse_hint
docker run -it --rm --cap-add=NET_ADMIN --cap-add=NET_RAW -v $(pwd)/cloud_size_distribution/test_sparse_hint:/workspace:rw -w /workspace -e ANTHROPIC_API_KEY claude-code claude --dangerously-skip-permissions "read prompt.txt"
```

**Check solution:**
```bash
python cloud_size_distribution/check_solution.py cloud_size_distribution/test/solution.csv cloud_size_distribution/answer_key.csv
```

## Tasks

- **cloud_size_distribution**: Compute power-law exponents for cloud area distributions
