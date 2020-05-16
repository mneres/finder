import os
from subprocess import Popen
import pipes

from gi.repository import Gio

class Applications():
    def __init__(self):
        self.applications = {}
        self.APP_FOLDER = '/usr/share/applications/'

    def getProperties(self, app, file_path):
        name = app.get_name()
        exec = app.get_string('Exec')
        icon = app.get_string('Icon')
        file_path = file_path
        # print(app.get_boolean('Terminal'))
        return { 'name' : name, 'exec': exec, 'icon': icon, 'file_path': file_path }

    def generate_apps_file(self):
        self.applications = {}
        for _, _, files in os.walk(self.APP_FOLDER):
            for filename in files:
                try:
                    file_path = os.path.join(self.APP_FOLDER, filename)
                    app = Gio.DesktopAppInfo.new_from_filename(file_path)
                    result = self.getProperties(app, file_path)
                    self.applications[result['name']] = result
                except:
                    print("An exception occurred", filename)
    
    def filter_apps(self, text):
        result = {}
        for app in self.applications:
            if app.lower().find(text.lower()) > -1:
                result[app] = self.applications[app]
        return result

    def launch_app(self, app_name):
        file_path = self.applications[app_name]['file_path']
        app = Gio.DesktopAppInfo.new_from_filename(file_path)
        app.launch()
