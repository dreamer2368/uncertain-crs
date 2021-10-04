.PHONY: FIGURES

all: all-redirect

LATEX = pdflatex
TALKNAME = overview
CHAPTERS = $(wildcard chapters/*.tex) $(wildcard chapters/**/*.tex)
REF = references.bib

.SUFFIXES: .pdf .tex

.tex.pdf: 
	$(LATEX) $*

all-redirect: $(TALKNAME).pdf

FIGURES:
	$(MAKE) -C figures

$(TALKNAME).pdf: $(TALKNAME).tex notations.tex $(REF) FIGURES $(CHAPTERS)
	pdflatex $(TALKNAME)
	bibtex $(TALKNAME)
	pdflatex $(TALKNAME)
	pdflatex $(TALKNAME)


clean:
	rm -f *.vrb *.tex~ *.toc *.aux *.log *.nav *.out *.snm *.flc
	$(MAKE) -C figures clean

realclean: clean
	rm -f $(TALKNAME).pdf
	$(MAKE) -C figures realclean

