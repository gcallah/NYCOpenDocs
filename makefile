# Need to export as ENV var
export TEMPLATE_DIR = templates
PYTHONFILES = $(shell find ../NYCOpenRecords -name '*.py')
PTML_DIR = html_src
UTILS_DIR = utils

INCS = $(TEMPLATE_DIR)/navbar.txt $(TEMPLATE_DIR)/head.txt

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///')

%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 $(UTILS_DIR)/html_checker.py $< 
	# python3 $(UTILS_DIR)/url_checker.py $<
	# https://gcallah.github.io/NYCOpenDocs
	$(UTILS_DIR)/html_include.awk <$< >$@
	git add $@

website: $(INCS) $(HTMLFILES)
	-git commit -a 
	git pull origin master
	git push origin master

local: $(HTMLFILES)

clean:
	touch $(PTML_DIR)/*.ptml; make local

menu: $(PYTHONFILES)
	echo $(PYTHONFILES) > menu.txt
