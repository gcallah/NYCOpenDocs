# NYC Open Records Documentation

This is a buildable documentation system for the NYC Open Records project.
It reads the structure of that projects GitHub repo
[https://github.com/CityOfNewYork/NYCOpenRecords] to create a menu and 
file skeleton. The skeleton is then filled in by:

1. Automatically extracting doc strings from source code files.
2. Running lint tools against python and javascript files to get code style
   reports.
3. Creating handwritten documents and code reviews.

The skeleton has reserved places for each of the above three sources of text,
and there are scripts included to put them in the right place.

The entire build of the documentation system, from reading the GitHub repo to
the final HTML pages, is controlled by a makefile
[https://github.com/gcallah/NYCOpenDocs/blob/master/makefile]
in the top-level directory. `make all` we build the system from the bottom up.
The build hierarchy is documented here:
[https://github.com/gcallah/NYCOpenDocs/blob/master/NYCOpenDocsBuild.png]

The documentation is currently hosted here:
[https://gcallah.github.io/NYCOpenDocs/]
