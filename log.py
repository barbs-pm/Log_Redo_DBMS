from ConnectDB import ConnectDB
from beautifultable import BeautifulTable
import re

started = []
commited = []

connect = ConnectDB('trabalho_log', 'postgres','admin', '127.0.0.1', '5432')
conn = connect.ConnectDB()
conn.autocommit = False 

def redo(lines, lines_b_ckpt, ckpt_found, idxCkpt = 0):

    for i in range(len(lines_b_ckpt)-1, 0, -1):
        if 'commit' in lines_b_ckpt[i]:
            commited.append(lines_b_ckpt[i].split()[1])
        if 'start' in lines_b_ckpt[i]:
            started.append(lines_b_ckpt[i].split()[1])
        
    if ckpt_found:
        res = re.findall(r'\(.*?\)', lines[idxCkpt])
        res = "".join([x for x in res[0] if x != '(' and x != ")"])
        print(res)
        [started.append(x) for x in res.split(',')]

    commited.reverse()
    for t in commited:
        compareValues(lines, t)

def compareValues(lines, t):
    print("-- Transação --", t)
    for line in lines:
        #print(line)
        
        if t in line and 'start' not in line and 'commit' not in line and 'CKPT' not in line:
            splt = line.split(',')
            id = splt[1]
            col = splt[2]
            value = splt[3]
            cur = conn.cursor()
            cur.execute("select {} from log_table where id = {}".format(col, id))
            result = cur.fetchall()
            var = result[0][0]
            if var != value:
                cur.execute("update log_table set {} = {} where id = {}".format(col, value, id))
                print("Atualizando {} onde o id é {} para o valor {}".format(col, id, value))
                conn.commit()

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
    cur = conn.cursor()
    cur.execute("select * from log_table order by id")
    result = cur.fetchall()

    table = BeautifulTable()
    table.columns.header = ["ID", "A", "B"]

    for i in range (len(result)):
        table.rows.append(result[i])

    print(table)

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

def find_start(lines):
    start = 0
    end = False
    for idx, line in enumerate(lines):
        if 'Start CKPT' in line:
            start = idx 
        if 'End CKPT' in line:
            end = True 
    
    return start, end
  
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
    idxCkpt, end = find_start(lines)

    if end == False:
        print("CKPT nao tem END")
        lines_b_ckpt = lines
        redo(lines, lines_b_ckpt, end, idxCkpt)
    else:
        lines_b_ckpt = lines[idxCkpt::]
        redo(lines, lines_b_ckpt, end, idxCkpt)

    print("\n** SAÍDA **\n")

    for c in started:
        if c in commited:
            print(c, 'Realizou Redo')
        else:
            print(c, 'Não Realizou Redo')

    valorVariaveis()

if __name__ == '__main__': 
    main()