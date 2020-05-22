import statictypes
import unittest


class TestStaticTypes(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()
