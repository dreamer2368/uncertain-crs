all: all-redirect

LATEX = pdflatex
FIGURESRC = $(wildcard *.tex)
FIGUREOBJ = $(FIGURESRC:.tex=.pdf)

.SUFFIXES: .pdf .tex

.tex.pdf: 
	$(LATEX) $*

all-redirect: $(FIGUREOBJ)

%.pdf: %.tex
	pdflatex $<

clean:
	rm -f *.vrb *.tex~ *.toc *.aux *.log *.nav *.out *.snm *.flc *.aux *.gz

realclean: clean
	rm -f $(FIGUREOBJ)

