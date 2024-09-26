import numpy as np
import cv2
from utils import getInverseSquareMat

'''
Brain class
'''
class Brain():
    def __init__(self, input_size, output_size, brain_size):
        self.input_size = input_size
        self.output_size = output_size
        self.brain_size = brain_size

        self.brain_weight = \
            np.random.normal(0,1,(input_size+brain_size,brain_size+output_size))
        self.input_cells = np.zeros((1,input_size))
        self.brain_cells = np.zeros((1,brain_size))
        self.output_cells = np.zeros((1,output_size))

    def think(self):
        brain_in = np.concatenate((self.input_cells,self.brain_cells),axis=1)
        brain_out = np.matmul(brain_in,self.brain_weight) # FC layer
        brain_out[brain_out<-500] = -500 # exp overflows from 710
        brain_out = 1/(1+np.exp(-brain_out)) # sigmoid activation func
        # brain_out = brain_out[brain_out>0] # relu
        self.brain_cells = brain_out[:,:self.brain_size].copy()
        self.output_cells = brain_out[:,self.brain_size:].copy()
        self.input_cells *= 0 # reset input cells

    def copy_with_noise(self):
        new_brain = Brain(self.input_size,self.output_size,self.brain_size)
        new_brain.brain_weight *= 0.005
        new_brain.brain_weight += self.brain_weight
        new_brain.brain_cells *= 0.005
        new_brain.brain_cells += self.brain_cells

        return new_brain
        

'''
Fish class
can smell, eat, feel hunger(and fullness)
can move forward, turn 90 degree
cycle : smell-eat-think(use input and reset)-move-touch
'''
class Fish():
    angle2v = {0:(1,0),1:(0,-1),2:(-1,0),3:(0,1)}
    
    img = np.array([
        [1,1,1,0,0],
        [0,1,1,1,0],
        [0,0,1,1,1],
        [0,1,1,1,0],
        [1,1,1,0,0]
    ],dtype=np.uint8)*255

    def __init__(self, brain_size):
        # input : smell, fullness, touch(front/back/left/right)
        # output : left, right
        self.brain = Brain(6,2,brain_size)
        
        self.life = 1
        self.smell_intensity = 0
        self.fullness = 0

        self.x = 0
        self.y = 0
        self.angle = 0
        
    def smell(self,intensity):
        self.smell_intensity = intensity

    def eat(self):
        self.life = 1
        self.fullness = 10

    def senseTouch(self, side):
        if side == 'front':
            self.brain.input_cells[0,2] = 1
        elif side == 'back':
            self.brain.input_cells[0,3] = 1
        elif side == 'left':
            self.brain.input_cells[0,4] = 1
        elif side == 'right':
            self.brain.input_cells[0,5] = 1
    
    def think(self):
        self.brain.input_cells[0,0] = self.smell_intensity
        self.brain.input_cells[0,1] = self.fullness
        self.brain.think()

    def move(self):
        left, right = self.brain.output_cells[0,:] > 0.5
        if left and right:
            dx, dy = Fish.angle2v[self.angle]
            self.x += dx
            self.y += dy
            self.fullness = -1
            self.life -= 0.003
        elif left:
            self.angle = (self.angle+1)%4
            self.fullness = -1
            self.life -= 0.002
        elif right:
            self.angle = (self.angle+3)%4
            self.fullness = -1
            self.life -= 0.002
        else:
            self.fullness = -0.1
            self.life -= 0.001
            
    def reproduce(self):
        child = Fish(self.brain.brain_size)
        child.brain = self.brain.copy_with_noise()
        child.life = 1
        dx, dy = Fish.angle2v[child.angle]
        child.x += dx
        child.y += dy

        return child

    def spawnRandom(self, min_x, max_x, min_y, max_y):
        self.x = np.random.randint(min_x,max_x)
        self.y = np.random.randint(min_y,max_y)

    def spawnAt(self,xcor,ycor):
        self.x = xcor
        self.y = ycor

class Food():
    img = np.array([
        [0,1,0],
        [1,1,1],
        [0,1,0]
    ],dtype=np.uint8)*255

    smell_max = 97
    smell_img = getInverseSquareMat(149,10000,100,smell_max)

    def __init__(self):
        self.x = 0
        self.y = 0
        self.age = 0

    def reproduce(self):
        if self.age > 200:
            self.age = 0
            return 1
        else:
            self.age += 1
            return 0

    def spawnRandom(self, min_x, max_x, min_y, max_y):
        self.x = np.random.randint(min_x,max_x)
        self.y = np.random.randint(min_y,max_y)

    def spawnAt(self,xcor,ycor):
        self.x = xcor
        self.y = ycor


        

        