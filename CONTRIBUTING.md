# 🤝 Contributing to PulmoAI

Thank you for considering contributing to PulmoAI! This document provides guidelines and instructions for contributing.

---

##  Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- ✅ Be respectful and professional
- ✅ Welcome diverse perspectives
- ✅ Focus on constructive feedback
- ✅ Report harassment or violations to the maintainers

---

## Reporting Bugs

### Before Submitting a Bug Report

- Check existing [Issues](../../issues) to avoid duplicates
- Verify the bug hasn't been fixed in the latest version
- Gather information about your environment

### How to Submit a Bug Report

1. Go to [Issues](../../issues)
2. Click **"New Issue"**
3. Use this template:

```markdown
**Describe the bug:**
Clear description of what the bug is.

**To Reproduce:**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior:**
What you expected to happen.

**Screenshots:**
If applicable, add screenshots.

**Environment:**
- OS: [Windows/macOS/Linux]
- Python version: [3.9/3.10/3.11]
- TensorFlow version: [2.13.0]
- Reproduction rate: [Always/Sometimes/Rarely]

**Additional context:**
Any other context about the problem.
```

---

##  Suggesting Enhancements

### Before Submitting an Enhancement

- Check existing [Discussions](../../discussions)
- Ensure it aligns with project goals
- Consider the implementation complexity

### How to Submit an Enhancement

1. Go to [Discussions](../../discussions)
2. Click **"New Discussion"** → Category: "Ideas"
3. Describe your feature idea:
   - What problem does it solve?
   - How would it work?
   - Examples of usage

---

##  Setting Up Development Environment

### 1. Fork the Repository

1. Click **Fork** button on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR-USERNAME/PulmoAI.git
cd PulmoAI
```

### 2. Create Development Branch

```bash
# Create feature branch from main
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
```
feature/description          # New feature
bugfix/description          # Bug fix
docs/description            # Documentation
refactor/description        # Code refactor
test/description            # Tests
```

### 3. Install Development Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install with dev extras
pip install -r requirements_pinned.txt
pip install pytest pytest-cov black flake8 mypy  # Dev tools

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### 4. Make Your Changes

Edit files as needed. Remember:
- ✅ Keep changes focused and small
- ✅ Follow the code style (see below)
- ✅ Add tests for new features
- ✅ Update documentation

---

##  Code Style Guidelines

### Python Code Style

We follow **PEP 8** with these tools:

```bash
# Format code with Black
black .

# Check style with Flake8
flake8 .

# Type checking with MyPy
mypy .
```

### Naming Conventions

```python
# Constants: UPPER_CASE
MAX_UPLOAD_SIZE = 16777216
MODEL_PATH = "ai_model/model.h5"

# Functions: snake_case
def predict_image(image_path):
    pass

# Classes: PascalCase
class ImageAnalyzer:
    pass

# Private functions: _leading_underscore
def _process_image(image):
    pass
```

### Code Quality

- Keep functions **small and focused** (< 50 lines)
- Write **clear comments** for complex logic
- Use **type hints** for function arguments
- Avoid **deeply nested** code (max 3 levels)

### Example of Good Code

```python
from typing import Tuple
import cv2
import numpy as np

def preprocess_image(image_path: str, target_size: Tuple[int, int]) -> np.ndarray:
    """
    Preprocess X-ray image for model prediction.
    
    Args:
        image_path: Path to X-ray image file
        target_size: Target dimensions (height, width)
        
    Returns:
        Preprocessed image array normalized to [0, 1]
        
    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If image cannot be loaded
    """
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    # Resize with aspect ratio preservation
    image = cv2.resize(image, target_size)
    
    # Normalize to [0, 1]
    image = image.astype('float32') / 255.0
    
    return image
```

---

##  Commit Messages

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Build, dependencies, etc.

### Examples

```bash
# Good commit messages
git commit -m "feat(gradcam): improve heatmap visualization blending"
git commit -m "fix(auth): handle jwt token expiration correctly"
git commit -m "docs(readme): add installation instructions"
git commit -m "test(model): add unit tests for preprocessing"
```

---

##  Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_model.py

