import sys


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


def create_csv():
    # menu_file = open("html_menu.txt", "w")
    file_names = read_file_names()
    output = str(0) + "\tNYCOpenDocs\t\tNYCDocs\n"
    output += str(1) + "\tHome\tindex.html\t\tglyphicon-home\n"
    current_dir = []
    source_code = "https://github.com/CityOfNewYork/NYCOpenRecords/blob/master/"
    # loop through the file names
    for file in file_names:
        # if file is a string, it's not in a sub directory
        if isinstance(file, str):
            output += str(1) + "\t" + file + "\t" + file.strip(".") + ".html\t\t\t" + source_code + file + "\n"
            current_dir = []
        # otherwise, check the directory paths
        # number of tabs = the index we start at that was
        # returned from check directories
        else:
            index_dif = check_directories(current_dir, file)
            while index_dif < len(file):
                output += str(index_dif + 1) + "\t" + file[index_dif]
                if index_dif == len(file) - 1:
                    output += "\t" + "_".join(file) + ".html"
                    output += "\t\t\t" + source_code + "/".join(file)
                else:
                    output += ("\n" + str(index_dif + 2) +
                               "\tAbout the directory '" + file[index_dif] + "'" +
                               "\t" + "_".join(file[:index_dif + 1]) + "_" + file[index_dif] +
                               ".html")
                output += "\n"
                index_dif += 1
            current_dir = file
    # menu_file.write(output)
    # menu_file.close()
    sys.stdout.write(output)


def main():
    create_csv()


main()
