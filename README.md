# Grandstream_Dial
Grandstream dial is a simple Python script that allows numbers to be dialed from the command line.

## Installation

Clone the git repo in the directory you would like to install it `git clone https://github.com/havoc83/grandstream_dial`.

## Setup

Prior to first running you will want to setup your config file. First edit the values in dial_config.example.ini to reflect your devices settings, then rename the file to dial_config.ini.
Make sure you do not include ' or " around your values unless they are suppose to be there (for instance in a password).

## Execution

To run the program and have it send digits to your grandstream simply run the program using python >= 3.5.

`python dial.py 5555555555` or `python3 dial.py 5555555555` or assuming your python3 executable is located at /usr/bin `./dial.py 5555555555`

Make sure when you are entering phone numbers you do not include - or ) just the numbers dialed the same as if you were using a keypad.

## License
[MIT](https://choosealicense.com/licenses/mit/)
