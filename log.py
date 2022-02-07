
from ConnectDB import ConnectDB
from beautifultable import BeautifulTable
import re

def redo():

def criaTabela():

def pre_process():

  
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

     
main()