<img src="data/marketing/logo-header.png/">

<p align="right">
  <a style="font-size: 7pt" href="https://www.flaticon.com/free-icons/school" title="school icons">School icons created by Freepik - Flaticon</a>
</p>

---

**school reports** is a simple way to create, store and customize your reports.

## Disclaimer
  - Every student is responsible for their reports. No developer takes any blame if your reports do not fulfill the requirements for your school or institute you may take full responsibilty for this.
  - If you wish to change something or wish for a feature, please create a new issue [here](https://github.com/XOYZ69/school_reports/issues/new).
  - On every pull your files could be changed. So if you want to work with the newest build please backup your `modules/config.py` and `reports.json` since school reports currently does not offer automatic backups.

## Requirements

This project does need [Python](https://www.python.org/) and [LaTeX](https://www.latex-project.org/) to work corectly.

<a href="https://www.python.org/"><img src="https://skillicons.dev/icons?i=python" alt="Python"></a>
<a href="https://www.latex-project.org/"><img src="https://skillicons.dev/icons?i=latex" alt="LaTeX"></a>

### Python
Python can be installed through the provided installer or package on theri [download page](https://www.python.org/downloads/).

### LaTeX

If you have installed LaTeX please make sure the terminal command `pdflatex` is working correctly since this is the building command used for the reports.

## Prepare

  1. Firtly make sure you've installed all requirements.
  2. After that you need a `reports.json` file. This file is your base file for all your reports and lies in the main directory of the software if you did not change the config.
  3. With that said please review the file `config.py` in `modules/config.py` and change the respective values to your needs.
  4. If everything is working correctly try to run `python setup.py BUILD` for the console variant or `python setup.py --gui` for the GUI variant.
  5. After a successful build there should be a `.pdf` file in your main directory.

## Information & Tips

  - If there are any characters which are not displayed correctly it could be due to incorrect backend handling. You can try to add backslashes before it.
    - '&' -> '\\\\&'
    - You need two backslashes because of the way the software works behind the scenes.
  - Any entries starting the line with '$s' (you can replace 's' with x 'config_shortcut_x' which can be defined in the config.)
  - Using '::' will replace theese caharacters with ' - ' and make the text before it bold.
  - To use color you can use the following notation
    - \<color:red\>Text\<color:end\>
