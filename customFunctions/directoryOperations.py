from shutil import rmtree
from os import listdir


def deleteDir(dir_name):
    rmtree(dir_name)


def scanDir():
    files = listdir('.')
    for file in files:
        q = file[0]
        if q == "q":
            return file
