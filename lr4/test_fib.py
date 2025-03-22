from gen_fib import my_genn
import unittest

class TestFib(unittest.TestCase):
    def test_1 (self):
        gen = my_genn()
        result = gen.send(5)
        self.assertEqual(result, [0, 1, 1, 2, 3])

    def  test2(self):
        gen = my_genn()
        result = gen.send(10)
        self.assertEqual(result, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])

    def  test3(self):
        gen = my_genn()
        result = gen.send(0)
        self.assertEqual(result, [])       

    def  test3(self):
        gen = my_genn()
        result = gen.send(-20)
        self.assertEqual(result, []) 


if __name__== "__main__":
    unittest.main()

