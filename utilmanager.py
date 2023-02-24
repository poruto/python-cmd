from utilslocal.cmd import cmd
from utilslocal.hashtool import hashtool


class UtilManager:
    def __init__(self, console):
        self.console = console
        
        #  Utilizing features
        self.cmd = cmd.Cmd(self.console)
        self.hashtool = hashtool.Hashtool(self.console)
        
        