import unittest
import subprocess

def run_test(test_case: unittest.TestCase, file_name: str):
    source_file = f"{file_name}.ppp"
    output_file = f"{file_name}.out"
    result = subprocess.run(["python3.12", "src/main.py", source_file], stdout=subprocess.PIPE)
    file = open(output_file, 'r')
    expected_output = file.read()
    file.close()
    test_case.assertEqual(str(result.stdout, encoding='utf-8'), expected_output)

class TestStringMethods(unittest.TestCase):
    def test_hello_world(self):
        run_test(self, "tests/hello_world")

if __name__ == '__main__':
    unittest.main()
