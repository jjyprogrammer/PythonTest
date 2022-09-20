
def removeSameValue(list1,list2):
    print("removeSameValue")  
    for j in list2:
        for i in list1:        
            if(i == j):
                list1.remove(i)
    return list1


list1 = [1, 2, 3, 4, 5];
list2 = [2, 3, 4, 5];

removeSameValue(list1, list2)

print(list1);