

class MyVector:
    def __init__(self, vector):
        self.vector=[]
        if type(vector)==list:
            self.vector=vector

    def get_vector(self):
        return self.vector

    def __mul__(self, other):
        scalar=0
        for i in range(len(self.vector)):
            scalar+=self.vector[i]*other.vector[i]

        return scalar






if __name__ == "__main__":
    vec1 = MyVector([1,2,3]) # vektory mohou byt i jine dimenze nez 3!
    vec2 = MyVector([3,4,5])
    print(vec1.get_vector()) # priklad ziskani seznamu
    dot_product = vec1*vec2  # vypocet skalarniho soucinu, pretizeny operator *, vola se __mul__
    print(dot_product)       # jen kontrolni vypis

