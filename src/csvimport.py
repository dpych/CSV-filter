# -*- coding: UTF-8 -*-

__author__ = "Dawid Pych"
__date__ = "$2015-05-07 13:01:38$"

import csv
import sqlite3
import os
import platform

conn = sqlite3.connect('db.sqlite')
sklep = ""
plec = ""
baza = ""


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
    conn.commit()

def get_stuff():
    filename = 'test.csv'
    with open(filename, "rb") as csvfile:
        datareader = csv.reader(csvfile, delimiter=';', quotechar='|')
        count =0
        active =0
        purchases = []
        for row in datareader:
            count+=1
            if len(row) >= 3 and row[2] == 'active' :
                active +=1
                i = [
                    row[0].decode('utf-8'), 
                    row[3].decode('utf-8'), 
                    row[5].decode('utf-8'), 
                    row[2].decode('utf-8'), 
                    row[7].decode('utf-8'),
                    row[4].decode('utf-8'),
                    'sklep.sizeer.com']
                purchases.append(i)
                if len(purchases) >= 1000 :
                    insert_into_contact(purchases);
                    purchases = []
                #print row[0]
        insert_into_contact(purchases);
    print active
    return count

def get_export():
    global sklep, plec, baza
    
    limit = 10000
    dir = './generate/'
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

def get_rows():
    cur = conn.cursor()
    cur.execute('select count(*) from contacts')
    conn.commit()
    return cur.fetchone()
        
def print_menu():
    menu = {
        0: exit,
        1: get_stuff,
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
