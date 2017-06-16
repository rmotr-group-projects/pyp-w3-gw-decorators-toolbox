# implement your decorators here.

def add(a,b):
    return a+b
    
def sub(a, b):
    return a-b

def check_only_ints(fn):
    def internal_func(a,b):
        if type(a) != int or type(b) != int:
            raise ValueError("Only ints allowed")
                
        return fn(a,b)
            
    return internal_func
    
    
add_only_ints = check_only_ints(add)

print(add_only_ints(2,3))
print(check_only_ints(add)(2,3)) # 
print(check_only_ints(add(2,3))) # == 5 << Wrong! 5(a,b)
print(check_only_ints

 
def internal_func(fn):
    if type(a) != int or type(b) != int:
        raise ValueError("Only ints allowed")
            
    return fn(a,b)
    
add = internal_func(add) # add(a,b)

add()



# ints_add = check_only_ints(add)
# def ints_add(a, b):
#     if type(a) != int or type(b) != int:
#         raise ValueError("Only ints allowed")
                
#     return add(a,b)
    
    
# type(ints_add) #function
# ints_add(2,3)
# check_only_int(add)(2,3)

# #add = check_only_ints(add)

# # print(check_only_ints(add(3,2)))
# # print(check_only_ints(5))
# # a = check_only_ints(5)
# # a(2,3)
# #print(add(3,2))