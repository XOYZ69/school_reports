import shutil
import os
import json
import calendar
import datetime
import subprocess
import time
import sys
import logging
from colorama import Fore
from modules.config import config_data
from tqdm import tqdm
from pathlib import Path

class Workspace:
    latex_compile_times = 2
    latex_command = [
        'pdflatex',
        '-interaction=nonstopmode',
        '-output-directory=output',
        'report.tex'
    ]

    start_time = time.time()

    def __init__(self, args):
        self.path = Path(config_data['config_path_export'])
        self.data = {}
        self.weekdays = [
            'Montag',
            'Dienstag',
            'Mittwoch',
            'Donnerstag',
            'Freitag',
            'Samstag',
            'Sonntag'
        ]
        self.MODE = 0
        self.MODES = [
            'normal',
            'build',
            'list-missing'
        ]

        calendar.setfirstweekday(0)

        if len(args) > 1:
            if args[1].lower() in self.MODES:
                self.MODE = self.MODES.index(args[1].lower())
            else:
                try:
                    self.MODE = int(args[1])
                except ValueError:
                    pass

    def prepare(self, path=None):
        if path is not None:
            self.path = Path(path)

        try:
            shutil.rmtree(self.path)
        except Exception:
            pass

        shutil.copytree('latex', self.path, dirs_exist_ok=True)

        # Title page variables
        report_path = self.path / 'report.tex'
        report_content = report_path.read_text(encoding='utf-8').splitlines()

        for i in range(len(report_content)):
            for key in config_data:
                to_replace = '$' + key.split('config_')[1] + '$'
                if to_replace in report_content[i]:
                    logging.info(f'Replacing {to_replace} with {config_data[key]}')
                    report_content[i] = report_content[i].replace(to_replace, config_data[key])

        report_path.write_text('\n'.join(report_content), encoding='utf-8')

    def load_data(self):
        self.data = json.loads(Path(config_data['config_path_report_json']).read_text(encoding='utf-8'))

        for week in self.data:
            if len(self.data[week]) < 5:
                logging.warning(f'--- {week} Detected only {len(self.data[week])} days in this week. Please check')
            for date in self.data[week]:
                if self.data[week][date] == []:
                    logging.warning(f'{date} equals []')
                elif self.data[week][date] == ['$s Berufsschule']:
                    logging.warning(f'{date} School Content not defined.')
                elif self.data[week][date] == ['Allgemein']:
                    logging.warning(f'{date} Be more specific')

        if self.MODES[self.MODE] == 'list-missing':
            sys.exit()

    def fill(self, text, length, fill, before=False):
        c = str(text)
        while len(c) < length:
            c = fill + c if before else c + fill
        return c

    def escape_latex_special_chars(self, text):
        latex_special_chars = {
            '#': '\#',
        }
        for char, replacement in latex_special_chars.items():
            text = text.replace(char, replacement)
        return text

    def write_data(self):
        lines = []
        count = 0
        for date_range in self.data:
            count += 1
            lines.append('\\newpage')
            lines.append('\\section{Ausbildungswoche vom ' + date_range.split('-')[0] + ' bis ' + date_range.split('-')[1] + '}')
            lines.append('\\hline')

            lines.append('\\begin{tabularx}{\\textwidth}{p{10cm} l}')
            lines.append('Wochenbericht Nr.\\dotfill : & ' + str(count) + '\\\\')
            lines.append('Ausbildungsjahr\\dotfill : & ' + date_range.split('.')[-1] + '\\\\')
            lines.append('Auszubildender \\dotfill : & ' + config_data['config_name_auszubildender'] + ' \\\\')
            lines.append('Ausbilder \\dotfill : & ' + config_data['config_name_ausbilder'] + ' \\\\')
            lines.append('Tägliche Arbeitszeit \\dotfill : & ' + config_data['config_recurring_worktime'] + ' \\\\')
            lines.append('Druckdatum \\dotfill : & ' + self.today())
            lines.append('\\end{tabularx}')

            for myDate in self.data[date_range]:
                myDate_split = myDate.split('.')
                newDate = datetime.date(int(myDate_split[2]), int(myDate_split[1]), int(myDate_split[0]))

                try:
                    lines.append('\\subsection{' + myDate + ' - ' + self.weekdays[newDate.weekday()] + '}')
                except Exception as e:
                    logging.error(f'Caught exception on {newDate} with weekday {newDate.weekday()} | Exception: {e}')
                    sys.exit()

                lines.append('\\begin{itemize}')
                list_table_style = '{p{12cm}}'
                lines.append('\\setlength\\itemsep{' + config_data['config_lists_spacing'] + '}')

                if config_data['config_group_lists']:
                    list_table_style = '{| p{12cm}}'

                school_items = []
                shortcuts = {}

                for item in self.data[date_range][myDate]:
                    if not item:
                        continue

                    # Escape LaTeX special characters
                    item = self.escape_latex_special_chars(item)

                    if item.startswith('$s'):
                        school_items.append(item[3:] if item[2] == ' ' else item[2:])
                    elif item.startswith('$') and 'config_shortcut_' + item[1:2] in config_data:
                        shortcuts.setdefault(item[1:2], []).append(item[3:] if item[2] == ' ' else item[2:])
                    else:
                        if '::' in item:
                            item_s = item.split('::')
                            if ' - ' in item_s[0]:
                                item_parts = item_s[0].split(' - ', 1)
                                lines.append('\\item \\textbf{\\textit{' + item_parts[0] + '}} - ' + item_parts[1])
                            else:
                                lines.append('\\item \\textbf{\\textit{' + item_s[0] + '}}')
                            
                            if len(item_s) > 1:
                                lines.append('\\begin{tabularx}{\\textwidth}{' + list_table_style + '}')
                                for sub_item in item_s[1].split(' | '):
                                    lines.append('- ' + sub_item + '\\\\')
                                lines.append('\\end{tabularx}')
                        else:
                            lines.append('\\item ' + item)

                school_mode = config_data['config_school_mode']

                if school_mode == 0 and school_items:
                    lines.append('\\item \\textbf{Berufsschule}')
                    lines.append('\\begin{itemize}')
                    for item in school_items:
                        lines.append('\\item ' + item)
                    lines.append('\\end{itemize}')
                elif school_mode == 1 and school_items:
                    lines.append('\\item \\textbf{Berufsschule}')
                    lines.append('\\begin{tabularx}{\\textwidth}{p{5cm} p{7cm}}')
                    for item in school_items:
                        cell_1, cell_2 = item.split('::') if '::' in item else (item, '')
                        lines.append(cell_1 + ' \\dotfill : & ' + cell_2 + '\\\\' if cell_2 else cell_1 + ' & ' + cell_2 + '\\\\')
                    lines.append('\\end{tabularx}')

                if shortcuts:
                    for shot, items in shortcuts.items():
                        lines.append('\\item \\textbf{' + config_data['config_shortcut_' + shot] + '}')
                        lines.append('\\begin{itemize}')
                        for item in items:
                            if '<color:' in item:
                                item = self.colorize(item)
                            lines.append('\\item ' + item)
                        lines.append('\\end{itemize}')

                lines.append('\\end{itemize}')

            lines.append('\\vspace*{\\fill}')
            lines.append('\\begin{tabularx}{\\textwidth}{p{5cm} p{5cm} X}')
            lines.append('\\hrulefill & \\hrulefill &  \\\\')
            lines.append('Auszubildender & Ausbilder & \\hfill \\\\')
            lines.append(config_data['config_name_auszubildender'] + ' & ' + config_data['config_name_ausbilder'] + ' & \\\\')
            lines.append('\\end{tabularx}')

        with open(self.path / 'content.tex', 'a', encoding='utf-8') as content:
            content.write('\n'.join(lines) + '\n')


    def build(self):
        if self.MODES[self.MODE] != 'build':
            logging.info('Please specify "BUILD" as a parameter if you want to build')
            return

        self.compile_latex()
        output_pdf = self.path / 'output' / 'report.pdf'
        if output_pdf.exists():
            self.copy_with_progress(output_pdf, 'Wochenberichte.pdf')
            logging.info(f'Finished in {round(time.time() - self.start_time, 2)}s')
        else:
            logging.error(f'Failed in {round(time.time() - self.start_time, 2)}s')

    def compile_latex(self):
        for _ in tqdm(range(self.latex_compile_times), desc=time.ctime() + ' Compiling LaTeX Document'):
            os.chdir(self.path)
            process = subprocess.Popen(self.latex_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            os.chdir('..')
            stdout, stderr = process.communicate()
            Path('latex.log').write_bytes(stdout)

    def copy_with_progress(self, src, dst, chunk_size=1024):
        total_size = os.path.getsize(src)
        progress_bar = tqdm(
            desc=time.ctime() + f' Copying [{src}]',
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024
        )

        with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
            while True:
                data = fsrc.read(chunk_size)
                if not data:
                    break
                fdst.write(data)
                progress_bar.update(len(data))

        progress_bar.close()

    def today(self):
        gm = time.gmtime()
        return (self.fill(gm.tm_mday, 2, '0', True) + '.' +
                self.fill(gm.tm_mon, 2, '0', True) + '.' +
                self.fill(gm.tm_year, 2, '0', True) + ' - ' +
                self.fill(gm.tm_hour, 2, '0', True) + ':' +
                self.fill(gm.tm_min, 2, '0', True) + ':' +
                self.fill(gm.tm_sec, 2, '0', True))

    def colorize(self, text):
        split_text = text.split('color:')
        split_text[0] = split_text[0][:-1]
        color_text = split_text[1].split('>')
        return split_text[0] + '\\textcolor{' + color_text[0] + '}{' + color_text[1][:-1] + '}'
