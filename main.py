import random


class Job:
    ...


class Home:
    __slots__ = ("mess", "food", "ecology")

    def __init__(self):
        self.mess = 0
        self.food = 0
        self.ecology = 0

class Car:
    ...


class Human:
    __slots__ = ("name", "money", "gladness", "satiety", "job", "home", "car")

    def __init__(self, name: str = "Human", job: Job = None, home: Home = None, car: Car = None):
        self.name = name
        self.money = 100
        self.gladness = 50
        self.satiety = 50
        self.job = job
        self.home = home
        self.car = car

    def get_home(self):
        self.home = Home()

    def get_food(self):
        if self.home.food < 0:
            self.shopping("food")
        elif self.satiety >= 100:
            self.satiety = 100
            return
        self.satiety += 5
        self.home.food -= 5
