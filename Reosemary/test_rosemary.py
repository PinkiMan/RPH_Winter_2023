
from rosemary import Item, update















def test_Name_Change_Bread():
    for i in range(10,-10,-1):
        item = Item('Bread', days_left=i, quality=5)
        update(item)
        if item.name!='Bread':
            return False

    return True

def test_Quality_Radius_Bread():
    for i in range(10, -10, -1):
        item = Item('Bread', days_left=i, quality=5)
        update(item)
        if (item.quality != 4 and i>0) or (i<=0 and item.quality != 3):
            return False

    return True

def test_Quality_Radius_Bread_Second():
    for i in range(50, -1, -1):
        item = Item('Bread', days_left=3, quality=i)
        update(item)
        if (item.quality!=i-1 and i>0) or (i==0 and item.quality!=0):
            return False

    return True

def test_Day_Change_Bread():
    for i in range(10, -10, -1):
        item = Item('Bread', days_left=i, quality=5)
        update(item)
        if item.days_left != i-1:
            return False

    return True








def test_Name_Change_Aged_Brie():
    for i in range(10,-10,-1):
        item = Item('Aged Brie', days_left=i, quality=5)
        update(item)
        if item.name!='Aged Brie':
            return False

    return True

def test_Quality_Radius_Aged_Brie():
    for i in range(10, -10, -1):
        item = Item('Aged Brie', days_left=i, quality=5)
        update(item)
        if item.quality != 6:
            return False

    return True

def test_Quality_Radius_Aged_Brie_Second():
    for i in range(50, -1, -1):
        item = Item('Aged Brie', days_left=3, quality=i)
        update(item)
        if (item.quality!=i+1 and i<50) or (i==50 and item.quality!=50):
            return False

    return True

def test_Quality_Radius_Aged_Brie_best():
    for i in range(10, -10, -1):
        item = Item('Aged Brie', days_left=i, quality=5)
        update(item)
        if item.days_left != i-1:
            return False

    return True








def test_Name_Change_Diamond():
    item = Item('Diamond', days_left=3, quality=5)
    update(item)

    return item.name=='Diamond'

def test_Quality_Radius_Diamond():
    item = Item('Diamond', days_left=3, quality=100)
    update(item)

    return item.quality==100

def test_Quality_Radius_Diamond():
    item = Item('Diamond', days_left=0, quality=100)
    update(item)

    return item.quality==100

def test_Day_Change_Diamond():
    item = Item('Diamond', days_left=0, quality=100)
    update(item)

    return item.days_left==0








def test_Name_Change_Tickets():
    for i in range(10,-10,-1):
        item = Item('Tickets', days_left=i, quality=5)
        update(item)
        if item.name!='Tickets':
            return False

    return True

def test_Quality_Radius_Tickets_far():
    for i in range(20, 10, -1):
        item = Item('Tickets', days_left=i, quality=5)
        update(item)
        if item.quality != 6:
            return False

    return True



def test_Quality_Radius_Tickets_mid():
    for i in range(10, 5, -1):
        item = Item('Tickets', days_left=i, quality=5)
        update(item)
        if item.quality != 7:
            return False

    return True


def test_Quality_Radius_Tickets_low():
    for i in range(5, 0, -1):
        item = Item('Tickets', days_left=i, quality=5)
        update(item)
        if item.quality != 8:
            return False

    return True



def test_Quality_Radius_Tickets_now():
    for i in range(0, -10, -1):
        item = Item('Tickets', days_left=i, quality=5)
        update(item)
        if item.quality != 0:
            return False

    return True


def test_Quality_Radius_Tickets_second():
    for i in range(50, -1, -1):
        item = Item('Tickets', days_left=15, quality=i)
        update(item)
        if (item.quality != i + 1 and i < 50) or (i == 50 and item.quality != 50):
            return False

    return True


