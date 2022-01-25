import Biome
import cv2

if __name__ == '__main__':
    myWorld = Biome.Biome(400)
    myWorld.setUp(20,40,40)

    while cv2.waitKey(10) < 0:
        myWorld.update()
        cv2.imshow('map',myWorld.map)
