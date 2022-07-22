import pandas as pd

class Action():
    def printSomething(self):
        print("hello world")

class Obt():
    def __init__(self):
        self.name = None

    def setName(self, data):
        self.name = data

if __name__ == '__main__':
    act = Action()
    widget = Obt()

    widget.setName(act.printSomething)
    widget.name()