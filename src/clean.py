import os

def clean():
    
    if os.path.exists(os.getcwd() + '.png'):
        os.system("rm .png")
                      
    if os.path.exists(os.getcwd() + '/data/out'):
        os.system("rm -r data/out")
        
    if os.path.exists(os.getcwd() + '/data/temp'):
        os.system("rm -r data/temp")
    
    if os.path.exists(os.getcwd() + '/test/out'):
        os.system("rm -r test/out")

            