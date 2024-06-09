import os

from modules.workspace import Workspace
from modules.format.string import fit
from modules.error_handling import Error

class TestWorkspace:

    new_workspace = Workspace()

    def test_workspace_creation(self):
        self.new_workspace = Workspace()
    
    def test_workspace_preparing(self):
        self.new_workspace.prepare()
    
    def test_workspace_load_data(self):
        self.new_workspace.load_data()
    
    def test_workspace_write_data(self):
        self.new_workspace.write_data()
    
    def test_workspace_build(self):
        os.system('python setup.py --build')
        output_pdf = self.new_workspace.path / 'output' / 'report.pdf'
        with open('latex.log', 'r', encoding='utf-8') as logger:
            cache = logger.readlines()
            line_width = len(str(len(cache)))
            for line in range(len(cache)):
                print(' -- LaTeX log', fit(line, line_width, ' ', False)+ ':', cache[line], end='')
        assert output_pdf.exists
