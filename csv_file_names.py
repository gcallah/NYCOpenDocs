import sys

LEVEL = 0
TITLE = 1
URL = 2
SHORT_TITLE = 3
GLYPHICON = 4
LINK_INSERT = 5
DOC_TXT = 6


def read_file_names():
    names = open("templates/menu_input.txt", "r")
    file_names = names.read()
    # when echo is called, all the names were concatenated into
    # a single string
    file_names = file_names.split("../NYCOpenRecords/")
    file_names.sort()
    # for each name, split on the /
    # if no slash, keep it as a string
    for i in range(len(file_names)):
        file_names[i] = file_names[i].strip().strip("\n")
        if "/" in file_names[i]:
            file_names[i] = file_names[i].split("/")
    names.close()
    # getting rid of the first one which is an empty string
    file_names.pop(0)
    return file_names


def check_directories(lst1, lst2):
    # check if the two directories are the same
    # return the index where the file paths are different
    # if empty list, return 0
    if lst1 == []:
        return 0
    # otherwise, loop up until the last index, which is a py name
    for i in range(min(len(lst1), len(lst2)) - 1):
        if lst1[i] != lst2[i]:
            return i
    # return index of the minimum length - 1 between two lists
    return min(len(lst1), len(lst2)) - 1


def create_csv(connector):
    file_names = read_file_names()
    # make a list of strings for the output 
    # each string has fields filled in
    output = []
    header = ["0", "NYCOpenDocs", "", "NYCDocs"]
    header = connector.join(header)
    base_url = "/NYCOpenDocs/"
    html_url = base_url + "html/"
    home = ["1", "Home", base_url + "index.html", "", "glyphicon-home"]
    home = connector.join(home)
    output.append(header)
    output.append(home)
    current_dir = []
    source_code = "https://github.com/CityOfNewYork/NYCOpenRecords/blob/master/"
    template_dir = "templates/"
    # loop through the file names
    for file in file_names:
        output_lst = ["", "", "", "", "", "", ""]
        # if file is a string, it's not in a sub directory
        if isinstance(file, str):
            py_js_file = ".py" in file or ".js" in file
            output_lst[LEVEL] = str(1)
            output_lst[TITLE] = file
            output_lst[URL] = html_url + file.strip(".") + ".html"
            output_lst[LINK_INSERT] = source_code + file
            if py_js_file:
                output_lst[DOC_TXT] = template_dir + file.strip(".") + "_ex.txt"
            output.append(connector.join(output_lst))
            current_dir = []
        # otherwise, check the directory paths
        # number of tabs = the index we start at that was
        # returned from check directories
        else:
            py_js_file = ".py" in file[-1] or ".js" in file[-1]
            output_dir_lst = ["", "", ""]
            # have a boolean in case we are dealing with a directory
            # not a file
            out_dir = False
            index_dif = check_directories(current_dir, file)
            while index_dif < len(file):
                output_lst[LEVEL] = str(index_dif + 1)
                output_lst[TITLE] = file[index_dif]
                if index_dif == len(file) - 1:
                    output_lst[URL] = html_url + "_".join(file) + ".html"
                    output_lst[LINK_INSERT] = source_code + "/".join(file)
                    if py_js_file:
                        output_lst[DOC_TXT] = template_dir + "_".join(file) + "_ex.txt"
                else:
                    output_dir_lst[LEVEL] = str(index_dif + 2)
                    output_dir_lst[TITLE] = ("About the directory '" +
                                             file[index_dif] + "'")
                    output_dir_lst[URL] = html_url
                    output_dir_lst[URL] += ("_".join(file[:index_dif + 1]) +
                                            "_" + file[index_dif] + ".html")
                    out_dir = True
                # append the output_lst, joined by the connector
                # strip off remaining connectors in case the last fields
                # are not filled in
                output.append(connector.join(output_lst).strip(connector))
                output_lst = ["", "", "", "", "", "", ""]
                # if we filled in for a directory
                # append this after the output_lst
                if out_dir:
                    output.append(connector.join(output_dir_lst))
                    out_dir = False
                    output_dir_lst = ["", "", ""]
                index_dif += 1
            current_dir = file
    # construct the output string by joining on new lines
    output = "\n".join(output)
    sys.stdout.write(output)


def main():
    create_csv("\t")


main()
