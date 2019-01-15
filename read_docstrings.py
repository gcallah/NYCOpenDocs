def read_file_names():
    names = open("templates/menu_input.txt", "r")
    # when echo is called, all the names were concatenated into
    # a single string
    file_names = names.read().split(" ")
    file_names.sort()
    for i in range(len(file_names)):
        file_names[i] = file_names[i].strip()
    names.close()
    return file_names


def read_docstrings(file_name):
    output = ""
    program_file = open(file_name, "r")
    docstring = False
    for line in program_file:
        spaces = 0
        # if found a function or class 
        if "def " in line or "class" in line:
            if "class" in line:
                spaces = line.find("class")
            else:
                spaces = line.find("def")
            output += (spaces // 4) * "&emsp;" + line + "<br>"
        # check for docstrings 
        elif "'''" in line or '"""' in line:
            quotes_occurrence = 0
            if line.count("'''") != 0:
                quotes_occurrence = line.count("'''")
                spaces = line.find("'''")
            else:
                quotes_occurrence = line.count('"""')
                spaces = line.find('"""')
            # check if start and end of docstring are on the same line
            # if so, add the line
            # otherwise have a boolean to determine which lines 
            # are part of the docstring
            if quotes_occurrence == 2:
                output += (spaces // 4) * "&emsp;" + line + "<br>"
            else:
                if not docstring:
                    docstring = True
                else:
                    output += (spaces // 4) * "&emsp;" + line + "<br>"
                    docstring = False
        if docstring:
            with_space = len(line)
            without_space = len(line.strip(" "))
            spaces = with_space - without_space
            output += (spaces // 4) * "&emsp;" + line + "<br>"
    program_file.close()
    # write the output to templates/name of file 
    write_filenm = file_name.split("NYCOpenRecords/")[-1]
    write_filenm = "_".join(write_filenm.split("/"))
    write_filenm += "_ex.txt"
    output_file = open("templates/" + write_filenm, "w")
    output_file.write(output)
    output_file.close()


def read_docs():
    '''
    Read documention of python files for now 
    '''
    file_names = read_file_names()
    for filenm in file_names:
        if ".py" in filenm:
            read_docstrings(filenm)


def main():
    read_docs()


main()
