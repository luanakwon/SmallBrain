import Biome
from Creature import Fish
import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
import os


if __name__ == '__main__':
    np.random.seed(31415)
    fish_pop = []
    food_pop = []

    myWorld = Biome.Biome(550)
    myWorld.setUp(30,400,400)

    while cv2.waitKey(5) < 0:
        myWorld.update()
        cv2.imshow('map',myWorld.map)
        cv2.imshow('smell',myWorld.smell_map/180)

        fish_pop.append(len(myWorld.fishes))
        food_pop.append(len(myWorld.foods))
        
        if len(myWorld.fishes) < 5:
            break

    # save brains
    fish_br_weights = []
    fish_br_cells = []
    for i, fish in enumerate(myWorld.fishes):
        if isinstance(fish,Fish) and  i < 20:
            fish_br_weights.append(fish.brain.brain_weight.copy())
            fish_br_cells.append(fish.brain.brain_cells.copy())
    fish_br_weights = np.array(fish_br_weights)
    fish_br_cells = np.array(fish_br_cells)

    lct = time.localtime()
    lct_str = '%4d%02d%02d%02d%02d'%(
        lct.tm_year,lct.tm_mon,lct.tm_mday,lct.tm_hour,lct.tm_min)
    dir_path = os.path.join('SmallBrain_v2','Model_saves',lct_str)
    os.makedirs(dir_path)
    np.save(os.path.join(dir_path,'weights'),fish_br_weights)
    np.save(os.path.join(dir_path,'cells'),fish_br_cells)

    plt.figure(figsize=(5,5))
    plt.plot(fish_pop,label='fish population')
    plt.plot(food_pop,label='food population')
    plt.legend()
    plt.show()
