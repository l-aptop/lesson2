import random


class Job:
    ...


class Home:
    ...


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
