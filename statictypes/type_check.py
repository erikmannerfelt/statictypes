"""Decorators for static type checking, converting and enforcing."""

import inspect
import warnings
import itertools
import typing


class StaticTypeError(Exception):
    """Error for an incorrect given function argument or keyword argument type."""

    error_kind = "exception"

    def __init__(self, *args):
        """Construct exception instance with an optional message."""
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        """Return string representation of exception."""
        if self.message:
            return "{0} ".format(self.message)

        return "MyCustomError has been raised"


class StaticTypeWarning(Warning):
    """Error for an incorrect given function argument or keyword argument type."""

    error_kind = "warning"

    def __init__(self, *args):
        """Construct exception instance with an optional message."""
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        """Return string representation of exception."""
        if self.message:
            return "{0} ".format(self.message)

        return "MyCustomError has been raised"


def warn_or_raise(message, error_type):
    """Warn or raise an exception with a message based on the given error type."""
    if error_type.error_kind == "warning":
        warnings.warn(message, error_type)
    else:
        raise error_type(message)


def _type_checker(func, error_type):
    """Check the types of each argument and keyword argument, and produce a fitting response."""
    # Get function metadata
    meta = inspect.getfullargspec(func)

    # Collect arg and kwarg names to check if annotations are set.
    arg_names = meta.args.copy()
    if arg_names is None and meta.varargs is None:
        return func
    if meta.varargs is not None:
        arg_names.append(meta.varargs)

    # Check which annotations are missing
    missing_annotations = []
    for arg_name in arg_names:
        if meta.annotations.get(arg_name) is None:
            missing_annotations.append(arg_name)
    if missing_annotations != []:
        warn_or_raise(f"Missing type for argument{'s' if len(missing_annotations) > 1 else ''}: {', '.join(missing_annotations)}", error_type)

    # Check if return annotation exist
    if "return" not in meta.annotations.keys():
        warn_or_raise("Missing function return type.", error_type)

    def wrapper(*args, **kwargs):
        """Wrap the outside function in type checking function."""
        # Check types for all arguments
        for arg_name, arg in itertools.chain(zip(meta.args, args), kwargs.items()):
            expected_type = meta.annotations[arg_name]
            if is_type(arg, expected_type):
                continue

            warn_or_raise(f"Argument '{arg_name}' got wrong type. Expected {expected_type}, got {type(arg)}", error_type)

        return func(*args, **kwargs)

    return wrapper


def is_type(input_object, expected_type) -> bool:
    """
    Check if an object corresponds to a given type.

    Works similarly to isinstance but also works on select 'typing' types.
    """
    try:
        module = expected_type.__module__
    except AttributeError:
        module = "default"

    if module == "typing":

        if isinstance(input_object, dict):
            right_types = []
            for key, value in input_object.items():
                right_types.append(
                    all([
                        isinstance(key, expected_type.__args__[0]),
                        isinstance(value, expected_type.__args__[1])
                    ])
                )
            return all(right_types)

        if isinstance(input_object, (list, tuple)):
            accepted_types = expected_type.__args__
            if not isinstance(accepted_types, list):
                accepted_types = [accepted_types] * len(input_object)

            right_types = [is_type(element, accepted_types[i]) for i, element in enumerate(input_object)]

            return all(right_types)

        if expected_type.__origin__ == typing.Union:
            for accepted_type in expected_type.__args__:
                if isinstance(input_object, accepted_type):
                    return True

        return False
    if input_object is None:
        if expected_type is None:
            return True
        return False
    return isinstance(input_object, expected_type)


def enforce(func):
    """
    Enforce the type annotations of a function.

    Raises a StaticTypeError if annotations are not correct.
    """
    return _type_checker(func, StaticTypeError)


def warn(func):
    """
    Warn about unmet type annotation requirements of a function.

    Gives a StaticTypeWarning if annotations are not correct.
    """
    return _type_checker(func, StaticTypeWarning)


def convert(func):
    """
    Try to convert given arguments and keyword arguments to the annotated type.

    Raises a StaticTypeError if this is not possible.
    """
    # Get function metadata
    meta = inspect.getfullargspec(func)

    def wrapper(*args, **kwargs):
        """Wrap the outside function in type converting function."""
        # Convert all arguments and keyword arguments to the right type.
        # The ones with a correct type to begin with are left unchanged.
        new_args = []
        for arg_name, arg in zip(meta.args, args):
            if arg_name in meta.annotations.keys():
                if is_type(arg, meta.annotations[arg_name]):
                    new_args.append(arg)
                    continue
                try:
                    new_args.append(meta.annotations[arg_name](arg))
                except ValueError:
                    raise StaticTypeError(f"Argument '{arg_name}' got inconvertible type. Expected {meta.annotations[arg_name]}, recieved {type(arg)}.")
            else:
                new_args.append(arg)

        new_kwargs = {}
        for kwarg_name, kwarg in kwargs.items():
            if kwarg_name in meta.annotations.keys():
                if is_type(kwarg, meta.annotations[kwarg_name]):
                    new_kwargs[kwarg_name] = kwarg
                    continue
                try:
                    new_kwargs[kwarg_name] = meta.annotations[kwarg_name](kwarg)
                except ValueError:
                    raise StaticTypeError(f"Argument '{kwarg_name}' got inconvertible type. Expected {meta.annotations[kwarg_name]}, recieved {type(kwarg)}.")
            else:
                new_kwargs[kwarg_name] = kwarg

        return func(*new_args, **new_kwargs)

    return wrapper
