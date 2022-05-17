import pathlib
import shutil
import os
from datetime import datetime

def make_backup():
    if pathlib.Path("db\\database.sqlite3").exists() and pathlib.Path("db\\database.sqlite3").is_file():
        if not pathlib.Path("backup").exists():            
            os.mkdir("backup")
        if pathlib.Path("backup").is_dir():
            shutil.copy("db\\database.sqlite3", "backup\\"+datetime.now().strftime("%Y%m%d_%H%M")+".bkp")
            return True
        else:
            return False
    else:
        return False
    
if __name__ == "__main__":
    print (make_backup())
