import os

def clean():
    cwd = os.getcwd() + '/'
    os.system("rm .png")
    os.system("rm /data/out/*")
    os.system("rm /data/temp/*")
    os.system("rm /test/out/*")
