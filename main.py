import random
from typing import Literal


class NotEnoughMoney(Exception):
    ...


class Present(Exception):
    ...


class Broke(Exception):
    ...


class Job:
    __slots__ = ("worker", "gain", "time")

    def __init__(self, worker):
        self.worker = worker
        self.gain = 100
        self.time = 8

    def work(self):
        self.worker.satiety -= random.randint(20, 30)
        if self.worker.satiety < 1:
            self.worker.satiety = 1
        self.worker.money += self.gain
        self.gain += random.randint(1, 5)
        return self.worker


class Home:
    __slots__ = ("mess", "food", "ecology", "owner", "people")

    def __init__(self, owner):
        self.mess = 0
        self.food = 0
        self.ecology = 0
        self.owner = owner
        self.people = [owner]


class Car:
    __slots__ = ("color", "durability", "owner")

    def __init__(self, owner, color=random.choice(["red", "green", "blue"])):
        self.color = color
        self.durability = 200
        self.owner = owner

    def repair(self):
        if self.owner.money > 40:
            self.durability += random.randint(15, 30)
            self.owner.money -= 40
            return self
        raise NotEnoughMoney(f"You do not have enough money to repair your car. "
                             f"You have {self.owner.money} and you need more than 40")

    def ride(self):
        if self.durability < 1:
            self.owner.car = None
            raise Broke("Your car is broken! buy a new one")
        self.durability -= random.randint(2, 4)
        self.owner.satiety -= random.randint(1, 2)
        if self.owner.satiety < 1:
            self.owner.satiety = 1
        return self

    def paint(self, color: Literal["red", "green", "blue"]):
        if self.owner.money > 30:
            self.color = color
            self.owner.money -= 30
            return self
        raise NotEnoughMoney(f"You do not have enough money to buy a home."
                             f" You have {self.owner.money} and you need more than 30")


class Bicycle:
    __slots__ = ("color", "durability", "owner")

    def __init__(self, owner, color=random.choice(["red", "green", "blue"])):
        self.color = color
        self.durability = 100
        self.owner = owner

    def ride(self):
        if self.durability < 1:
            self.owner.bicycle = None
            raise Broke("Your bicycle is broken! buy a new one")
        self.durability -= random.randint(1, 3)
        self.owner.satiety -= random.randint(3, 4)
        if self.owner.satiety < 1:
            self.owner.satiety = 1
        return self

    def paint(self, color: Literal["red", "green", "blue"]):
        if self.owner.money > 10:
            self.color = color
            self.owner.money -= 10
            self.owner.satiety -= random.randint(4, 6)
            if self.owner.satiety < 1:
                self.owner.satiety = 1
            return self
        raise NotEnoughMoney(f"You do not have enough money to paint your car. "
                             f"You have {self.owner.money} and you need more than 10")


class Human:
    __slots__ = ("name", "money", "gladness", "satiety", "job", "home", "car", "bicycle")

    def __init__(self, name: str = "Human", job: Job = None,
                 home: Home = None, car: Car = None, bicycle: Bicycle = None):
        self.name = name
        self.money = 100
        self.gladness = 50
        self.satiety = 100
        self.job = job
        self.home = home
        self.car = car
        self.bicycle = bicycle

    def shopping(self, what: Literal["food"]):
        prices = {"food": {"price": 5, "gives": ("home.food", 10)}}
        if self.money > prices[what]["price"]:
            self.money -= prices[what]["price"]
            self.__setattr__(prices[what]["gives"][0], prices[what]["gives"][1])
            return self
        raise NotEnoughMoney(f"You do not have enough money to buy {what} "
                             f"You have {self.money} and you need more than {prices[what]['price']}")

    def get_home(self):
        if self.home is not None:
            raise Present(f"You already have a home")
        if self.money > 50:
            self.home = Home(self)
            self.money -= 50
            return self.home
        raise NotEnoughMoney(f"You do not have enough money to buy a home. "
                             f"You have {self.money} and you need more than 50")

    def get_food(self):
        if self.home.food < 0:
            self.shopping("food")
        elif self.satiety >= 100:
            self.satiety = 100
            raise Present("You are not hungry")
        self.satiety += 5
        self.home.food -= 5
        if self.satiety >= 100:
            self.satiety = 100
        if self.home.food < 100:
            self.satiety = 100
        return self.satiety

    def get_bicycle(self):
        if self.bicycle is not None:
            raise Present(f"You already have a bicycle")
        if self.money > 20:
            self.bicycle = Bicycle(self)
            self.money -= 20
            return self.bicycle
        raise NotEnoughMoney(f"You do not have enough money to buy a bicycle. "
                             f"You have {self.money} and you need  more than 20")

    def get_car(self):
        if self.car is not None:
            raise Present(f"You already have a car")
        if self.money > 100:
            self.car = Car(self)
            self.money -= 100
            return self.car
        raise NotEnoughMoney(f"You do not have enough money to buy a car. "
                             f"You have {self.money} and you need more than 100")

    def get_job(self):
        self.job = Job(self)


me = Human()
me.money = 9999
my_car = me.get_car()
my_car.ride()