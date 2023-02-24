import hashlib
import traceback
from threading import Thread
from random import randint

class Hashtool:
    def __init__(self, console):
        self.console = console
        self.str_help = '\n---HashTool Usage---\nhash -help\nUsage:\n'
        self.str_help += 10 * " " + 'hash -str "HashType eg: sha256, md5, ..." "String"'
        self.str_help += "\n"
        self.str_help += 10 * " " + 'hash -find "HashType eg: sha256, md5, ..." "Path to hash file" "Path word list file"\n'
        self.str_help += 10 * " " + 'hash -getfile "HashType eg: sha256, md5, ..." "Path to file"\n'
        self.str_help += 10 * " " + 'hash -changefile "Path to file"'
        self.str_help += "\n----------------------------"
        print(self)
    
    def __str__(self):
        return "HashTool module loaded."
    
    def help(self):
        self.console.print(self.str_help, type = "help", color = "yellow")
    
    def commands(self, command):
        strings = []
        string = ""
        find = False
        for i in range(len(command)):
            if command[i] == '"':
                if not find:
                    find = True
                else:
                    find = False
                    strings.append(string)
                    string = ""
            else:
                if find:
                    string += command[i]
        
        try:
            if "-h" in command:
                self.help()
            elif "-str" in command:
                self.console.print(self.str_to_hash(strings[0], strings[1]), color = "green", type = "ok")
            elif "-find" in command:
                    Thread(target = self.find_thread(strings[0], strings[1], strings[2])).start()
            elif "-getfile" in command:
                self.console.print(self.file_to_hash(strings[0], strings[1]))
            elif "-changefile" in command:
                self.file_change_hash(strings[0])
            elif "hash" in command:
                self.help()
            else:
                error = "Command parameters incorrect"
                self.console.print(error, color = "red", type = "not_ok")
                self.help()
        except Exception as e:
            print(e)
            self.console.print("Enter all of the parameters", color = "red", type = "not_ok")
            self.help()
            
    
    def find_thread(self, hash_type, path_to_hash, path_to_world_list):
        continue_ = True
        find = False
        try:
            file = open(path_to_world_list, "r")
            lines = file.readlines()
            file.close()
        except:
            self.console.print("Failed to open the file " + path_to_world_list, color = "red", type = "not_ok")
            continue_ = False
        
        try:
            file = open(path_to_hash, "r")
            hash = file.read()
            file.close()
        except:
            self.console.print("Failed to open the file " + path_to_hash, color = "red", type = "not_ok")
            continue_ = False
        
        if continue_:
            for i in range(len(lines)):
                try:
                    str = lines[i]
                    str = str.replace("\n", "")
                    print(repr(str))
                    str_hash = self.str_to_hash(hash_type, str)
                    if hash == str_hash:
                        self.console.print(hash + "\n" + "String to this hash: " + str, color = "green", type = "ok")
                        find = True
                        break
                    else:
                        self.console.print(str_hash +  "\n", color = "orange", type = "progress")
                except:
                    self.console.print(traceback.format_exc(), color = "red", type = "not_ok")
                    break
            if not find:
                self.console.print("The hash was not found in this list.")
    
    def file_change_hash(self, path_to_file):
        self.console.print("OLD MD5: " + self.file_to_hash("md5", path_to_file), color = "orange", type = "progress")
        file = open(path_to_file, "br")
        str = file.read()
        file.close()
        str = str + bytes(randint(0, 1000))
        for i in range(len(path_to_file)):
            i_ = len(path_to_file) - 1 - i
            if path_to_file[i_] == "/":
                break
        new_path = path_to_file[0:i_ + 1]
        file_name = "hashed_" + path_to_file[i_ + 2:len(path_to_file)] 
        new_path += file_name
        file = open(new_path, "bw")
        file.write(str)
        file.close()
        self.console.print("NEW MD5: " + self.file_to_hash("md5", new_path), color = "green", type = "ok")
        
    
    def file_to_hash(self, hash_type, path_to_file):
        try:
            file = open(path_to_file, "br")
            str = file.read()
            file.close()
            new = hashlib.new(hash_type)
            new.update(str)
            return new.hexdigest()
        except:
            self.console.print(traceback.format_exc(), color = "red", type = "not_ok")
            self.help()
            return ""
                
    def str_to_hash(self, hash_type, str):
        try:
            new = hashlib.new(hash_type)
            new.update(str.encode())
            return new.hexdigest()
        except:
            self.console.print(traceback.format_exc(), color = "red", type = "not_ok")
            self.help()
            return ""
        
        
    