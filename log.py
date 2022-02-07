
from ConnectDB import ConnectDB
from beautifultable import BeautifulTable
import re

started = []
commited = []

connect = ConnectDB('vintage', 'rafinha','senha', 'localhost', '5432')
conn = connect.ConnectDB()
conn.autocommit = False 

def redo():
    print()
def criaTabela():
    cur = conn.cursor()
    cur.execute("create table if not exists log_table (id int not null, a int, b int, primary key(id))")
    conn.commit
    print("Tabela criada com sucesso")

def pre_process(lines):
    for idx in range(len(lines)):
        lines[idx] = re.sub('\n', '', lines[idx])
        lines[idx] = re.sub('<', '',lines[idx])
        lines[idx] = re.sub('>', '',lines[idx])
    
    return lines


def valorVariaveis():
    print()

def insertFirst( lines, idx):
    cur = conn.cursor()
    cur.execute("truncate table log_table")
    inserts = lines[0:idx]

    for ins in inserts:
        ins = re.sub('=', ',', ins)
        splt = ins.split(',')
        cur.execute("select * from log_table where id = {}".format(splt[1]))
        result = cur.fetchall()
        if result:
            cur.execute("update log_table set {} = {} where id = {}".format(splt[0], splt[2], splt[1]))
        else:
            cur.execute("insert into log_table (id, {}) values ({}, {})".format(splt[0], splt[1], splt[2]))

    conn.commit()
    print("\n------\nValores antes do REDO")
    valorVariaveis()

def find_start():
    print()
  
def main():
    file = open('t.txt', 'r') 
    lines = []
    for f in file:
        lines.append(f)
    
    lines = pre_process(lines)

    criaTabela()

    ins = 0
    for idx in range(len(lines)):
        if lines[idx] == '':
            ins = idx
            insertFirst(lines, idx)
            break
    
    lines = lines[ins+1::]
    

    
    print("\n** SAÍDA **\n")

    for c in started:
        if c in commited:
            print(c, 'Realizou Redo')
        else:
            print(c, 'Não Realizou Redo')

    valorVariaveis()

if __name__ == '__main__': 
    main()