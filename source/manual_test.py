import arrow
import threading
from pyganizer import Pyganizer
import time
import json
import sys
# import urwid
# from Tkinter import * 
# from PyQt4 import Qt
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

time.sleep(0.2)
print("adsf")

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




