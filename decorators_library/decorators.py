# implement your decorators here.
def inspect(func):
   
  def func_wrapper(*args):
    print ("my_add invoked with {}. Result: {}".format(str(args)[1:-1],func(*args)))
  return func_wrapper  
  
@inspect
def my_add(a, b):
    return a + b
