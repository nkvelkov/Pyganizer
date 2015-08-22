import Qt
'''
import arrow
import threading
from pyganizer import Pyganizer
import time
import json
import sys
# import urwid
# from Tkinter import * 

# from lxml import etree

with open("test_data.txt", "w") as f:
    f.write("{} {}".format("asdf", "more and more asdf\n"))

with open("test_data.txt", "a") as f:
    f.write("{} {}".format("asdf", "more and more asdf\n"))

with open("test_data.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        print(line)

pygan = Pyganizer()

F = True

def foo():
    while F:
        time.sleep(1)
        print("foo")

# thread = threading.Thread(target=pygan.execute)
# thread.start()

# time.sleep(0.2)
# print("adsf")

# doc = etree.parse('test.xml')
# print(doc)

class Foo:
    def __init__(self, asdf):
        self.asdf = asdf

    def __str__(self):
        return self.asdf

foo = Foo("ASDF")
bar = Foo("adsf")

foo.friend = bar

l = [bar, foo]
print("asdf {}", l[0] is bar and foo is l[1])
l.pop(l.index(foo.friend))

print(str(l))

d = {(1, 1): '1', (2, 2): '2'}
print(d)
string = json.dumps(d)
print(string)

newd = json.loads(string)
print(newd)
'''
class MyMethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        print("get called {} {}".format(instance, owner))
        if instance:
            return lambda: self.func(instance)
        else:
            return lambda explicit_instance: self.func(explicit_instance)

class Python:
    name = 'Monty'
    greet = MyMethod(lambda self: 'My name issss %s' % self.name)

# Bound methods: Проста имплементация!

snake = Python()
snake.greet() # 'My name issss Monty'
snake.name = 'Nagini'
# Python.greet() # TypeError: <lambda>() takes exactly 1 argument (0 given)
Python.greet(snake) # 'My name issss Nagini'

'''
class B:
    def __get__(self, instance, owner):
        return "You came to the wrong neighborhood, motherflower!{}".format(owner)

    def __set__(self, instance, value):
        print("What!? You think you can change my personality just like that!?")

    def __delete__(self, instance):
        print("Can't touch me!")

class A:
    foo = B()

a = A()
print(a.foo)
a.foo = 'bar'
del a.foo
print(a.foo)

from contextlib import closing
from urllib.request import urlopen

class closing(object):
  def __init__(self, thing):
      self.thing = thing

  def __enter__(self):
      return self.thing

  def __exit__(self, type, value, traceback):
      self.thing.close()


with closing(urlopen('http://www.python.org')) as page:
    for line in page:
        print(line)
    print("asdf")
def fibonacci(x):
    print("foo ")
    if x in [0,1]:
        return 1
    return fibonacci(x-1) + fibonacci(x-2)

def memorize(func):
    memory = {}
    def memorized(*args):
        print("bar ")
        if args in memory:
            return memory[args]
        result = func(*args)
        memory[args] = result
        return result
    return memorized

fibonacci = memorize(fibonacci)

fibonacci(1)
print("adsf")
fibonacci(2)

def notifyme(f):
    def logged(*args, **kwargs):
        print(f.__name__, ' called with', args, 'and', kwargs)
        return f(*args, **kwargs)
    return logged

@notifyme
def square(x):
    return x * x

res = square(25)
print(res)

class GoatSimulator:
    goats = []
    count = 0

    @staticmethod
    def register(name):
        self.goats
        GoatSimulator.goats.append(name)
        print(len(GoatSimulator.goats), " goats are registered now")

class Countable:
    count = 0

    def __init__(self, data):
        self.data = data
        self.increase_count()

    @classmethod
    def increase_count(cls):
        cls.count += 1

    @classmethod
    def greet(cls, someone):
        print(someone, "was greeted from", cls)

    @classmethod
    def decrease_count(cls):
        cls.count -= 1

class Foo(Countable):
    def __init__(self, arg):
        self.arg = arg

c = Countable(3)
print(c.count)
cc = Countable(3)
print(c.count)
c.increase_count()
print(Foo.count)
class Battery(object):
    def __init__(self):
        self._voltage = 100000

    @classmethod
    def greet(cls, someone):
        print(someone, "was greeted from", cls)

    @property
    def voltage(self):
        print("""Get the current voltage.""")
        return self._voltage
# Това превръща voltage в getter към атрибут само за четене със същото име
b = Battery()
print(None is c.greet("asdf")) # 100000
'''


