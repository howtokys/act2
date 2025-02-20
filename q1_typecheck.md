## Type Checking with `mypy` 

### Overview

`mypy` is a static type checker for Python that helps ensure the code is type-safe. It uses type hints to check for type errors without running the code, making it an essential tool for developers.

### Type Hints

Type hints are annotations that specify the expected types of variables, function arguments, and return values. They enhance code clarity and assist tools like `mypy` in performing type checks effectively.

### Example

```python
def welcome_user(user: str) -> str:
    return f"Welcome to the platform, {user}!"
```

### Running `mypy`

To execute `mypy`, use the following command:

```sh
mypy your_script.py
```