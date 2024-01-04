import os




def read_classification_from_file(Filepath):
    Dictionary = {}

    with open(Filepath, 'r', encoding='utf-8') as FILE:
        for line in FILE:
            line=line.replace('\n','').split()

            Dictionary[line[0]]=line[1]

    return Dictionary



def write_classification_to_file(Filepath,Dictionary):
    with open(Filepath, 'w', encoding='utf-8') as FILE:
        for item in Dictionary:
            FILE.write(item+' '+Dictionary[item]+'\n')


