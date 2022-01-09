import numpy as np
import cv2
import Creature

class Biome():
    def __init__(self):
        self.fishes = []
        self.foods = []
        self.world_map = np.zeros((500,500),dtype=np.uint8)
        self.smell_map = np.zeros((500,500),dtype=np.float32)
        self.food_idx_map = np.ones((500,500),dtype=np.int32)*-1

        self.fish_img = np.uint8(
            [[1,1,1,0,0],
            [0,1,1,1,0],
            [0,0,1,1,1],
            [0,1,1,1,0],
            [1,1,1,0,0]]
        )*255

        self.food_img = np.uint8(
            [[0,1,0],
            [1,1,1],
            [0,1,0]]
        )*255

    def setup(self):
        for i in range(200):
            self.fishes.append(Creature.Fish(20))
        for fish in self.fishes:
            fish.spawnRandom(10,490,10,490)
            M = cv2.getRotationMatrix2D((2,2),fish.angle,1)
            img = cv2.warpAffine(self.fish_img,M,(5,5),flags=cv2.INTER_LINEAR)
            self.world_map[fish.y-2:fish.y+3,fish.x-2:fish.x+3] = img

        for i in range(70):
            self.foods.append(Creature.Food())
        for i, food in enumerate(self.foods):
            food.spawnRandom(10,490,10,490)
            self.world_map[food.y-1:food.y+2,food.x-1:food.x+2] = self.food_img
            self.food_idx_map[food.y,food.x] = i
            self.smell_map[food.y,food.x] = 1
            
        self.smell_map = cv2.GaussianBlur(self.smell_map,(255,255),40)
        self.smell_map *= (2*np.pi*40*40)


        cv2.imshow('smell',self.smell_map)
        cv2.waitKey()


    def loop(self):
        new_foods = []
        eaten_foods = []
        for fn, fish in enumerate(self.fishes):
            # eat if possible
            nearby_foods = self.food_idx_map[fish.y-3:fish.y+4,fish.x-3:fish.x+4].flatten()
            for i in nearby_foods:
                if 0 <= i and i < len(self.foods) and i not in eaten_foods:
                    food = self.foods[i]
                    fish.eat(1)
                    self.food_idx_map[food.y,food.x] = -1
                    eaten_foods.append(i)

                    # print(f'({fish.y},{fish.x}) nice taste ({food.y},{food.x})')
                    print(f'# fish = {len(self.fishes)}, # food = {len(self.foods)}')
                    children = []
                    if len(self.fishes) < 50:
                        children = fish.reproduce(10)
                    elif len(self.fishes) < 150:
                        children = fish.reproduce(7)
                    elif len(self.fishes) < 300:
                        children = fish.reproduce(1)
                    
                    for child in children:
                        child.spawnAt(fish.x,fish.y)
                        self.fishes.append(child)

                    new_food = Creature.Food()
                    new_food.spawnRandom(10,490,10,490)
                    new_foods.append(new_food)

                    break

            fish.smell(self.smell_map[fish.y+fish.dy*2,fish.x+fish.dx*2])
            fish.think()
            fish.move()
            
        for i in range(len(self.fishes)-1,-1,-1):
            # kill condition
            if self.fishes[i].fullness < 0:
                self.fishes.pop(i)
        for fish in self.fishes:
            if fish.x > 490 and fish.dx > 0:
                fish.angle = 180 - fish.angle
                fish.dx *= -1
            elif fish.x < 10 and fish.dx < 0:
                fish.angle = 180 - fish.angle
                fish.dx *= -1
            if fish.y > 490 and fish.dy > 0:
                fish.angle = 360 - fish.angle
                fish.dy *= -1
            elif fish.y < 10 and fish.dy < 0:
                fish.angle = 360 - fish.angle
                fish.dy *= -1

        if eaten_foods:
            eaten_foods.sort(reverse=True)
            for f_idx in eaten_foods:
                self.foods.pop(f_idx)

        if new_foods:
            self.foods = self.foods + new_foods
            self.food_idx_map = self.food_idx_map*0 - 1
            self.smell_map *= 0
            for i, food in enumerate(self.foods):
                self.food_idx_map[food.y,food.x] = i
                self.smell_map[food.y,food.x] = 1
            self.smell_map = cv2.GaussianBlur(self.smell_map,(255,255),40)
            self.smell_map *= (2*np.pi*40*40)



        # print(np.max(self.smell_map))
        
            
        self.world_map *= 0
        for fish in self.fishes:
            M = cv2.getRotationMatrix2D((2,2),fish.angle,1)
            img = cv2.warpAffine(self.fish_img,M,(5,5),flags=cv2.INTER_LINEAR)
            self.world_map[fish.y-2:fish.y+3,fish.x-2:fish.x+3] = img
        for food in self.foods:
            self.world_map[food.y-1:food.y+2,food.x-1:food.x+2] = self.food_img

        cv2.imshow('map',self.world_map)
        cv2.imshow('smell',self.smell_map)

        
        

if __name__ == '__main__':
    myWorld = Biome()
    myWorld.setup()
    fr = 0
    while cv2.waitKey(33) < 0:
        myWorld.loop()
        fr += 1
        print(f'\r{fr}', end='')


