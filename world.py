import numpy as np
import cv2
import matplotlib.pyplot as plt
import Creature
import time
import os

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

    def save_model(self, dir_path, max_n):
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        max_n = min(len(self.fishes), max_n)
        for i, fish in enumerate(self.fishes[:max_n]):
            np.save(os.path.join(dir_path,f'{i}'),fish.export_model())

    def loop(self):
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
                        children = fish.reproduce(7)
                    elif len(self.fishes) < 150:
                        children = fish.reproduce(3)
                    elif len(self.fishes) < 1000:
                    #else:
                        children = fish.reproduce(1)
                    
                    for child in children:
                        child.spawnAt(fish.x-2*fish.dx,fish.y-2*fish.dy)
                        self.fishes.append(child)
                    
                    break

            fish.smell(self.smell_map[fish.y+fish.dy*2,fish.x+fish.dx*2])
            fish.think()
            fish.move()
            
        # explicitly preventing from extinction
        the_last_fish = self.fishes[0]

        # kill condition
        for i in range(len(self.fishes)-1,-1,-1):
            if self.fishes[i].fullness < 0:
                self.fishes.pop(i)
        # wall condition
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

        # explicitly preventing from extinction
        if len(self.fishes) < 1:
            children = the_last_fish.reproduce(40)
            for child in children:
                child.spawnRandom(10,490,10,490)
            self.fishes += children

        # remove eaten foods, reproduce(duplicate) food
        if eaten_foods:
            eaten_foods.sort(reverse=True)
            for f_idx in eaten_foods:
                self.foods.pop(f_idx)

        any_new_food = False
        for food in self.foods:
            for i in range(food.reproduce()):
                any_new_food = True
                new_food = Creature.Food()
                new_food.spawnRandom(10,490,10,490)
                self.foods.append(new_food)

        if eaten_foods or any_new_food:
            self.food_idx_map = self.food_idx_map*0 - 1
            self.smell_map *= 0
            for i, food in enumerate(self.foods):
                self.food_idx_map[food.y,food.x] = i
                self.smell_map[food.y,food.x] = 1
            self.smell_map = cv2.GaussianBlur(self.smell_map,(255,255),40)
            self.smell_map *= (2*np.pi*40*40)



        # redraw world map
        self.world_map *= 0
        for fish in self.fishes:
            M = cv2.getRotationMatrix2D((2,2),fish.angle,1)
            img = cv2.warpAffine(self.fish_img,M,(5,5),flags=cv2.INTER_LINEAR)
            self.world_map[fish.y-2:fish.y+3,fish.x-2:fish.x+3] = img
        for food in self.foods:
            self.world_map[food.y-1:food.y+2,food.x-1:food.x+2] = self.food_img

        # show graphics
        cv2.imshow('map',self.world_map)
        out.write(cv2.cvtColor(self.world_map, cv2.COLOR_GRAY2BGR))
        cv2.imshow('smell',self.smell_map)

        return len(self.fishes), len(self.foods)

        
        

if __name__ == '__main__':
    np.random.seed(31415)

    lct = time.localtime()
    lct_str = '%4d%02d%02d%02d%02d'%(
        lct.tm_year,lct.tm_mon,lct.tm_mday,lct.tm_hour,lct.tm_min)

    myWorld = Biome()
    myWorld.setup()
    fr = 0

    video_savepath = os.path.join('Videos',f'fish_mung{lct_str}.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_savepath,fourcc,30.0,(500,500))
    fish_population = []
    food_population = []

    while cv2.waitKey(10) < 0:
        nfish, nfood = myWorld.loop()
        if nfish*nfood == 0:
            break
        fish_population.append(nfish)
        food_population.append(nfood)
        if fr > 10000 and fr%1000 == 0:
            myWorld.save_model(os.path.join('Model saves',lct_str),10)
        fr += 1
        print(f'\r{fr}', end='')

    out.release()

    plt.figure(figsize=(5,5))
    plt.plot(fish_population,label='fish population')
    plt.plot(food_population, label='food population')
    plt.legend()
    plt.show()


