import shutil
import os
import json
import calendar
import datetime
import subprocess
import time
import sys
import re

from tqdm import tqdm
from pathlib import Path

from modules.error_handling import Error
from modules.io import copy_with_progress
from modules.format.console_style import kiroku
from modules.config.config_handler import setting_load
from modules.format.string import fit, colorize, format_bytes, escape_latex_special_chars, today

class Workspace:
    latex_compile_times = setting_load('latex_compile_times', 'export', 'int')
    latex_command = setting_load('latex_command', 'export')

    start_time = time.time()

    def __init__(self, args=()):
        self.args = args
        
        # Check for reports file
        if not os.path.exists(setting_load('path_report_json', 'export')): 
            kiroku(f'The report file \'{setting_load('path_report_json', 'export')}\' was not found.', 'ERR')
            sys.exit()
        
        self.path = Path(setting_load('path_export', 'export'))
        self.path.mkdir(parents=True, exist_ok=True)
        self.data = {}

        # calendar settings
        calendar.setfirstweekday(0)
        self.weekdays = [
            'Montag',
            'Dienstag',
            'Mittwoch',
            'Donnerstag',
            'Freitag',
            'Samstag',
            'Sonntag'
        ]

    def prepare(self, path=None):
        if path is not None:
            self.path = Path(path)

        try:
            shutil.rmtree(self.path)
        except Exception:
            pass
        
        cache_source = setting_load('path_source', 'export')
        cache_report = setting_load('report_version', 'export')

        kiroku(f'Copy \'{cache_source}/{cache_report}\' to \'{self.path}\'', 'CPY')
        shutil.copytree(cache_source + '/' + cache_report, self.path, dirs_exist_ok=True)

        # Title page variables
        report_path = self.path / 'report.tex'
        kiroku(f'Reading {report_path.name}')
        report_content = report_path.read_text(encoding='utf-8').splitlines()

        pattern = r'\$.*?\$'
        replaced_items = 0

        for i in range(len(report_content)):
            matches = re.findall(pattern, report_content[i])
            for to_replace in matches:
                cache = setting_load(to_replace.replace('$', ''))

                if Error().is_error(cache):
                    kiroku(cache.get_error_message(), 'ERR')
                    cache.print_traceback()
                    continue
                kiroku(f'{to_replace} -> {cache}', 'DTA')
                report_content[i] = report_content[i].replace(to_replace, cache)
                replaced_items += 1
        kiroku(f'Replaced {replaced_items} variables in \'{report_path}\'', 'INF')

        kiroku(f'Writing {format_bytes(sum(len(i) for i in report_content), 2)} to {report_path.name}')
        report_path.write_text('\n'.join(report_content), encoding='utf-8')

    def load_data(self):
        self.data = json.loads(Path(setting_load('path_report_json', 'export')).read_text(encoding='utf-8'))

        for week in self.data:
            if len(self.data[week]) < 5:
                kiroku(f'{week} Detected only {len(self.data[week])} days in this week. Please check', 'WRN')
            for date in self.data[week]:
                if self.data[week][date] == []:
                    kiroku(f'{date} equals []', 'WRN')
                elif self.data[week][date] == ['$s Berufsschule']:
                    kiroku(f'{date} School Content not defined.', 'WRN')
                elif self.data[week][date] == ['Allgemein']:
                    kiroku(f'{date} Be more specific', 'WRN')

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
            lines.append('Auszubildender \\dotfill : & ' + setting_load('name_auszubildender') + ' \\\\')
            lines.append('Ausbilder \\dotfill : & ' + setting_load('name_ausbilder') + ' \\\\')
            lines.append('Tägliche Arbeitszeit \\dotfill : & ' + setting_load('recurring_worktime') + ' \\\\')
            lines.append('Druckdatum \\dotfill : & ' + today())
            lines.append('\\end{tabularx}')

            for myDate in self.data[date_range]:
                myDate_split = myDate.split('.')
                newDate = datetime.date(int(myDate_split[2]), int(myDate_split[1]), int(myDate_split[0]))

                try:
                    lines.append('\\subsection{' + myDate + ' - ' + self.weekdays[newDate.weekday()] + '}')
                except Exception as e:
                    kiroku(f'Caught exception on {newDate} with weekday {newDate.weekday()} | Exception: {e}', 'ERR')
                    sys.exit()

                lines.append('\\begin{itemize}')
                list_table_style = '{p{12cm}}'
                lines.append('\\setlength\\itemsep{' + setting_load('lists_spacing', 'style') + '}')

                if setting_load('group_lists', 'style', 'bool'):
                    list_table_style = '{| p{12cm}}'

                school_items = []
                shortcuts = {}

                for item in self.data[date_range][myDate]:
                    if not item:
                        continue

                    # Escape LaTeX special characters
                    item = escape_latex_special_chars(item)

                    if item.startswith('$s'):
                        school_items.append(item[3:] if item[2] == ' ' else item[2:])
                    elif item.startswith('$') and setting_load('shortcut_' + item[1:2], 'style'):
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

                school_mode = setting_load('school_mode', 'shortcut')

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
                        lines.append('\\item \\textbf{' + setting_load('shortcut_' + shot, 'shortcut') + '}')
                        lines.append('\\begin{itemize}')
                        for item in items:
                            if '<color:' in item:
                                item = colorize(item)
                            lines.append('\\item ' + item)
                        lines.append('\\end{itemize}')

                lines.append('\\end{itemize}')

            lines.append('\\vspace*{\\fill}')
            lines.append('\\begin{tabularx}{\\textwidth}{p{5cm} p{5cm} X}')
            lines.append('\\hrulefill & \\hrulefill &  \\\\')
            lines.append('Auszubildender & Ausbilder & \\hfill \\\\')
            lines.append(setting_load('name_auszubildender') + ' & ' + setting_load('name_ausbilder') + ' & \\\\')
            lines.append('\\end{tabularx}')

        with open(self.path / 'content.tex', 'a', encoding='utf-8') as content_writer:
            cache_content = '\n'.join(lines)
            kiroku(f'Writing {format_bytes(len(cache_content))} to \'{self.path}/content.tex\'')
            content_writer.write(cache_content + '\n')


    def build(self):
        if not self.args.build:
            kiroku('Please specify "BUILD" as a parameter if you want to build', 'INF')
            return

        self.compile_latex()
        output_pdf = self.path / 'output' / 'report.pdf'
        if output_pdf.exists():
            copy_with_progress(output_pdf, 'Wochenberichte.pdf')
            kiroku(f'Exported PDF contains {format_bytes(os.path.getsize('Wochenberichte.pdf'), rounding=2)}', 'INF')
            kiroku(f'Finished in {round(time.time() - self.start_time, 2)}s', 'INF')
        else:
            kiroku(f'Failed in {round(time.time() - self.start_time, 2)}s', 'ERR')

    def compile_latex(self):
        kiroku(f'Using compiling command: {self.latex_command}', 'INF')
        for _ in tqdm(range(self.latex_compile_times), desc=kiroku('Compiling LaTeX Document', 'INF', print_to_console=False)):
            os.chdir(self.path)
            process = subprocess.Popen(self.latex_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            os.chdir('../../../')
            stdout, stderr = process.communicate()
            Path('latex.log').write_bytes(stdout)
