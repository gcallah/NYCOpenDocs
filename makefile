# Need to export as ENV var
export TEMPLATE_DIR = templates
# PYTHONFILES = $(shell find ../NYCOpenRecords -name '*.py')
FILES = $(shell find ../NYCOpenRecords \( -name '*.py' -or -name '*.js' -or -name '*.yml' -or -name '*.sh' \))
PTML_DIR = html_src
UTILS_DIR = utils
MENU_INP = $(TEMPLATE_DIR)/menu_input.txt
SITE_OUTLINE = $(TEMPLATE_DIR)/site_struct.txt
NAV_BAR = $(TEMPLATE_DIR)/navbar.txt

INCS = $(NAV_BAR) $(TEMPLATE_DIR)/head.txt

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

menu_inp: $(FILES)
	echo $(FILES) > $(MENU_INP)

site_outline: menu_inp
	python3 csv_file_names.py > $(SITE_OUTLINE)

menu: site_outline
	python3 $(UTILS_DIR)/create_menu.py $(SITE_OUTLINE) > $(NAV_BAR)

ptml_files: site_outline
	python3 $(UTILS_DIR)/create_pages.py $(SITE_OUTLINE) $(UTILS_DIR)/templates/template.ptml $(PTML_DIR)

site_struct: menu ptml_files
	git add $(PTML_DIR)/*.ptml
	make local
