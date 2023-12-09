




def count_rows_and_words(Filename):
    with open(Filename,'r',encoding='utf-8') as FILE:
        lines=FILE.readlines()

    words=0

    for line in lines:
        new_line = line.split(' ')

        for word in new_line:
            if len(word)>0 and word!=' ' and word!='\n':
                words+=1

    return (len(lines),words)

def compute_word_frequencies(Filename):
    Words=[]
    Dict={}

    with open(Filename,'r',encoding='utf-8') as FILE:
        lines=FILE.readlines()

    for line in lines:
        new_line = line.replace('\n','').split(' ')

        for word in new_line:
            if len(word)>0 and word!=' ' and word!='\n':
                if word not in Words:
                    Words.append(word)
                    Dict[word]=1
                else:
                    Dict[word]+=1

    return Dict




#print(compute_word_frequencies('File'))
#print(count_rows_and_words('File'))


