#! /usr/bin/python


class Base1(object):
    @classmethod
    def func_base(cls):
        print("base 1")
        super(Base1, cls).func_base()


class Base2(object):
    @classmethod
    def func_base(cls):
        print("base 2")


class Test(Base1, Base2):
    def print_test(self):
        print('Test')


test_instance = Test()

test_instance.func_base()

