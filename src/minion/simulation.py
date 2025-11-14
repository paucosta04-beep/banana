import random

def say_hi(name="caracol"):
    coin = random.random() > 0.5
    if coin:
        print("hi", name)
    else:
        print("bye", name)

def count_to_ten():
    for i in range(1, 11):
        print(i)
