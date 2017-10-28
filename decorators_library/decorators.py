def inspect(func):
  def func_wrapper(*args, **kwargs):
    kwargs_str = ""
    for kw in kwargs.keys():
           kwargs_str = ", " + ( kw+'='+str( kwargs[kw] ) )
    arg_str = str(args)[1:-1] + kwargs_str
    print ("{} invoked with {}. Result: {}".format(func.__name__, arg_str, func(*args,**kwargs)))
    return func(*args,**kwargs)
  return func_wrapper  
