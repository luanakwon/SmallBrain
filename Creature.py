import numpy as np

class Fish():
    def __init__(self, brain_size):
        self.brain = np.random.normal(0,1,(brain_size,brain_size))
        self.cells = np.zeros((brain_size,1))

        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = -1
        self.angle = 90 

        self.fullness = 1

    def smell(self, intensity):
        self.cells[1] += intensity

    def eat(self, amount):
        self.cells[0] += amount
        self.fullness = 1
    
    def think(self):
        self.cells = np.matmul(self.brain,self.cells)
        self.cells = 1/(1+np.exp(-self.cells)) # sigmoid
    
    def move(self):
        left_v = self.cells[2]
        right_v = self.cells[3]

        # no move, less energy loss
        if left_v < 0.5 and right_v < 0.5:
            self.fullness -= 0.001
            self.cells[0] -= 0.1
        # move or turn. more energy loss
        else:
            self.fullness -= 0.002
            self.cells[0] -= 0.2
            # move forward
            if left_v > 0.5 and right_v > 0.5:
                self.x += self.dx
                self.y += self.dy
            else:
                # turn right
                if left_v > 0.5:
                    self.angle -= 45
                # turn left
                if right_v > 0.5:
                    self.angle += 45

                if self.angle < 0:
                    self.angle += 360
                self.dx = int(1.5*np.cos(self.angle*np.pi/180))
                self.dy = -int(1.5*np.sin(self.angle*np.pi/180))

    def spawnRandom(self, min_x, max_x, min_y, max_y):
        self.x = np.random.randint(min_x,max_x)
        self.y = np.random.randint(min_y,max_y)

    def spawnAt(self,xcor,ycor):
        self.x = xcor
        self.y = ycor

    def reproduce(self, n):
        children = []
        # child = Fish(0)
        # child.brain = self.brain.copy()
        # child.cells = self.cells.copy()
        # children.append(child)
        for i in range(n):
            child = Fish(0)
            child.brain = self.brain.copy()
            noise = np.random.normal(0,1,child.brain.shape)
            child.brain += noise*(noise < 0.4)*0.005
            child.cells = self.cells.copy()
            children.append(child)

        return children

class Food():
    def __init__(self):
        self.x = 0
        self.y = 0

    def spawnRandom(self, min_x, max_x, min_y, max_y):
        self.x = np.random.randint(min_x,max_x)
        self.y = np.random.randint(min_y,max_y)

    def spawnAt(self,xcor,ycor):
        self.x = xcor
        self.y = ycor
