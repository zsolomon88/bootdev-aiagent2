from functions.get_files_info import get_files_info

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

if __name__ == '__main__':
    test_current_directory()
    test_pkg_directory()
    test_bin_directory()
    test_parent_directory()