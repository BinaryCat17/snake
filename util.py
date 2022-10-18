from os import listdir
from os.path import isfile, join
import math

def roundup(x, base):
        return int(math.ceil(x / base)) * base

def list_files(path):
        return [join(path, f) for f in listdir(path) if isfile(join(path, f)) and f.endswith('.png')]