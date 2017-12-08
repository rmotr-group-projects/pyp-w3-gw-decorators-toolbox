# implement your decorators here.


def inspect(fn):

    if fn.__name__ == 'my_add':

        def Ifn(x, y):

            print("my_add invoked with {}, {}. Result: {}".format(x, y, fn(x, y)))
            return fn(x, y)

        return Ifn

    elif fn.__name__ == 'calculate':

        def Ifn(*args, operation='add'):

            inputs = ", ".join(str(x) for x in args)

            if operation == "add":

                print("calculate invoked with {}. Result: {}".format(inputs, fn(*args, operation)))
                return fn(*args, operation)

            else:

                print("calculate invoked with {}, operation={}. Result: {}".format(inputs, operation, fn(*args, operation='subtract')))

                return fn(*args, operation)

        return Ifn
