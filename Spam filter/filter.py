
import utils
import corpus

import os
import re

class Data:
    def __init__(self, Name):
        self.Name = Name
        self.OK = 0
        self.SPAM = 0

class MyFilter:
    def __init__(self):
        self.Words = []
        self.URLs = []
        self.Mail_Addresses = []

        self.Word_List = []

        self.Threshold = 0.7 # Percentage
        self.Max_Words = 100


    def train(self, path):
        dictionary = utils.read_classification_from_file(os.path.join(path,'!truth.txt'))

        Corpus_Obj = corpus.Corpus(path)

        for email in Corpus_Obj.emails():
            Filename = email[0]
            Content = email[1]

            STATUS = dictionary[Filename]

            URLs = self.get_URL_from_email(Content)
            Mail_Addresses = self.get_mail_adress_from_email(Content)
            Words = self.get_words_from_email(Content)


            self.add_URLs(URLs, STATUS)
            self.add_Mail_Addresses(Mail_Addresses, STATUS)
            self.add_Words(Words, STATUS)

        #print(len(self.Words), len(self.URLs), len(self.Mail_Addresses))



    def add_URLs(self, URLs, STATUS):
        for URL in URLs:
            IN_List = False
            for Item in self.URLs:
                if Item.Name == URL:
                    IN_List = True
                    if STATUS=='OK':
                        Item.OK+=1
                    elif STATUS=='SPAM':
                        Item.SPAM+=1
                    break

            if IN_List == False:
                New_URL = Data(URL)
                if STATUS == 'OK':
                    New_URL.OK += 1
                elif STATUS == 'SPAM':
                    New_URL.SPAM += 1
                self.URLs.append(New_URL)

    def add_Mail_Addresses(self, Mail_Addresses, STATUS):
        for Mail_Address in Mail_Addresses:
            IN_List = False
            for Item in self.URLs:
                if Item.Name == Mail_Address:
                    IN_List = True
                    if STATUS == 'OK':
                        Item.OK += 1
                    elif STATUS == 'SPAM':
                        Item.SPAM += 1
                    break

            if IN_List == False:
                New_Mail_Address = Data(Mail_Address)
                if STATUS == 'OK':
                    New_Mail_Address.OK += 1
                elif STATUS == 'SPAM':
                    New_Mail_Address.SPAM += 1
                self.Mail_Addresses.append(New_Mail_Address)

    def add_Words(self, Words, STATUS):
        for Word in Words:
            if Word not in self.Word_List:
                self.Word_List.append(Word)

            IN_List = False
            for Item in self.URLs:
                if Item.Name == Word:
                    IN_List = True
                    if STATUS == 'OK':
                        Item.OK += 1
                    elif STATUS == 'SPAM':
                        Item.SPAM += 1
                    break

            if IN_List == False:
                New_Word = Data(Word)
                if STATUS == 'OK':
                    New_Word.OK += 1
                elif STATUS == 'SPAM':
                    New_Word.SPAM += 1
                self.Words.append(New_Word)



    def test(self, path):
        Corpus_Obj = corpus.Corpus(path)

        Dictionary = {}

        for email in Corpus_Obj.emails():
            Filename = email[0]
            Content = email[1]

            URLs = self.get_URL_from_email(Content)
            Mail_Adresses = self.get_mail_adress_from_email(Content)
            Words = self.get_words_from_email(Content)

            Dictionary[Filename] = self.Eval(URLs,Mail_Adresses,Words)

        utils.write_classification_to_file(os.path.join(path,'!prediction2.txt'),Dictionary)



    def get_URL_from_email(self,email_content):
        return re.findall(r'\"(https?://\S+)\"', email_content)

    def get_mail_adress_from_email(self,email_content):
        return re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', email_content)

    def get_words_from_email(self, email_content):
        List = []
        All = email_content.split()
        if len(All)>self.Max_Words+100:
            All = All[100:self.Max_Words+100]

        for word in All:
            if word not in List:
                List.append(word)

        return List

    def Eval(self, URLs, Mail_Addresses, Words):
        OK = 0
        SPAM =0


        for URL in URLs:
            for Item in self.URLs:
                if Item.Name == URL:
                    if Item.OK/(Item.OK+Item.SPAM)>=self.Threshold:
                        OK += 1
                    else:
                        SPAM += 1
                    break

        for Mail_Address in Mail_Addresses:
            for Item in self.Mail_Addresses:
                if Item.Name == Mail_Address:
                    if Item.OK/(Item.OK+Item.SPAM)>=self.Threshold:
                        OK += 1
                    else:
                        SPAM += 1
                    break

        for Word in Words:
            if Word in self.Word_List:
                for Item in self.Words:
                    if Item.Name == Word:
                        if Item.OK/(Item.OK+Item.SPAM)>=self.Threshold:
                            OK += 1
                        else:
                            SPAM += 1
                        break

        return 'OK' if OK>SPAM else 'SPAM'


"""Obj = MyFilter()
print('Train')
Obj.train('2')
print('Test')
Obj.test('2')"""







