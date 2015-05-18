# -*- coding: UTF-8 -*-

__author__ = "Dawid Pych"
__date__ = "$2015-05-07 13:01:38$"

import csv
import sqlite3
import os
import platform
import sys

#sys.path.append('./')
conn = sqlite3.connect('db.sqlite')
csv.field_size_limit(sys.maxsize)
import data

output_dir = "./generate/"
unzip_dir = "./unzip/"
sklep = ""
plec = ""
baza = ""
keys = ['Address','imie','plec','Status','sklep','kod_pocztowy','baza']

data.extract_all()

def clrScr():
    if platform.system() == 'Windows' :
        os.system('cls')
    if platform.system() == 'Linux' :
        os.system('clear')

def set_up():
    contact = "select name from sqlite_master where type='table' and name='contacts'"
    cur = conn.cursor()
    cur.execute(contact)
    data = cur.fetchone()
    if data == None :
        create_table_contacts()
        print 'Tworzenie bazy danych i tabel\n';

def create_table_contacts():
    sql = "create table contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(255), email varchar(255), gender varchar(255), status varchar(255), sklep varchar(255), zipcode varchar(255), baza varchar(255))"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def insert_into_contact(purchases):
    cur = conn.cursor()
    cur.executemany('insert into contacts (email,name,gender,status,sklep,zipcode,baza) VALUES (?,?,?,?,?,?,?)', purchases)
    #poni¿ej zapytanie powoduje proporcjonalnie do wprowadzonych wierszy czas importu
    #cur.executemany('insert or replace into contacts (id,email,name,gender,status,sklep,zipcode,baza) VALUES ((select id from contacts where email=? and baza=?),?,?,?,?,?,?,?)', purchases)
    conn.commit()

def get_stuff(filename):
    #filename = 'test.csv'
    print "import pliku: " + filename;
    with open(filename, "rb") as csvfile:
        datareader = csv.reader(csvfile, delimiter=';', quotechar='|')
        count =0
        active =0
        tmp=0;
        purchases = []
        ids = {'Address':None,'imie':None,'plec':None,'Status':None,'sklep':None,'kod_pocztowy':None}

        for col in datareader.next() :
            for k in keys:
                if k==col :
                    ids.update({k:tmp})
            tmp+=1

        for row in datareader:
            count+=1
            sys.stdout.write("\r%d%%" % count)
            sys.stdout.flush()
            i = [None, None, None, None, None, None, filename]
            if len(row) >= 3 and row[2] == 'active' :
                active +=1
                
                if ids['Address'] :
                    i[0] = row[ids['Address']].decode('utf-8')
                if ids['imie'] :
                    i[1] = row[ids['imie']].decode('utf-8')
                if ids['plec'] :
                    i[2] = row[ids['plec']].decode('utf-8')
                if ids['Status'] :
                    i[3]= row[ids['Status']].decode('utf-8')
                if ids['sklep'] :
                    i[4] = row[ids['sklep']].decode('utf-8')
                if ids['kod_pocztowy'] :
                    i[5] = row[ids['kod_pocztowy']].decode('utf-8')
                
                purchases.append(i)
                if len(purchases) >= 1000 :
                    insert_into_contact(purchases);
                    purchases = []
        insert_into_contact(purchases);
    print "\n" + str(active)
    return count

def get_export():
    global sklep, plec, baza, output_dir
    
    limit = 10000
    dir = output_dir
    file = sklep + "_" + plec + "_" + baza + ".csv"

    if not os.path.exists(dir) :
        os.mkdir(dir)
        
    handler = open(dir + file, 'wb')
    wr = csv.writer(handler, quoting=csv.QUOTE_ALL)
    
    rows = get_rows();
    i = rows[0]//limit #przebiegi
    if rows[0]%limit > 0 :
        i += 1
    
    for n in range(0,i) :
        cur = conn.cursor()
        rows = cur.execute('select * from contacts limit %i,%i'  % (n*limit, limit))
        conn.commit()
        for row in rows :
            wr.writerow((
                row[2].encode("utf-8"),
                row[1].encode("utf-8")
            ))
#            print row 

def get_data():
    lista = data.get_list_files('csv',unzip_dir);
    clrScr()
    print lista
    for filename in lista:
        get_stuff(unzip_dir + filename);

def get_rows():
    cur = conn.cursor()
    cur.execute('select count(*) from contacts')
    conn.commit()
    return cur.fetchone()
        
def print_menu():
    menu = {
        0: exit,
        1: get_data,
        2: setup_export
    }
    clrScr()
    print "\n1. Importuj do programu"
    print "2. Exportuj"
    print "0. Zamknij program"
    option = input( "Wybiecz opcje:" )
    menu[option]()
    print_menu()
    
def setup_export():
    clrScr()
    o = None
    menu = {
        0 : print_menu,
        1 : set_sklep,
        2 : set_plec,
        3 : set_baza,
        4 : get_export
    }
    print "\nUstawienia:\n\tSklep: ", sklep , "\n\tPlec: ", plec ,"\n\tBaza: ", baza
    print "\n1. Wybierz sklep"
    print "2. Wybiery pleæ"
    print "3. Wybiery bazê"
    if sklep and plec and baza:
        print "4. wykonaj export"
        
    o = input( "Wybiecz opcje:" )

    if o != None :
        if o != 4 :
            menu[o]()
        if o == 4 and sklep and plec and baza :
            menu[o]()
    
def set_sklep():
    global sklep
    sklep = raw_input( "Podaj nazwê sklepu: " )
    setup_export()

def set_plec():
    global plec 
    plec = raw_input( "Podaj p³eæ: " )
    setup_export()

def set_baza():
    global baza 
    baza = raw_input( "Podaj baza: " )
    setup_export()

if __name__ == "__main__":
    set_up()
    print_menu()
