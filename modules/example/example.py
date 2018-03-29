def init():  # init will be run on module load if it exists
    pass


def main():
    '''This is an example function.'''
    print("example.main started!")


def error(err):
    '''This function errors out with an error of your choosing. When passing a string as an argument, use quotes.'''
    return err


def test(x, y):
    '''This function prints two arguments.'''
    print("example.test started!")
    print("Arguments passed:", x, y)


def test2(*x):
    '''This function prints a dynamic amount of arguments.'''
    print("example.test2 started!")
    print("Argument(s) passed:", x)
