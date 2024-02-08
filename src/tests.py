import unittest
import subprocess
from os import walk

def run_test(test_case: unittest.TestCase, file_name: str):
    source_file = f"{file_name}.ppp"
    output_file = f"{file_name}.out"
    result = subprocess.run(["python3.12", "src/main.py", source_file], stdout=subprocess.PIPE)
    file = open(output_file, 'r')
    expected_output = file.read()
    file.close()
    test_case.assertEqual(str(result.stdout, encoding='utf-8'), expected_output)

class TestStringMethods(unittest.TestCase):
    pass

if __name__ == '__main__':
    f = []
    for (dirpath, dirnames, filenames) in walk("tests/"):
        for filename in filenames:
            base_name, extension = filename.split(".")
            if extension != "ppp":
                continue
            test_name = f"{dirpath}{base_name}"
            def run_this_test(self, test_name=test_name):
                run_test(self, test_name)
            setattr(TestStringMethods, f"test_{base_name}", run_this_test)
    unittest.main()
