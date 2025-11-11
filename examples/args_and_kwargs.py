
def test(a, b, *args, **kwargs):
    print(a)
    print(b)
    print(args)
    print(kwargs)


test(10, 20, 1, 2, 3, 4, age=45, country='USA', type='package')