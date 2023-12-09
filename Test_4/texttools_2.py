




def count_rows_and_words(Filename):
    FILE=open(Filename,'r',encoding='utf-8')


    lines=FILE.readlines()

    words=0

    for line in lines:
        new_line = line.split(' ')

        for word in new_line:
            if len(word)>0 and word!=' ' and word!='\n':
                words+=1

    FILE.close()

    return (len(lines),words)


#print(count_rows_and_words('File'))


