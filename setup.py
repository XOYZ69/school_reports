import os
import sys
import argparse

from modules.workspace import Workspace
from modules.gui import run_gui
from modules.config.config_handler import setting_load

parser = argparse.ArgumentParser()
parser.add_argument('-g', '--gui', required=False, action='store_true', help='show a gui window for editing the reports')
args = parser.parse_args()

def main():
    print('Printing all available reports')
    
    # Check for reports file
    if not os.path.exists(setting_load('path_source', 'export')): 
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

if args.gui:
    run_gui()
else:
    if __name__ == "__main__":
        main()
