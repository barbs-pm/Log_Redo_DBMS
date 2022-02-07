
from ConnectDB import ConnectDB
from beautifultable import BeautifulTable
import re

started = []
commited = []

def redo():
    print()
def criaTabela():
    print()

def pre_process():
    print()

def valorVariaveis():
    print()

def insertFirst():
    print()

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
     
main()