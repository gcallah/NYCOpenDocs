# Need to export as ENV var
export TEMPLATE_DIR = templates

RECORDS_DIR = ../NYCOpenRecords
PYTHON_LINT := $(shell find $(RECORDS_DIR) -name '*.py' -exec flake8 --max-line-length 120 "{}" \;)
PTML_DIR = html_src
UTILS_DIR = utils
HTML_DIR = html
MENU_INP = $(TEMPLATE_DIR)/collect_file_namesut.txt
MENU_INPUT = collect_file_namesut.txt
SITE_OUTLINE = $(TEMPLATE_DIR)/site_struct.txt
NAV_BAR = $(TEMPLATE_DIR)/navbar.txt
PTML_TEMPL = $(TEMPLATE_DIR)/template.ptml
EXT_FILE = extensions.txt

INCS = $(NAV_BAR) $(TEMPLATE_DIR)/head.txt

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\//html\//')
HTMLFILES += $(shell ls -a $(PTML_DIR)/.*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\//html\//')

# a "fake" target to force a target to always build.
FORCE:

# packages we depend upon to build properly:
requirements: FORCE
	pip install flake8
	# we need node also, but that's best installed from:
	# https://nodejs.org/en/download/
	npm install

# update our submodules (utils and node_modules right now):
submods: FORCE
	git submodule foreach 'git pull origin master'

# run a linting tool on python and javascript code:
lint: FORCE
	./lint_report.sh

# force a new build of all html files:
clean_html: FORCE
	touch $(PTML_DIR)/*.ptml; make html_from_ptml

# we survey all files in the open records system to make our menu:
collect_file_names: FORCE
	./code_files.sh $(RECORDS_DIR) $(EXT_FILE) > $(MENU_INP)

# we pull docstrings out of python and javascript code files:
extract_docs: collect_file_names
	python3 read_docstrings.py

# site outline is a document used to make the sidebar menu:
site_outline: collect_file_names
	python3 csv_file_names.py $(EXT_FILE) > $(SITE_OUTLINE)

# now we create the menu itself:
menu: site_outline $(SITE_OUTLINE)
	python3 $(UTILS_DIR)/create_menu.py $(SITE_OUTLINE) > $(NAV_BAR)

# we create "stub" ptml files (if absent!) to be filled in later:
ptml_files: site_outline $(PTML_TEMPL) $(SITE_OUTLINE)
	python3 $(UTILS_DIR)/create_pages.py $(SITE_OUTLINE) $(PTML_TEMPL) $(PTML_DIR)
	git add $(PTML_DIR)/*.ptml

# To get the menu and uniform header on each page, we build the .html
# files from .ptml files. We also code check them:
$(HTML_DIR)/%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 $(UTILS_DIR)/html_checker.py $< 
	$(UTILS_DIR)/html_include.awk <$< >$@
	git add $@

# this is the target to build all of the html files from ptml:
html_from_ptml: $(HTMLFILES) $(INCS) extract_docs ptml_files lint
	echo "Building html from ptml."
	cp $(HTML_DIR)/index.html index.html

# this should re-build everything needed:
all: menu html_from_ptml

# push everything to production:
prod: all
	-git commit -a 
	git pull origin master
	git push origin master
