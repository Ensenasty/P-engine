SOURCES != fd *.py --type f .

.SUFFIXES=
.SUFFIXES= py

.PHONY: default installreqs

default:

contreq: requirements.txt
	python -m pip install -upgrade pip
	python -m pip install wheel
	pip install -r requirements.txt

installreqs: requirements.txt
	source .venv/bin/activate && pip install -r $<

tags: $(SOURCES)
	ctags -f $@ $<

%:

