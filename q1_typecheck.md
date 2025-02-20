## Type Checking with `mypy`

### Overview

`mypy` is a static type checker for Python that helps ensure the code is type-safe. It uses type hints to check for type errors without running the code.

### Type Hints

Type hints are annotations that specify the expected types of variables, function arguments, and return values. They improve code readability and help tools like `mypy` perform type checking.

### Example

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

### Running `mypy`

The following command is used to run `mypy`:

```sh
mypy your_script.py
```

### Screenshot

![mypy example](mypy.png)