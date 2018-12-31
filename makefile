PYTHONFILES = $(shell find ../NYCOpenRecords -name '*.py')

menu: $(PYTHONFILES)
	echo $(PYTHONFILES) > menu.txt

