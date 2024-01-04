
import os


class Corpus:
    def __init__(self,Directory):
        self.Directory = Directory

    def emails(self):
        Dir = os.listdir(self.Directory)

        for File in Dir:
            if '!' != File[0]:
                Filepath=os.path.join(self.Directory,File)
                with open(Filepath, 'r', encoding='utf-8') as FILE:
                    text = FILE.read()

                yield File,text
            else:
                pass


