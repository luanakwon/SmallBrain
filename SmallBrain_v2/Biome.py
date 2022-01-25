import numpy as np
import cv2
from Creature import Fish, Food
from utils import draw

class Biome():
    def __init__(self, world_size):
        self.world_size = world_size

        self.map = np.zeros((world_size,world_size))
        self.smell_map = np.zeros_like(self.map)

        self.fishes = []
        self.foods = []

    def add_fish(self, brain_size, n):
        for i in range(n):
            fish = Fish(brain_size)
            fish.spawnRandom(5,self.world_size-5,5,self.world_size-5)
            self.fishes.append(fish)

    def add_food(self, n):
        for i in range(n):
            food = Food()
            food.spawnRandom(5,self.world_size-5,5,self.world_size-5)
            self.foods.append(food)

    def update_smell_map(self):
        self.smell_map *= 0
        for food in self.foods:
            draw(self.smell_map,Food.smell_img,food.x,food.y,strategy='add')

    def update_map(self):
        self.map *= 0
        for fish in self.fishes:
            if fish.angle == 1:
                img = cv2.rotate(Fish.img,cv2.ROTATE_90_COUNTERCLOCKWISE)
            elif fish.angle == 2:
                img = cv2.rotate(Fish.img,cv2.ROTATE_180)
            elif fish.angle == 3:
                img = cv2.rotate(Fish.img,cv2.ROTATE_90_CLOCKWISE)
            else:
                img = Fish.img
            draw(self.map,img,fish.x,fish.y)
        for food in self.foods:
            draw(self.map,Food.img,food.x,food.y)

    def setUp(self, brain_size, fish_n, food_n):
        self.add_fish(brain_size,fish_n)
        self.add_food(food_n)
        self.update_map()
        self.update_smell_map()
        cv2.imshow('map',self.map)
        cv2.imshow('smell',self.smell_map/np.max(self.smell_map))
        cv2.waitKey()

    def update(self):
        for fish in self.fishes:
            dx, dy = Fish.angle2v[fish.angle]
            intensity = self.smell_map[fish.y+dy*2,fish.x+dx*2]
            fish.smell(intensity)
            if intensity >= 180:
                fish.eat()
            fish.think()
            fish.move()
        
        # wall condition
        for fish in self.fishes:
            if fish.x > self.world_size-5 and fish.angle == 0:
                fish.angle = 2
            elif fish.x < 5 and fish.angle == 2:
                fish.angle = 0
            if fish.y > self.world_size-5 and fish.angle == 3:
                fish.angle = 1
            elif fish.y < 5 and fish.angle == 1:
                fish.angle = 3

        self.update_map()