import os
import uuid
import timeit

from util import Util

class Folders():
    def __init__(self):
        self.home = os.path.expanduser('~')
        self.result_folders = {}
        self.SEPARATOR = '$'

    def filter_folders(self, keyword):
        result = {}

        # Load folders if not loaded
        if len(self.result_folders.keys()) == 0:
            for root, dirs, _ in os.walk(self.home):

                dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('__')]
                
                for dir_name in dirs:
                    full_path = os.path.join(root, dir_name)
                    self.result_folders[dir_name + self.SEPARATOR + str(uuid.uuid4())] = {
                        'name': dir_name,
                        'path': full_path
                    }

        for dir_name in self.result_folders:
            if(dir_name.lower().find(keyword.lower()) == -1):
                continue

            result[dir_name] = self.result_folders[dir_name]
        return result
