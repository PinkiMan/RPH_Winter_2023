




def read_classification_from_file(Filepath):
    Dictionary = {}

    with open(Filepath, 'r', encoding='utf-8') as FILE:
        for line in FILE:
            line=line.replace('\n','').split()

            Dictionary[line[0]]=line[1]

    return Dictionary






