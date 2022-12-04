import os

def clean():
    
    if os.path.exists(os.getcwd() + '.png'):
        os.system("rm .png")
                      
    if os.path.exists(os.getcwd() + '/data/out'):
        if os.listdir(os.getcwd() + '/data/out'):
            os.system("rm data/out/*")
        
    if os.path.exists(os.getcwd() + '/data/temp'):
        if os.listdir(os.getcwd() + '/data/temp'):
            os.system("rm data/temp/*")
    
    if os.path.exists(os.getcwd() + '/test/out'):
        if os.listdir(os.getcwd() + '/test/out'):
            os.system("rm test/out/*")

            