

def is_start(p):
    if p.init_value==p.value:
        return True
    return False

class p:
    def __init__(self,value):
        self.value=value
        self.init_value=value

p1=p(5)
p2=p(10)

for p in [p1,p2]:
    p.value+=1

while not is_start(p):
    p.value+=1

while True:
    p.value+=1
    p.value+=1




