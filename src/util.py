import os
import sys

class Util():
    # def __init__():
    def get_path(self, f):
        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)
        return os.path.join(application_path, f)
