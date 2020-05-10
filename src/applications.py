import re
import os
import json
import collections

from util import Util

class Applications():
    def __init__(self):
        self.applications = {}
        self.APP_FOLDER = '/usr/share/applications/'
        self.DESKTOP_ENTRIES = r'\[Desktop.*?[\]]'
        self.NAME_VAR = 'Name='
        self.EXEC_VAR = 'Exec='
        self.ICON_VAR = 'Icon='

    def findValue(self, key, string):
        regex = re.search(r'\b' + key, string)
        if regex == None:
            return ''
        newStr = string[regex.end():]
        end = newStr.find('\n')
        return newStr[:end].strip()

    def getProperties(self, content):
        name = self.findValue(self.NAME_VAR, content)
        exec = self.findValue(self.EXEC_VAR, content)
        icon = self.findValue(self.ICON_VAR, content)

        return { 'name' : name, 'exec': exec, 'icon': icon }
    
    def searchFiles(self, file):
        file_content = file.read()
        entries = re.split(self.DESKTOP_ENTRIES, file_content)

        isMainAdded = False

        for content in entries:
            if(len(content) < 10):
                continue

            if(isMainAdded == False):
                main = self.getProperties(content)
                main['subs'] = []
                isMainAdded = True
                continue

            main['subs'].append(self.getProperties(content))
        
        if len(main['name']) == 0 or len(main['exec']) == 0:
            return

        self.applications[main['name']] = main
    
    def generate_apps_file(self):
        self.applications = {}
        for _, __, files in os.walk(self.APP_FOLDER):
            for filename in files:
                try:
                    with open(self.APP_FOLDER + filename) as file:
                        self.searchFiles(file) 
                except:
                    print("An exception occurred", filename)

        with open(Util.get_path(self, 'apps.json'), 'w') as outfile:
            od = collections.OrderedDict(sorted(self.applications.items()))
            json.dump(od, outfile)
    
    def filter_apps(self, text):
        result = {}
        file_path = Util.get_path(self, 'apps.json')
        with open(file_path) as json_file:
            data = json.load(json_file)
            for app in data:
                if app.lower().find(text.lower()) > -1:
                    result[data[app]['name']] = data[app]
        return result