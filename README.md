# Convert gedcom to html with bootstrap, d3 and jquery using python
## Usage



Questions : 
En cas de multiples mariages, le quel mettre ?

Pour les lieux (mariage, naissance, etc..) j'affiche quoi ? Il y a plusieurs champs différents, parfois indiqués parfois non.
Pour le moment j'affiche ville (département)





```
python gedcom2html_test.py
```
## An example says it all. So have a look at:
* [Dutch Royal Family](//picnicprojects.com/gedcom2html/dutchroyalfamily/)
## Features
- one html page for each individual in the gedcom file
- ancenstor and descendant fan charts
- a navigator chart (with d3 force simulation)
## Special Thanks
- gedcom2html uses [gedcom.py](https://github.com/nickreynke/python-gedcom) by Nick Reynke to parse the gedcom file
- [famousfamilytrees](http://famousfamilytrees.blogspot.com/?m=1) for the demo gedcom files
## To do
- beautify CSS / colors
- command line options
   * -private
      * none
      * hide dates of people alive
      * hide all people alive
   * -output-dir
   * -language
- list of people in right column
- improve age calculation
