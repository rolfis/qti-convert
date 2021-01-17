# qti-convert
Converts QTI (LMS quiz format) in Canvas export package to other formats. 

This Python code is provided as-is and enhancements are welcome. The goal is to provide a simple script for converting QTI XML files into other formats, like PDF and Word. Even if these quizes are made digital-first, some teachers want to print them out to paper, for which there is no straightforward way today as I know about.

Uses pipenv for package dependencies. Install pipenv with `pip install pipenv` then run `pipenv install` to install needed packages in virtual environment.

Note: This code has only been tested with Canvas export packages. They need to be unzipped first. All paths are relative, so `cd` to the export directory first, then run main.py to get all paths correct. This will eventually be fixed in the future.


## Examples


    main.py imsmanifest.xml

Converts the quizes and questions to JSON on STDOUT.


    main.py -o quiz.json imsmanifest.xml

Converts the quizes and questions to JSON and writes output to file `quiz.json`.


    main.py -f docx imsmanifest.xml

Converts the quizes and questions to Microsoft Word 2007 format (docx) and outputs to file `output.docx`.

