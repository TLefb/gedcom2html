# Convert gedcom to html with bootstrap, d3 and jquery using python
## Usage



Naissance
Marriage
Contrat de mariage (CONT)
Testament (TEST)
Deces

Propriété (en haut à gauche de l'image de droite)


Freres et soeurs en dessous des enfants


Questions : 
En cas de multiples mariages, le quel mettre ?

Pour les lieux (mariage, naissance, etc..) j'affiche quoi ? Il y a plusieurs champs différents, parfois indiqués parfois non.
Pour le moment j'affiche ville (département)

0 @F01130@ FAM
1 HUSB @I00154@
1 WIFE @I02679@
1 CHAN
2 DATE 30 MAY 2022
3 TIME 08:22:59
0 @N03011@ NOTE Marié avant 1788 avec Marie DOUMEIZIEL qui décéde le 4 mars 1806

Pourquoi famille en 2022 ?

1 NAME jean louis /ATGER/
2 GIVN jean, louis
2 SURN ATGER
1 SEX M
1 _SOSADABOVILLE 162 G8
1 RELI Validé
1 FAMC @F01131@
1 BIRT
2 DATE 11 MAR 1757
2 PLAC Meyrueis, Sérigas, Lozère, France, , , , ,
3 MAP
4 LATI N44.1775335
4 LONG E3.4306186
2 NOTE @N03029@
2 SOUR @S01542@
1 FAMS @F00070@
1 FAMS @F01179@
1 FAMS @F01181@
1 BARM Y
1 BASM Y
1 OCCU cultivateur
1 SSN x
1 PROP rang 8  M
1 DEAT
2 DATE 7 FEB 1823
2 PLAC Sainte Enimie, Dignas, Lozère, France, , , , ,
3 MAP
4 LATI N44.3769826
4 LONG E3.4056394
2 NOTE @N03030@
2 SOUR @S01543@
1 NOTE @N03011@
1 FAMS @F01129@
1 FAMS @F01130@
1 FAMS @F01180@

Il a deux groupes de familles dont un qui correspond à celui en 2022 qui est en trop ? A etudier.




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
