import sys

LEVEL = 0
TITLE = 1
URL = 2
SHORT_TITLE = 3
GLYPHICON = 4
LINK_INSERT = 5
DOC_TXT = 6
HW_TXT = 7
LINT_TXT = 8

EXTENSIONS = []
ext_file = open(sys.argv[1], "r")
for ext_line in ext_file:
    EXTENSIONS.append(ext_line.strip("\n"))
CONNECTOR = "\t"

BASE_URL = "/NYCOpenDocs/"
HTML_URL = BASE_URL + "html/"
SOURCE_URL = "https://github.com/CityOfNewYork/NYCOpenRecords/blob/master/"
TEMPLATE_DIR = "templates/"


def read_file_names():
    names = open("templates/menu_input.txt", "r")
    file_names = names.read()
    file_names = file_names.split("../NYCOpenRecords/")
    file_names.sort()
    # for each name, split on the /
    for i in range(len(file_names)):
        file_names[i] = file_names[i].strip("\n")
        if "/" in file_names[i]:
            file_names[i] = file_names[i].split("/")
        else:
            file_names[i] = [file_names[i]]
    names.close()
    # getting rid of the first one which is an empty string
    file_names.pop(0)
    return file_names


def check_directories(lst1, lst2):
    # check if the two directories of a file path are the same
    # return the index where the file paths are different
    # which is where the path leads to a different directory
    # if empty list, return 0
    if lst1 == []:
        return 0
    # otherwise, loop up until the last index, which is a file name
    for i in range(min(len(lst1), len(lst2)) - 1):
        if lst1[i] != lst2[i]:
            return i
    # return index of the minimum length - 1 between two lists
    return min(len(lst1), len(lst2)) - 1


def get_extension(file_nm):
    '''
    Returns the extension given the file name
    Example:
        file_nm = "read_docstrings.py"
        Returns "py"
    '''
    return file_nm.split(".")[-1]


def csv_row_file(file_nm, level_num, title, url_txt_nm):
    '''
    Returns a list of the entries for the CSV pertaining to a file name
    '''
    output_lst = ["", "", "", "", "", "", "", "", ""]
    output_lst[LEVEL] = str(level_num)
    output_lst[TITLE] = title
    output_lst[URL] = HTML_URL + url_txt_nm.strip(".") + ".html"
    output_lst[LINK_INSERT] = SOURCE_URL + file_nm
    if get_extension(file_nm) in EXTENSIONS:
        output_lst[DOC_TXT] = TEMPLATE_DIR + url_txt_nm + "_ex.txt"
        output_lst[HW_TXT] = TEMPLATE_DIR + url_txt_nm + "_hw.txt"
    if get_extension(file_nm) == "py" or get_extension(file_nm) == "js":
        output_lst[LINT_TXT] = TEMPLATE_DIR + url_txt_nm + "_lint.txt"
    return CONNECTOR.join(output_lst).strip(CONNECTOR)


def csv_row_dir(level_num, title, url):
    '''
    Returns a list of the entries for the CSV pertaining to a
    directory name
    '''
    output_lst = ["", "", ""]
    output_lst[LEVEL] = str(level_num)
    output_lst[TITLE] = title
    output_lst[URL] = HTML_URL + url.strip(".") + ".html"
    return CONNECTOR.join(output_lst).strip(CONNECTOR)


def navbar_entry(level, title):
    '''
    If a directory is encountered in creating the CSV,
    create an entry in the CSV for the navbar
    '''
    output_lst = [str(level), title]
    return CONNECTOR.join(output_lst).strip(CONNECTOR)


def create_header_row():
    '''
    Creates the header and the home rows (first two rows) for the CSV file
    '''
    header = CONNECTOR.join(["0", "NYCOpenDocs", "", "NYCDocs"])
    home = ["1", "Home", BASE_URL + "index.html", "", "glyphicon-home"]
    home = CONNECTOR.join(home)
    return [header, home]


def create_csv():
    file_names = read_file_names()
    # make a list of strings for the output
    # each string has fields filled in
    output = create_header_row()
    current_dir = []
    # current types of files with docstrings extracted
    # loop through the file names
    for file in file_names:
        # check the directory paths
        # returned from check directories
        index_dif = check_directories(current_dir, file)
        while index_dif < len(file):
            # if list entry is a file name
            if index_dif == len(file) - 1:
                level = index_dif + 1
                title = file[index_dif]
                file_nm = "/".join(file)
                url_txt_nm = "_".join(file)
                output.append(csv_row_file(file_nm, level, title, url_txt_nm))
            # if list entry is a directory name
            else:
                # create the navbar entry
                nav_level = index_dif + 1
                nav_title = file[index_dif]
                output.append(navbar_entry(nav_level, nav_title))

                level = index_dif + 2
                title = "About the directory '" + file[index_dif] + "'"
                url = "_".join(file[:index_dif + 1]) + "_" + file[index_dif]
                output.append(csv_row_dir(level, title, url))
            index_dif += 1
        current_dir = file
    # construct the output string by joining on new lines
    output = "\n".join(output)
    sys.stdout.write(output)


def main():
    create_csv()


main()
