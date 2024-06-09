from modules.error_handling import Error
from modules.workspace import Workspace

class TestWorkspace:
    def test_workspace_creation(self):
        self.new_workspace = Workspace()
    
    def test_workspace_preparing(self):
        self.test_workspace_creation()
        self.new_workspace.prepare()
    
    def test_workspace_load_data(self):
        self.test_workspace_preparing()
        self.new_workspace.load_data()
    
    def test_workspace_write_data(self):
        self.test_workspace_load_data()
        self.new_workspace.write_data()
