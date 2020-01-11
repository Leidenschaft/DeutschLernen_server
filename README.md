# Deutsch-Lernen
This is the server side of the project. Complete description of the project can be found under manual/Introduction.pdf with url https://github.com/Leidenschaft/Deutsch-Lernen


## Requirement
python3.7 with packages listed in `requirements.txt`.
The frontend code is organized as submodule. Use `git submodule --init update` to get the submodule contents.

## Initialize the data
* copy all xml files in `example` to `Wort` directory
* create `audio` directory and copy all audio files in `example` to `audio` directory
* create `pictures` directory and copy all picture files in `example` to  `pictures` directory
* run `python3 manage.py runserver`

## Aim
We aim to develop an user-oriented German learning software, whose features include but not limit to dictionary and translator, for students in China who learn German as a second foreign language in university.
Wir wollen eine Software, die als ein Wörterbuch oder ein Übersetzer funktionieren kann, für die Chinisischen Studentinen und Studenten um ihren Universitätlernen zu helfen machen.       
この項目の目標は、大学生にドイツ語の勉強を手伝するソフトウェアを作る。

## Current Status
* Users can view, modify the existing words
