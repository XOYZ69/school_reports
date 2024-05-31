import os
import sys
from modules.workspace import Workspace

print('Printing all available reports')

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
