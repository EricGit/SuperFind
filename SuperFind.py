import sublime, sublime_plugin, os
import re

g_file_scanner = None

# to run:
# window.run_command('super_find') or window.run_command('super_find_all')

#binding is alt + left click which selects the word
#http://stackoverflow.com/questions/9694823/ctrl-click-binding-in-sublime-text-2
class SuperFind(sublime_plugin.WindowCommand):
    def run(self):
        print "Should never happen - overridden"

    def super_find(self, lang):

        global g_file_scanner
        if (g_file_scanner == None):
            g_file_scanner = FileScanner(self.window.folders()[0])

        selected_text = self.get_selected_text()

        #return if nothing selected
        current_file_name = self.window.active_view().file_name()
        if selected_text == "" or current_file_name == "":
            return

        # show list if 2 or more items (also for 0 to show that we couldn't find anything)
        self.files_list = g_file_scanner.scan_files(lang.get_regex_from_token(selected_text), lang.files_to_search())
        if (len(self.files_list) != 1):
            sublime.set_timeout(self.show_quick_panel, 10)
        else:
            self.window.open_file(self.files_list[0], sublime.ENCODED_POSITION)

    def show_quick_panel(self):
        if not self.files_list:
            sublime.error_message(__name__ + ': There are no files to list.')
            return
        self.window.show_quick_panel(self.files_list, self.on_done)

    def on_done(self, picked):
        if picked == -1:
            return
        file_name = self.files_list[picked]

        #def open_file():
        self.window.open_file(file_name, sublime.ENCODED_POSITION)
        #sublime.set_timeout(open_file, 10)
    
    def get_selected_text(self):
        view = self.window.active_view()

        to_return = ""
        selection_regionset  = view.sel()  
        for selection_region in selection_regionset :  
            to_return = view.substr(selection_region)
        return to_return

#find everything
class SuperFindAllCommand(SuperFind):
    def run(self):
        lang = BaseLang()
        self.super_find(lang)

#find everything based on language
#currently only looks for ruby and javascript constants, classes, and functions
class SuperFindCommand(SuperFind):
    def run(self):
        current_file_name = self.window.active_view().file_name()        
        lang = BaseLang.create_from_file(current_file_name)
        self.super_find(lang)

#searches files using a regex pattern
#it caches content that it scans to make things faster and faster as you search
class FileScanner:
    def __init__(self, a_root):
        self.root_dir = a_root
        self.all_files = {}

        #walk all files, folders recursively
        for root, subFolders, files in os.walk(a_root):
            #print list(subFolders) - file files here???
            for filename in files:
                filepath = os.path.join(root, filename)
                self.all_files[filepath] = None

    #file_types: array
    #patterm   : string
    def scan_files(self, pattern, file_types):
        files_to_return = []
        if pattern==None:
            return files_to_return

        #folders_to_skip = ["migrate"]

        prog = re.compile(pattern)
        for file_path, file_contents in self.all_files.iteritems():
            fileExtension = os.path.splitext(file_path)[1]
            if (fileExtension in file_types):
                #we haven't read this file yet so read it now
                if file_contents == None:
                    with open( file_path, 'r' ) as f:
                        file_contents = f.readlines()

                for line_number, file_line in enumerate(file_contents):
                    if prog.search(file_line) != None:
                        files_to_return.append(file_path + ":" + str(line_number+1)) #index to line number

        return files_to_return

class BaseLang(object):
    def __init__(self):
        #do nothing
        return

    def get_regex_from_token(self, token):
        return token #search by case for token by default

    def files_to_search(self):
        return [".js", ".rb", ".erb"] #search all files

    #class method
    @staticmethod
    def create_from_file(the_file):
        file_ext = os.path.splitext(the_file)[1].lower()
        # print file_ext
        if file_ext == ".rb":
            return RubyLang()
        elif file_ext == ".js":
            return JSLang()
        else:
            return BaseLang()

class RubyLang(BaseLang):
    def __init__(self):
        super(RubyLang, self).__init__()
    def get_regex_from_token(self, token):
        if re.match("^[A-Z_]*$", token):                              #constant
            return '{0} .*='.format(token)                             
        elif token[0].isupper():      #^[A-Z]                         #class or module
            return '(class .*{0}|module .*{0})(\W+|$)'.format(token)      
        elif re.match("^[a-z_]*$", token):                            #function
            return '(def|def self.) *{0}\\b'.format(token)                 
        else:
            return None

    def files_to_search(self):
        return [".rb"]            

class JSLang(BaseLang):
    def __init__(self):
        super(JSLang, self).__init__()
    def get_regex_from_token(self, token):
        return '(function\s+{0}\\b|\\b{0}(\s|=|:)+function)'.format(token)             #function
    def files_to_search(self):
        return [".js"]            


