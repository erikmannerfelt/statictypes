import statictypes
import unittest
from typing import Optional, Union, List, Tuple, Dict
import numpy as np

class MyClass:
    """Example class to use in tests."""
    @statictypes.enforce
    def __init__(self, arg1: str) -> None:
        self.arg1 = arg1

    def update(self):
        self.arg1 += ". Addition"


class TestStaticTypes(unittest.TestCase):
    """Unit tests."""

    def test_enforce(self):

        @statictypes.enforce
        def myfunc(text: str, num: int) -> str:
            """Test the type enforcing."""
            return text + str(num)

        self.assertEqual(myfunc("hello", 3), "hello3")
        self.assertEqual(myfunc("hello", 10000), "hello10000")

        with self.assertRaises(statictypes.StaticTypeError):
            myfunc("hello", "3")

  
    def test_convert(self):
        @statictypes.convert
        def myfunc2(text: str, num: int, extra: float = 3.4) -> str:
            return text + str(num) + str(extra)

        self.assertEqual(myfunc2("hello", "4"), "hello43.4")

    def test_typing_optional_and_union(self):

        @statictypes.enforce
        def myfunc3(text: str, num: Optional[float]) -> str:
            output = text
            if num is not None:
                output += str(num)
            return output
        
        self.assertEqual(myfunc3("hello", None), "hello")

        @statictypes.enforce
        def myfunc4(text: str, num: Union[float, int, None]) -> str:
            output = text
            if num is not None:
                output += str(num)
            return output

        self.assertEqual(myfunc4("hello", 1.1), "hello1.1")

    def test_typing_list(self):

        @statictypes.enforce
        def myfunc5(text: str, nums: List[int]) -> str:
            return text + " " + " ".join([str(num) for num in nums])

        self.assertEqual(myfunc5("hello", [1, 2, 3]), "hello 1 2 3")

    def test_typing_tuple(self):

        @statictypes.enforce
        def myfunc6(text: str, nums: Tuple[int, float, str]) -> str:
            return text + " " + " ".join([str(num) for num in nums])

        self.assertEqual(myfunc6("hello", (1, 2.2, "3")), "hello 1 2.2 3")

    def test_typing_dict(self):

        @statictypes.enforce
        def myfunc7(text: str, nums: Dict[str, int]) -> str:
            return text + " " + " ".join(str(nums[key]) for key in ["one", "two", "three"])
        
        self.assertEqual(myfunc7("hello", {"one": 5, "two": 2, "three": 3}), "hello 5 2 3")

    def test_numpy_array(self):

        @statictypes.enforce
        def myfunc(nums: np.ndarray) -> str:
            return " ".join([str(num) for num in nums])

        self.assertEqual(myfunc(np.array([1, 2, 3])), "1 2 3")

    def test_class_methods(self):
        """Check that 'self' is not type-checked."""
        myclass = MyClass("hello")
        myclass.update()


if __name__ == "__main__":
    unittest.main()
