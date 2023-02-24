import tkinter as tk
import ctypes
import subprocess, os
from tkinter import ttk
from tkinter import filedialog as fd
from threading import Thread

from utilmanager import UtilManager


def exit():
    os._exit(0)


class Console:
    VERSION = "1.0"
    
    def __init__(self):
        self.bgcolor = "#%02x%02x%02x" % (25, 17, 17)
        self.fgcolor = "white"
        self.font = "Arial 11"
        self.welcome_message = "Command Prompt Helper [Version " + str(self.VERSION) + "]" + "\n" + "[INSERT]: Toggle visibility" + "\n"
        self.command_enter_char = ">>>"
        self.console_resolution = (800, 400)
        self.tool_resolution = (self.console_resolution[0] + 20, 25)
        self.hide = False
        self.pressed = False
        
        #  UtilManager
        self.utilmanager = UtilManager(self)
    
    def init(self):
        Thread(target = self.main).start()
    
    def main(self):
        self.root = tk.Tk()
        self.root.title("Console")
        self.root.configure(bg = self.bgcolor)
        self.root.attributes("-alpha", 0.95)
        self.root.minsize(self.console_resolution[0], self.console_resolution[1])
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
                
        #  TTK SETTINGS
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure("TSeparator", background = "red")
        self.style.configure("Horizontal.TScale", background = self.bgcolor, fieldbackground = "red",  troughcolor= "#%02x%02x%02x" %(255, 46, 46))
        self.style.configure("TMenubutton", relief=tk.FLAT, font= self.font, bd=0, highlightthickness=0,
        arrowcolor="#909090", foreground= self.fgcolor, background= self.bgcolor)
        
        #  Frames
        self.main_frame = tk.Frame(self.root, bg = self.bgcolor)
        
        self.tool_frame = tk.Frame(self.main_frame, bg = self.bgcolor,
                              highlightbackground = "#%02x%02x%02x" % (200, 8, 8), highlightthickness = 2,
                              width = self.tool_resolution[0], height = self.tool_resolution[1])
        self.tool_frame.bind('<Button-1>',self.clickwin)
        self.tool_frame.bind('<B1-Motion>', lambda event: self.dragwin(event,self.root))
        
        self.console_frame = tk.Frame(self.main_frame, bg = self.bgcolor,
                              highlightbackground = "#%02x%02x%02x" % (100, 8, 8), highlightthickness = 1,
                              width = self.console_resolution[0], height = self.console_resolution[1])
        
        #  Console Frame
        self.text = tk.Text(self.console_frame, width = 100, height = 25,
                            bg = self.bgcolor, fg = "white", font = self.font, insertbackground = "red",
                            highlightthickness = 0, highlightcolor = self.bgcolor, highlightbackground = self.bgcolor)
        self.text.tag_config("python", foreground = "yellow")
        self.text.insert(tk.END, "Python ", "python")
        self.text.insert(tk.END, self.welcome_message)
        self.text.insert(tk.END, self.command_enter_char)
        self.text.bind("<Return>", self.execute_command)
        
        self.scrollb = ttk.Scrollbar(self.console_frame, command= self.text.yview)
        self.scrollb.grid(row=0, column=1, sticky='nsew')
        self.text['yscrollcommand'] = self.scrollb.set
        
        self.menu = tk.Menu(self.text, tearoff = 0, font = self.font)
        self.menu.add_command(label = "Tools", font = ("Arial", 9, "bold"))
        self.menu.add_separator()
        self.menu.add_command(label = "Path", command = self.insert_path, font = ("Arial", 9))
        self.menu.add_command(label = "Clear", command = self.clear, font = ("Arial", 9))
        
        self.text.bind("<Button-3>", self.do_popup)
        
        #  Tools Frame
        self.button_exit = tk.Button(self.tool_frame, text = "EXIT",
                                     bg = self.bgcolor, fg = self.fgcolor, font = "Arial 10", command = exit)
        self.checkbox_var = tk.IntVar()
        self.checkbox_var.set(False)
        self.checkbox_cmd = tk.Checkbutton(self.tool_frame, text = "CMD", variable = self.checkbox_var,
                                           bg = self.bgcolor, fg = self.fgcolor, command = self.utilmanager.cmd.toggle,
                                           activebackground= self.bgcolor, activeforeground= self.fgcolor, selectcolor= self.bgcolor)
        
        #  Frame Gridding
        self.main_frame.grid(column = 0, row = 1)
        self.console_frame.grid(column = 0, row = 1)
        self.tool_frame.grid(column = 0, row = 0, sticky = "we")
        
        #  Console Frame Gridding
        self.text.grid(row = 0, column = 0)
        
        #  Tool Frame Gridding
        self.button_exit.grid(row = 0, column = 0)
        self.checkbox_cmd.grid(row = 0, column = 2)
        
        self.root.after(100, self.check_user_input)
        self.root.mainloop()
    
    def check_user_input(self):
        if ctypes.windll.user32.GetKeyState(0x2D) > 0x0008 and not self.pressed:
            self.pressed = True
            if self.hide:
                self.root.deiconify()
            else:
                self.root.withdraw()
            self.hide = not(self.hide)
        elif not ctypes.windll.user32.GetKeyState(0x2D) > 0x0008:
            self.pressed = False
            
        self.root.after(100, self.check_user_input)
    
    def print(self, *args, color = "white", type = "normal"):
        self.text.tag_config(type, foreground = color)
        text = ""
        for i in range(len(args)):
            text += str(args[i])
            text += " "
        text += "\n"
        self.text.insert(tk.END, text, type)
        self.text.yview_moveto(1)
        self.utilmanager.cmd.print(text)
    
    def wait_command(self):
        pass_ = False
        content = self.text.get("1.0", "end-1l")
        lines = content.splitlines()
        last_line = lines[len(lines) - 1]
        command = last_line.replace(self.command_enter_char, "")
        commands = command.split(" ")
        if len(command.strip()) < 1:
            pass_ = True
        elif "exit" in commands:
            exit()
        elif "start" in commands:
            commands.insert(commands.index("start") + 1, ' ' + '""' + ' ')
            command = ""
            for i in range(len(commands)):
                command += commands[i]
            os.system(command)
            pass_ = True
        elif "ping" in commands:
            p = subprocess.Popen(command)
            p.wait()
            sucess = p.poll()
            if sucess == 0:
                sucess = "Ping was successful"
                self.print(sucess, color = "green", type = "ok")
            else:
                sucess = "Destination is unreachable."
                self.print(sucess, color = "red", type = "not_ok")
        elif "hash" in commands:
            self.utilmanager.hashtool.commands(command)
        else:
            try:
                output = subprocess.check_output(commands, shell = False, encoding="437")
                self.print(output, color = "green", type = "ok")
            except:
                error = "Command incorrect \n"
                self.print(error, color = "red", type = "not_ok")
        if not pass_:
            self.text.insert(tk.END, self.command_enter_char)
    
    def clear(self):
        self.text.delete("1.0", tk.END)
        self.insert_char()
    
    def insert_path(self):
        filename = fd.askopenfilename()
        if filename == "":
            pass
        else:
            self.text.insert(tk.END, '"' + filename + '"')
    
    def execute_command(self, *args):
        Thread(target = self.insert_char).start()
        Thread(target = self.wait_command).start()
    
    def do_popup(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()
    
    def insert_char(self):
        self.text.insert(tk.END, self.command_enter_char)
        
    def dragwin(self, event, parent):
        x = parent.winfo_pointerx() - self._offsetx
        y = parent.winfo_pointery() - self._offsety
        parent.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x
        self._offsety = event.y

        
if __name__ == "__main__":
    c = Console()
    c.init()