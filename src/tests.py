import unittest
import subprocess

class TestStringMethods(unittest.TestCase):
    def test_hello_world(self):
        result = subprocess.run(["python3.12", "src/main.py", "tests/hello_world.ppp"], stdout=subprocess.PIPE)
        file = open("tests/hello_world.out", 'r')
        expected_output = file.read()
        self.assertEqual(str(result.stdout, encoding='utf-8'), expected_output)

if __name__ == '__main__':
    unittest.main()
