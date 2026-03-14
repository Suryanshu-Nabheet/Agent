# Contributing to Agent 1.0

Thank you for your interest in contributing to **Agent 1.0**! As an Coding Agent project founded by **Suryanshu Nabheet**, we welcome developers from all over the world to help us build the future of open-source programming assistance.

We strive for **production-grade excellence**, and our codebase is held to the highest standards of clarity, efficiency, and robustness.

## How to Contribute

### 1. Reporting Bugs
- Use the GitHub Issue Tracker.
- Provide a clear, concise description of the bug.
- Include steps to reproduce, environment details (OS, GPU, CUDA version), and expected vs. actual behavior.

### 2. Feature Requests
- We are always looking to expand our 80+ language support and improve local execution.
- Open an issue labeled `enhancement` to discuss your ideas before implementation.

### 3. Pull Requests (PRs)
- **Branch Strategy**: Create a new branch for each feature or fix (`feature/your-feature-name` or `fix/your-fix-name`).
- **Code Style**: We follow PEP 8 for Python. Ensure your code is well-commented and clean.
- **Testing**: If you add logic, you **must** add corresponding tests in the `Evaluation/` or a new `tests/` directory.
- **Documentation**: Update any relevant `README.md` files if your changes affect the user workflow.

### 4. Development Standards
- **Local-First Focus**: Any new feature should prioritize local performance and privacy.
- **Documentation**: Every script should contain a header attributing it to Agent 1.0 and Suryanshu Nabheet.
- **Cleanliness**: Remove all redundant comments, print statements, or experimental code before submitting.

## Development Workflow
1. Fork the repository.
2. Run `./setup_agent.sh` to ensure your environment is correct.
3. Implement your changes.
4. Verify your changes using the `Evaluation/` suite (e.g., HumanEval).
5. Open a Pull Request with a detailed summary of your work.

---
*Built with passion for the global coding community by Suryanshu Nabheet.*
