import os
import sys
import argparse
from modules.workspace import Workspace
from modules.gui import run_gui

parser = argparse.ArgumentParser()
parser.add_argument('-g', '--gui', required=False, action='store_true', help='show a gui window for editing the reports')
args = parser.parse_args()

if args.gui:
    run_gui()
else:
    # Check for reports file
    if not os.path.exists('reports.json'): 
        print(os.listdir())
        print('Reports were not found! ABORT')
        sys.exit()

    # Build the report
    reports = Workspace(sys.argv)
    reports.prepare()
    reports.load_data()
    reports.write_data()

    # Print Reports
    reports.build()
