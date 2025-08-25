from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

def test_current_directory():
    result = "Result for current directory:\n"
    result += get_files_info("calculator", ".")
    print(result)

def test_pkg_directory():
    result = "Result for 'pkg' directory:\n"
    result += get_files_info("calculator", "pkg")
    print(result)

def test_bin_directory():
    result = "Result for 'bin' directory:\n"
    result += get_files_info("calculator", "bin")
    print(result)

def test_parent_directory():
    result = "Result for parent directory:\n"
    result += get_files_info("calculator", "../")
    print(result)

def test_lorem_file():
    result = "Result for 'lorem.txt' file:\n"
    result += get_file_content("calculator", "lorem.txt")
    print(result)

def test_main_file():
    result = "Result for 'main.py' file:\n"
    result += get_file_content("calculator", "main.py")
    print(result)

def test_calculator_file():
    result = "Result for 'calculator.py' file:\n"
    result += get_file_content("calculator", "pkg/calculator.py")
    print(result)

def test_cat_file():
    result = "Result for '/bin/cat' file:\n"
    result += get_file_content("calculator", "/bin/cat")
    print(result)

def test_missing_file():
    result = "Result for missing file:\n"
    result += get_file_content("calculator", "missing.txt")
    print(result)

def test_write_lorem():
    content = "wait, this isn't lorem ipsum"
    result = "Result for writing 'lorem.txt' file:\n"
    result += write_file("calculator", "lorem.txt", content)
    print(result)
    
def test_write_more_lorem():
    content = "lorem ipsum dolor sit amet"
    result = "Result for writing 'morelorem.txt' file:\n"
    result += write_file("calculator", "pkg/morelorem.txt", content)
    print(result)

def test_write_to_outside_directory():
    content = "this should not be allowed"
    result = "Result for writing to outside directory:\n"
    result += write_file("calculator", "/tmp/temp.txt", content)
    print(result)

def test_run_python_main():
    result = "Result for running 'main.py':\n"
    result += run_python_file("calculator", "main.py")
    print(result)

def test_run_python_calculator():
    result = "Result for running 'pkg/calculator.py':\n"
    result += run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)

def test_run_python_tests():
    result = "Result for running 'tests.py':\n"
    result += run_python_file("calculator", "tests.py")
    print(result)

def test_run_python_outside_directory():
    result = "Result for running outside directory:\n"
    result += run_python_file("calculator", "../main.py")
    print(result)

def test_run_python_nonexistent():
    result = "Result for running nonexistent file:\n"
    result += run_python_file("calculator", "nonexistent.py")
    print(result)

if __name__ == '__main__':
    test_run_python_main()
    test_run_python_calculator()
    test_run_python_tests()
    test_run_python_outside_directory()
    test_run_python_nonexistent()