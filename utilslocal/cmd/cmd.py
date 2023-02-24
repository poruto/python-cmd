import os
import ctypes
import platform, subprocess
from threading import Thread


kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
SW_HIDE = 0
SW_SHOW = 1


class Cmd:
    def __init__(self, console):
        self.console = console
        Thread(target = self.main).start()
        self.cmd = True
        self.hide = True
        self.toggle()
        print(self)
    
    def __str__(self):
        return "CMD module loaded."
    
    def toggle(self):
        hWnd = kernel32.GetConsoleWindow()
        if hWnd and self.cmd:
            user32.ShowWindow(hWnd, SW_HIDE)
        elif hWnd and not self.cmd:
            user32.ShowWindow(hWnd, SW_SHOW)
        self.cmd = not(self.cmd)
        
    def main(self):
        self.print("Windows Command Prompt" + "\n" + "(c) 2020 Microsoft Corporation.\n")
        self.print(20*"-" + "PC UNAME" + 20 *"-", get_computer(), 47 *"-")
        while True:
            command = input(">>> ")
            if command == "clear":
                self.print(100*"\n")
            else:
                os.system(command)
                self.print("\n")
    
    def print(self, *args):
        for i in range(len(args)):
            print(args[i])
            

def get_computer():
    string = "\n"
    nodes = platform.uname()
    cmd = 'wmic csproduct get uuid'
    uuid = str(subprocess.check_output(cmd))
    pos1 = uuid.find("\\n")+2
    uuid = uuid[pos1:-15]
    string += "UUID: " + uuid + "\n"
    for i in range(len(nodes)):
        string += nodes[i] + "\n"
    return string