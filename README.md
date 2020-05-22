# statictypes

```statictypes``` helps your Python functions do exactly what you asked them to do, and not anything else.
This package delivers three simple decorators:

* ```@statictypes.enforce```: Raise an error if the incorrect argument or return type is given.
* ```@statictypes.warn```: Give a warning if the incorrect argument  or return type is given.
* ```@statictypes.convert```: Try to convert into the given argument type, or return an error.

## Example 1

Let's define a simple function, and enforce Python's type annotations.

```python3
import statictypes

@statictypes.enforce
def myfunc(text: str, number: int) -> str:
    return text + " " + str(number)

myfunc("my number is", 1)  # This works as intended
myfunc("my number is", 1.1)  # This raises an error
```

Calling ```myfunc("my number is", 1)``` is valid, but ```myfunc("my number is", 1.1)``` results in:

```statictypes.StaticTypeError: Argument 'number' got incorrect type <class'float'>, expected <class'int'>.```

## Example 2

Let's instead choose to convert the arguments to the given type annotations.

```python3
import statictypes

@statictypes.convert
def myfunc(text: str, number: int) -> str:
    return text + " " + str(number)

myfunc("my number is", 1)  # This works as intended
myfunc("my number is", 1.1)  # This gives the same output as above
```

This time, both ```myfunc("my number is", 1)``` and ```myfunc("my number is", 1.1)``` is valid.
Note, however, that both expressions give the output ```"my number is 1"```, since ```number``` is in this case always converted to an integer.

## Limitations

1. ```@statictypes.convert``` only works for simple types from where a constructor method can be called, e.g. ```str```, ```int```.
The decorator does not work on e.g. ```List[float] -> List[int]``` since the following incorrect conversion is attempted: ```List[int](list_of_floats)```.
2. Only the builtin generic types ```Any, Union, Optional, Dict, List``` and ```Tuple``` are currently supported.
3. When using ```@statictypes.convert```, if a ```list``` is given to a function expecting a ```numpy.ndarray``` , an empty ```numpy.ndarray``` is returned with the shape of the ```list```.
This is because the ```numpy.ndarray``` has ```shape``` as its first positional argument, leading to a working but arguably unexpected result.

## Requirements

* Python 3.6 or above.

## Installation
```bash
pip install statictypes
```