# Run specific test
pytest tests/test_model.py::test_predict_image
```

### Writing Tests

Create tests in `tests/` directory:

```python
# tests/test_model.py
import pytest
from services.model_service import predict

def test_predict_valid_image():
    """Test prediction with valid image."""
    result = predict("test_data/sample.jpg")
    assert result is not None
    assert 'prediction' in result
    assert result['confidence'] >= 0

def test_predict_invalid_image():
    """Test prediction with invalid image."""
    with pytest.raises(FileNotFoundError):
        predict("nonexistent.jpg")
```

---

##  Documentation

### Update Docs When You

- Add new features
- Change existing functionality
- Fix bugs (especially if user-facing)

### Documentation Files

- **README.md** - Overview & quick start
- **docs/API.md** - API endpoints
- **docs/DEVELOPMENT.md** - Development guide
- **docs/DEPLOYMENT.md** - Deployment instructions
- **Inline comments** - Complex code explanations

---

##  Submitting Changes

### 1. Commit Your Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat(gradcam): improve visualization quality"

# Push to your fork
git push origin feature/your-feature-name
```

### 2. Create Pull Request

1. Go to [Pull Requests](../../pulls)
2. Click **"New Pull Request"**
3. Select `your-fork:feature-branch` → `main:main`
4. Fill in PR template:

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Closes #(issue number)

## Testing
- [ ] I have tested locally
- [ ] Tests pass (pytest)
- [ ] Code passes linting (flake8)

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
```

### 3. Code Review

- Respond to review comments
- Make requested changes
- Push updates (they auto-update the PR)

### 4. Merge

Once approved, maintainers will merge your PR! 

---

##  Development Workflow Example

```bash
# 1. Create feature branch
git checkout -b feature/add-pdf-export

# 2. Make changes
# ... edit files ...

# 3. Run tests
pytest

# 4. Format code
black .
flake8 .

# 5. Commit
git add .
git commit -m "feat(report): add PDF export functionality"

# 6. Push
git push origin feature/add-pdf-export

# 7. Create Pull Request on GitHub
# ... fill in PR template ...

# 8. Wait for review & approval
# ... address feedback ...

# 9. Merge (maintainer does this)
# ... celebrate! ...
```

---

##  Do NOT

- ❌ Commit sensitive information (passwords, API keys)
- ❌ Push directly to main branch
- ❌ Submit PRs without tests
- ❌ Ignore the Code of Conduct
- ❌ Make massive commits (split them up)
- ❌ Use `--force` on shared branches

---

## ✅ Do

- ✅ Write clear commit messages
- ✅ Keep PRs focused (one feature per PR)
- ✅ Test your changes locally
- ✅ Update documentation
- ✅ Follow code style guidelines
- ✅ Be responsive to feedback

---

##  Learning Resources

- **Git Workflow**: https://guides.github.com/introduction/flow/
- **PEP 8 Style Guide**: https://pep8.org/
- **Black Code Formatter**: https://black.readthedocs.io/
- **Pytest Documentation**: https://docs.pytest.org/

---

##  Getting Help

- **Questions?** Ask in email : erramyabdessamad2@gamil.com
- 

---

##  Recognition

Contributors will be:
- ✅ Listed in [CHANGELOG.md](../CHANGELOG.md)
- ✅ Credited in project
- ✅ Recognized in README

---

##  Additional Guidelines

### For Documentation Contributors

- Use clear, simple language
- Include examples and code snippets
- Add screenshots where helpful
- Keep docs up-to-date with code

### For Bug Fix Contributors

- Add test case that reproduces the bug
- Explain why the fix works
- Reference the original issue

### For Feature Contributors

- Discuss design in issue first
- Include tests covering edge cases
- Update relevant documentation
- Consider performance impact

---



---
##  Questions?

- Check [CONTRIBUTING.md](./CONTRIBUTING.md) (this file)
- Read [docs/FAQ.md](../docs/FAQ.md)
- Open a [Discussion](../../discussions)
- Email: erramyabdessamad2@gmail.com

---

**Thank you for contributing to PulmoAI!** ❤️

Together we're making medical AI accessible to healthcare professionals worldwide.