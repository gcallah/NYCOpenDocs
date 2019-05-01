# Need to export as ENV var
export TEMPLATE_DIR = templates
CODE_FILES = $(shell find ../NYCOpenRecords \( -name '*.py' -or -name '*.js' -or -name '*.yml' -or -name '*.sh' -or -name '*.html' -or -name '*.css' \))
PYTHON_LINT := $(shell find ../NYCOpenRecords -name '*.py' -exec flake8 --max-line-length 120 "{}" \;)
PTML_DIR = html_src
UTILS_DIR = utils
HTML_DIR = html
MENU_INP = $(TEMPLATE_DIR)/menu_input.txt
SITE_OUTLINE = $(TEMPLATE_DIR)/site_struct.txt
NAV_BAR = $(TEMPLATE_DIR)/navbar.txt
PTML_TEMPL = $(TEMPLATE_DIR)/template.ptml

INCS = $(NAV_BAR) $(TEMPLATE_DIR)/head.txt

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\//html\//')

$(HTML_DIR)/%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 $(UTILS_DIR)/html_checker.py $< 
	# python3 $(UTILS_DIR)/url_checker.py $<
	# https://gcallah.github.io/NYCOpenDocs
	$(UTILS_DIR)/html_include.awk <$< >$@
	git add $@

# update our submodules:
submods:
	git submodule foreach 'git pull origin master'

prod: $(INCS) $(HTMLFILES)
	-git commit -a 
	git pull origin master
	git push origin master

lint: 
	./lint_report.sh

local: $(HTMLFILES) $(INCS)

clean:
	touch $(PTML_DIR)/*.ptml; make local

menu_inp: $(CODE_FILES)
	echo $(CODE_FILES) > $(MENU_INP)

site_outline: menu_inp
	python3 csv_file_names.py > $(SITE_OUTLINE)

menu: site_outline $(SITE_OUTLINE)
	python3 $(UTILS_DIR)/create_menu.py $(SITE_OUTLINE) > $(NAV_BAR)

ptml_files: site_outline $(PTML_TEMPL) $(SITE_OUTLINE)
	python3 $(UTILS_DIR)/create_pages.py $(SITE_OUTLINE) $(PTML_TEMPL) $(PTML_DIR)

extract_docs:
	python3 read_docstrings.py

site_struct: menu ptml_files
	git add $(PTML_DIR)/*.ptml
	make local
