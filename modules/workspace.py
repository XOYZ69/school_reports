from functools import cache

from modules.config import config_data
import shutil
import os
import json
import calendar
import datetime
import time
import sys

class Workspace:

    path = config_data['config_path_export']
    latex_command = ""
    data = {}

    weekdays = [
        'Montag',
        'Dienstag',
        'Mittwoch',
        'Donnerstag',
        'Freitag',
        'Samstag',
        'Sonntag'
    ]

    MODE = 0

    MODES = [
        'NORMAL',
        'BUILD',
        'LIST-MISSING'
    ]

    def __init__(self, args) -> None:
        calendar.setfirstweekday(0)

        if len(args) > 1:
            if args[1] in self.MODES:
                self.MODE = self.MODES.index(args[1])
            else:
                try:
                    self.MODE = int(args[1])
                except Exception:
                    pass

    def prepare(self, path=None):
        if path is not None:
            self.path = path
        
        try:
            shutil.rmtree(self.path)
        except Exception:
            pass

        self.latex_command = 'pdflatex -interaction nonstopmode -output-directory=output report.tex'
        
        shutil.copytree('latex', self.path, dirs_exist_ok=True)

        # Title page variables
        with open(self.path + '/report.tex', 'r', encoding='utf-8') as report:
            report_content = report.readlines()

        for i in range(len(report_content)):
            for key in config_data:
                to_replace = '$' + key.split('config_')[1] + '$'
                if to_replace in report_content[i]:
                    print('Replacing', to_replace, 'with', config_data[key])
                    report_content[i] = report_content[i].replace(to_replace, config_data[key])

        with open(self.path + '/report.tex', 'w', encoding='utf-8') as report:
            report.writelines(report_content)

    def load_data(self):
        self.data = json.loads(open(config_data['config_path_report_json'], 'r', encoding='utf-8').read())

        for week in self.data:
            if len(self.data[week]) < 5:
                print('---', week, 'Detected only {days} days in this week. Please check'.format(days = len(self.data[week])))
            for date in self.data[week]:
                if self.data[week][date] == []:
                    print('!!!', date, 'equals []')
                elif self.data[week][date] == ['$s Berufsschule']:
                    print('???', date, "School Content not defined.")
                elif self.data[week][date] == ['Allgemein']:
                    print('###', date, 'Be more specific')
        
        if self.MODES[self.MODE] == 'LIST-MISSING':
            sys.exit()

    def fill(self, text, length, fill, before=False):
        c = str(text)
        for i in range(len(str(text)), length):
            if before:
                c = fill + c
            else:
                c += fill
        
        return c

    def write_data(self):
        lines = []
        # Go through every year and make sections
        count = 0
        for date_range in self.data:
            count += 1
            lines.append('\\newpage')

            # lines.append('\\section{' + date_range + '}')
            lines.append('\\section{Ausbildungswoche vom ' + date_range.split('-')[0] + 'bis' + date_range.split('-')[1] + '}')

            lines.append('\\hline')
            
            lines.append('\\begin{tabularx}{\\texwidth}{p{10cm} l}')
            lines.append('Wochenbericht Nr.\\dotfill : & ' + str(count) + '\\\\')
            # lines.append('Ausbildungsnachweiß Nr.\\dotfill : & ' + self.fill(str(count), 4, '0', True) + '\\\\')
            lines.append('Ausbildungsjahr\\dotfill : & ' + date_range.split('.')[-1] + '\\\\')
            lines.append('Auszubildender \\dotfill : & ' + config_data['config_name_auszubildender'] + ' \\\\')
            lines.append('Ausbilder \\dotfill : & ' + config_data['config_name_ausbilder'] + ' \\\\')
            lines.append('Tägliche Arbeitszeit \\dotfill : & ' + config_data['config_recurring_worktime'] + ' \\\\')
            lines.append('Druckdatum \\dotfill : & ' + self.today())
            lines.append('\\end{tabularx}')

            for myDate in self.data[date_range]:
                myDate_split = myDate.split('.')
                newDate = datetime.date(int(myDate_split[2]), int(myDate_split[1]), int(myDate_split[0]))

                # lines.append('\\subsection{' + myDate + ' - ' + self.weekdays[newDate.weekday()] + ' \\hfill\\textit{8h}}')
                try:
                    lines.append('\\subsection{' + myDate + ' - ' + self.weekdays[newDate.weekday()] + '}')
                except Exception as e:
                    print('Caught exception on', newDate.ctime(), 'with weekday', newDate.weekday(), ' | Exception:', e)
                    sys.exit()

                lines.append('\\begin{itemize}')

                list_table_style = '{p{12cm}}'

                lines.append('\\setlength\itemsep{' + config_data['config_lists_spacing'] + '}')

                if config_data['config_group_lists']:
                    list_table_style = '{| p{12cm}}'


                school_items = []

                shortcuts = {}

                for item in self.data[date_range][myDate]:
                    if item == '':
                        continue

                    if item[0:2] == '$s':
                        if item[2] == ' ':
                            school_items.append(item[3:])
                        else:
                            school_items.append(item[2:])
                    elif item[0] == '$' and 'config_shortcut_' + item[1:2] in config_data:
                        if item[1:2] not in shortcuts:
                            shortcuts[item[1:2]] = []
                        
                        if item[2] == ' ':
                            shortcuts[item[1:2]].append(item[3:])
                        else:
                            shortcuts[item[1:2]].append(item[2:])
                    else:
                        if '::' in item:
                            item_s = item.split('::')

                            # If you read this please do code cleanup
                            if '-' in item_s[0]:
                                print(date_range, item, 'ERROR: - in item_s[0]')
                                sys.exit()

                            item = '\\textbf{\\textit{' + item_s[0] + '}}' + ' - '
                            for i in range(1, len(item_s)):
                                item += item_s[i]
                                if i < len(item_s) - 1:
                                    item += ' - '
                        lines.append('\\item ' + item)
                    
                    # List Sub items of tasks
                    if ' | ' in item and '$' not in item:
                        item = item.split(' - ')
                        lines[-1] = '\\item ' + item[0] + ':'

                        lines.append('\\begin{tabularx}{\\texwidth}{' + list_table_style + '}')
                        
                        # print(date_range, item)
                        for sub_item in item[1].split(' | '):
                            lines.append('- ' + sub_item +  '\\\\')
                        lines.append('\\end{tabularx}')

                school_mode = config_data['config_school_mode']

                if school_mode == 0:
                    if school_items != []:
                        # lines.append('\\paragraph{Berufsschule}'
                        lines.append('\\item \\textbf{Berufsschule}')
                        lines.append('\\begin{itemize}')
                        for item in school_items:
                            lines.append('\\item ' + item)
                        lines.append('\\end{itemize}')
                elif school_mode == 1:
                    if school_items != []:
                        lines.append('\\item \\textbf{Berufsschule}')
                        lines.append('\\begin{tabularx}{\\texwidth}{p{5cm} p{7cm}}')
                        for item in school_items:
                            cell_1 = ''
                            cell_2 = ''
                            if '::' in item:
                                cell_1 = item.split('::')[0]
                                cell_2 = item.split('::')[1]
                            else:
                                cell_1 = item
                                cell_2 = ''
                            if cell_2 != '':
                                lines.append(cell_1 + ' \\dotfill : & ' + cell_2 + '\\\\')
                            else:
                                lines.append(cell_1 + ' & ' + cell_2 + '\\\\')
                        lines.append('\\end{tabularx}')
                        pass

                if shortcuts != {}:
                    for shot in shortcuts:
                        lines.append('\\item \\textbf{' + config_data['config_shortcut_' + shot] + '}')
                        lines.append('\\begin{itemize}')
                        for item in shortcuts[shot]:
                            if '<color:' in item:
                                item = self.colorize(item)
                            lines.append('\\item ' + item)
                        lines.append('\\end{itemize}')
                    
                lines.append('\\end{itemize}')

            lines.append('\\vspace*{\\fill}')
            
            lines.append('\\begin{tabularx}{\\textwidth}{p{5cm} p{5cm} X}')
            # lines.append('\\includegraphics[height=4cm, keepaspectratio]{classified.png} & \\\\')
            # lines.append('\\hrulefill & \\hrulefill & \\includegraphics[height=4cm, keepaspectratio]{classified.png} \\\\')
            lines.append('\\hrulefill & \\hrulefill &  \\\\')
            lines.append('Auszubildender & Ausbilder & \\hfill \\\\')
            lines.append(config_data['config_name_auszubildender'] + ' & ' + config_data['config_name_ausbilder'] + ' & \\\\')

            lines.append('\\end{tabularx}')

        with open(self.path + '/content.tex', 'a', encoding='utf-8') as content:
            for line in lines:
                content.write(line + '\n')

    def build(self):
        if not self.MODES[self.MODE] == 'BUILD':
            print('Please specifiy "BUILD" as a parameterif you want to build')
            return None
        
        os.chdir(self.path)
        os.system(self.latex_command)
        os.system(self.latex_command)
    
    def today(self):
        gm = time.gmtime()
        today =  self.fill(gm.tm_mday, 2, '0', True) + '.'
        today += self.fill(gm.tm_mon,  2, '0', True) + '.'
        today += self.fill(gm.tm_year, 2, '0', True) + ' - '
        today += self.fill(gm.tm_hour, 2, '0', True) + ':'
        today += self.fill(gm.tm_min,  2, '0', True) + ':'
        today += self.fill(gm.tm_sec,  2, '0', True)
        return today
    
    def colorize(self, text):
        # https://www.overleaf.com/learn/latex/Using_colours_in_LaTeX
        split_text = text.split('color:')
        split_text[0] = split_text[0][:-1] # Remove the '<'

        color_text = split_text[1].split('>')

        return split_text[0] + '\\textcolor{' + color_text[0] + '}{' + color_text[1][:-1] + '}'

