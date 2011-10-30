import os
import inspect

def find_file(filename, clazz_or_path):

    """ If file is relative, unrelate... """

    if filename[0] == "/":

        return filename

    if type(clazz_or_path) == type(""):
        return os.path.join(os.path.dirname(clazz_or_path), filename)

    return os.path.join(os.path.dirname(inspect.getfile(clazz_or_path)), 
                        filename)
