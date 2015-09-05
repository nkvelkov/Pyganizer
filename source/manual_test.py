from task import Task
from event import Event
from arrow_encoder import ArrowEncoder, as_arrow
import json
import arrow
import icalendar
from icalendar import Calendar

a = arrow.Arrow(2015, 9, 5, 0, 25, 0, 0, tzinfo='local')

print(a)

current_moment = arrow.now()
print(current_moment)
print(current_moment > a)
print(a.to('utc'))
print(current_moment.to('utc'))
print(current_moment.to('utc') > a.to('utc'))

with open("pending_events.txt", "w") as d:
    d.truncate()
 

def get_id():
    result_id = 1  
    with open("work_files/task_id.txt", "r") as f:
        saved_id = f.readline()
        if saved_id.isnumeric():
            result_id = int(saved_id) + 1

    with open("work_files/task_id.txt", "w") as f:
        f.write(str(result_id))
    
    return result_id


print(get_id())
print(get_id())
print(get_id())
print(get_id())
print(get_id())
print(get_id())

a = arrow.utcnow().to('local')
cal = Calendar()
cal['summary'] = 'Calendar '
e = icalendar.Event()
e['uid'] = '32'
e.add('dtstart', a.naive)
e['dtend'] = 'dad'
cal.add_component(e)

print(cal.to_ical())

print(a.naive)
evt = Event(a, a, 2, 1, 2, 2)
e1 = Event(a, a, 2, 1, 22, 22)
t = Task(a, 2, 3, 4, 5, 6)
t1 = Task(a, 2, 3, 4, 52, 21)

with open('active_events.txt', "w") as f:
    f.write("{}\n".format(evt.encode()))
    f.write("{}\n".format(e1.encode()))

with open('active_events.txt', "r") as f:
    lines = f.readlines()
    for line in lines:
        e = Event.decode(line)
        print(e)
        print(type(e))

try:
    foo()
    print("bar")
except:
    raise



with open('active_tasks.txt', "w") as f:
    f.write("{}\n".format(t.encode()))
    f.write("{}\n".format(t1.encode()))

d = t.encode()
r = Task.decode(d)
print(r)
print(type(r))

k = evt.encode()
print(k)

o = Event.decode(k)
print(o)
print(type(o))

d = t.encode()
print(d)
print(type(d))

r = Task.decode(d)
print(r)
print(type(r))

print(k)
with open('active_events.txt', "w") as f:
    f.write("{}\n".format(k))


k = json.dumps(a, cls=ArrowEncoder)
print(k)
res = json.loads(k, object_hook=as_arrow)
print(res)
print(type(res))
class PyganizerError(Exception):
    def __init__(self):
        self.message = "PyganizeError"

class TodoNameExistsError(PyganizerError):
    def __init__(self):
        super().__init__()
        self.message = "TodoNameExistsError"

def foo():
    raise PyganizerError

cal = Calendar()
cal['dtstart'] = '20050404T080000'
cal.to_ical()
print(cal)

ss = set()


ss.add(evt)
ss.add(t)
print(ss)

class A:
    def __init__(self, l):
        self.l = l;

    def __del__(self):
        print("de")

class B(A):
    def __init__(self):
        super().__init__('b')

class C(A):
    def __init__(self):
        super().__init__('c')

b = B()
c = C()
print(b.l)
print(c.l)



with open("work_data", "w") as f:
    f.truncate()
            


print(a.tzinfo)
print(type(a))

k = json.dumps(a, cls=ArrowEncoder)
print(k)
res = json.loads(k, object_hook=as_arrow)
print(res)
print(type(res))

print("adfasdfasdfasdfasdf")

task = Task(a, 'n;', 'm', 2, 1, 20)
s = json.dumps(task, cls=TaskEncoder)
print(s)

a = arrow.utcnow().to('local')
# t = json.loads('{"__task__": true, "id": 3, "datetime": a, "name": "n", "message": "mes", "completeness": 2, "priority": 1}',
  #   object_hook=as_task)

# print(t)
# print(type(t))
print("tt folloing")
tt = json.loads(s, object_hook=as_task)
print(tt)
print(type(tt))
print(tt is Task)
# tt.pop('__task__')
# ta = Task(**tt)
# print(type(ta))
print("\n\n\n")
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
snake.greet
snake.greet() # 'My name issss Monty'
snake.name = 'Nagini'
# Python.greet() # TypeError: <lambda>() takes exactly 1 argument (0 given)
Python.greet(snake) # 'My name issss Nagini'

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


