# Basic instructions
Always save all the files in UTF8 format.

## Template
The `repport_requirements.tex` file uses a custom made template: `sgreport.cls`.

To get correct references and page numbers in the output pdf compile the `repport_requirements.tex` file twice.

## Add a chapter
Create a new file `chapter_X.tex` under `chapters/` and include it in the main `repport_requirements.tex` file with the command `\include{chapter_X}`

## Glossary
The glossary file `glossarry.tex` is located under `glossary/`

There are two types of glossary entries: acronyms and glossary entries.

To create a new glossary entry insert in `glossarry.tex` either:

* An acronym:

```latex
\newacronym{⟨label⟩}{⟨short⟩}{⟨long⟩}
```

* A glossary entry:

```latex
\newglossaryentry{⟨label⟩} 
{ 
  name={⟨name⟩}, 
  description={⟨description⟩}, 
  ⟨other options⟩ 
}
```

Then build the `repport_requirements`, build glossary using makeglossary (`makeglossary repport_requirements`), build `repport_requirements` again.

See the [Wikibook section about glossaries][WGL] to see how to use a term in the document. 

[Short guide for glossaries][GLG]
[CTAN Reference][CTAN-GL]

## Bibliography
* The `.bib` file is located under `bibliography/p1_bib.bib`

Example: 

```latex
@book{ab94,
   author* = {Charalambos D. Aliprantis and Kim C. Border},
   year = {1994},
   title = {Infinite Dimensional Analysis},
   publisher = {Springer},
   address = {Berlin}
}
```
To cite the book just insert `\cite{ab94}` in the document

Then build the bibliography:

```shell
$ latex repport_requirements
$ biber repport_requirements
$ latex repport_requirements
$ latex repport_requirements
```
Usually there is a macro in your favourite LaTeX editor to build bibliographies. Make sure that you use biber and not bibtex. Look here on how to [configure your editor][COE]
 
[Short guide about BibTeX][SGB]
To add a reference use a program from [Programs](#programs)

### Programs
* [Zotero][ZTO]: Save books, links, video references quickly. Need to setup Default Output Format (Preferences->Export). Allows drag&drop to tools like Bibdesk and Jabref.
* [Jabref][JBF]: Like [Bibdesk][BD], manage .bib files but cross platform compatible.
* [Other Alternatives][OT]

[BD]:http://bibdesk.sourceforge.net
[CTAN-GL]:http://ctan.sharelatex.com/tex-archive/macros/latex/contrib/glossaries/glossariesbegin.html#sec:defterm
[COE]:http://tex.stackexchange.com/questions/154751/biblatex-with-biber-configuring-my-editor-to-avoid-undefined-citations
[GLG]:https://philmikejones.wordpress.com/2015/02/27/glossary-acronyms-latex/
[JBF]:http://www.jabref.org
[OT]:http://mactex-wiki.tug.org/wiki/index.php?title=GUI_Tools#Bibliographies
[SGB]:https://www.economics.utoronto.ca/osborne/latex/BIBTEX.HTM
[WGL]:https://en.wikibooks.org/wiki/LaTeX/Glossary#Using_defined_terms
[ZTO]:https://www.zotero.org
