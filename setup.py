import os
import sys
import argparse

from modules.gui import run_gui
from modules.workspace import Workspace
from modules.format.console_style import kiroku
from modules.config.config_handler import setting_load

parser = argparse.ArgumentParser()
parser.add_argument('-g', '--gui', required=False, action='store_true', help='show a gui window for editing the reports')
parser.add_argument('-b', '--build', required=False, action='store_true', help='build the pdf report')
args = parser.parse_args()

def main():
    kiroku('Starting console version', 'INF')

    # Build the report
    reports = Workspace(args)
    reports.prepare()
    reports.load_data()
    reports.write_data()

    # Print Reports
    reports.build()

if args.gui:
    kiroku('Starting gui version', 'INF')
    run_gui()
else:
    if __name__ == "__main__":
        main()
