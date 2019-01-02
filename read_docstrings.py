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
        # if found a function or class 
        if "def " in line or "class" in line:
            if "class" in line:
                    line = line.strip()
            if len(output) != 0:
                output += "\n"
            output += line
        # check for docstrings 
        elif "'''" in line or '"""' in line:
            quotes_occurrence = 0
            if line.count("'''") != 0:
                quotes_occurrence = line.count("'''")
            else:
                quotes_occurrence = line.count('"""')
            # check if start and end of docstring are on the same line
            # if so, add the line
            # otherwise have a boolean to determine which lines 
            # are part of the docstring
            if quotes_occurrence == 2:
                output += line
            else:
                if not docstring:
                    docstring = True
                else:
                    output += line
                    docstring = False
        if docstring:
            output += line
    program_file.close()
    # write the output to templates/name of file 
    write_filenm = file_name.split("NYCOpenRecords/")[-1]
    write_filenm = "_".join(write_filenm.split("/"))
    write_filenm += ".txt"
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
