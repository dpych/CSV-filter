# -*- coding: utf-8 -*-  
__author__ = "Dawid Pych"
__date__ = "$2015-05-18 09:31:57$"

from prettytable import from_db_cursor, from_csv
import sqlite3
import glob
import os
import zipfile
import tempfile

import_dir = "./import/"
unzip_dir = "./unzip/"

if not os.path.exists(import_dir) :
    os.mkdir(import_dir)

if not os.path.exists(unzip_dir) :
    os.mkdir(unzip_dir)

if __name__ == "__main__":
    print "Tylko do importu. Zestaw funkcji"
    
def test():    
    print 'dziala'
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute("select * from contacts");
    tab = from_db_cursor(c)
    t =  tab.get_string()
    print t.encode('utf-8')

def extract_all():
    lista = get_list_files("zip")
    temp_dir = tempfile.mkdtemp()
    count = 100/len(lista);
    for zip in lista :
        tmp = zip.split('.')
        with zipfile.ZipFile(import_dir + zip,"r") as z:
            z.extractall(temp_dir)
        with zipfile.ZipFile(import_dir + zip,"r") as z:
            for f in z.namelist() :
                newname = tmp[0] + '_' + f
                newname = os.path.join(unzip_dir, newname)
                if not os.path.exists(newname) :
                    os.rename(os.path.join(temp_dir, f), newname)
    return True
        
    
def show_csv_file(name):
    fp = open(name, "r")
    mytab = from_csv(fp)
    fp.close()
    print mytab
    
def get_list_files(ext='csv',dir = None):
    global import_dir
    if not dir : 
        lista = glob.glob(import_dir + '*.'+ ext )
    else :
        lista = glob.glob(dir + '*.'+ ext )
        
    files = []
    for file in lista :
        tmp = file.split("\\")
        files.append(tmp[-1])
    return files
        
    