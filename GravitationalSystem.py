import math
import pygame

def sign(x):
    if x >= 0:
        return 1.
    else:
        return -1.

class object:
    def __init__(self, name, mass, x0, y0, v0x, v0y):
        self.forExport = None

        self.name = name
        self.mass = mass

        self.XPos = x0
        self.YPos = y0

        self.vX = v0x
        self.vY = v0y

        self.forceX = 0
        self.forceY = 0

        #to be reset
        self.maxForce = 0
        self.minForce = 10 ** 99
        self.avgForce = 0

        self.maxVelocity = -999
        self.minVelocity = 10 ** 99
        self.avgVelocity = 0

        self.minDistanceFromSun = 10 ** 1000
        self.maxDistanceFromSun = 0
        self.avgDistanceFromSun = 0

    def resetForces(self):
        self.forceX = 0
        self.forceY = 0

    def getVelocityX(self):
        return self.vX

    def getVelocityY(self):
        return self.vY

class system:
    def __init__(self, timeInterval, endTimeYears):
        self.grid = []
        self.g = 6.67 * 10 ** -11
        self.timeInterval = timeInterval #should be in seconds
        self.endTimeSecs = endTimeYears * 365 * 24 * 60 * 60 #put in in years, converted to seconds
        self.forExport = open("System.csv","w")
        self.forExport.write("Object" + " ," + "Max distance from sun" + " ," + "Min distace from sun" + " ," + "Avg distance from sun" + " ," + "Max vel" + " ," + "Min vel" + " ," + "Avg vel" + " ," + "Max acceleration" + " ," + "Min acceleration" + "Avg acceleration" + "\n")

    def addObject(self, toAdd):
        self.grid.append(toAdd)
        # toAdd.forExport = open(str(toAdd.name) + ".csv","w")
        # toAdd.forExport.write("XForce" + " ," + "YForce" + " ," + "time (seconds)" + ', ' + "x(t)" + ', ' + "y(t)" + ', ' + "vX(t)" + ', ' + "vY(t)" + ', ' + "v(t)" + '\n')

    def calcKinematic(self):
        #without planetX
        for run in range(int(self.endTimeSecs / self.timeInterval)):
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.updateForces()
        #calculate velocities, update position values
            screen.fill((255, 255, 255))
            for obj in self.grid:
                #xf = Vit + 1/2at^2 + xi
                xNow = obj.getVelocityX() * self.timeInterval + (1.0/2) * obj.forceX/obj.mass * self.timeInterval ** 2 + obj.XPos
                yNow = obj.getVelocityY() * self.timeInterval + (1.0/2) * obj.forceY/obj.mass * self.timeInterval ** 2 + obj.YPos

                rad = math.sqrt(xNow ** 2 + yNow **2)
                if( rad > obj.maxDistanceFromSun):
                    obj.maxDistanceFromSun = rad
                if( rad < obj.minDistanceFromSun):
                    obj.minDistanceFromSun = rad
                obj.avgDistanceFromSun += rad

                #V = Vi + at
                newVx = obj.getVelocityX() + obj.forceX/obj.mass * self.timeInterval
                newVy = obj.getVelocityY() + obj.forceY/obj.mass * self.timeInterval

                obj.vX = newVx
                obj.vY = newVy

                vel = math.sqrt(obj.vX ** 2 + obj.vY ** 2) #* sign(obj.vX) * sign(obj.vY)
                if(vel < obj.minVelocity):
                    obj.minVelocity = vel
                if(vel > obj.maxVelocity):
                    obj.maxVelocity = vel
                obj.avgVelocity += vel

                obj.XPos = xNow
                obj.YPos = yNow

                # obj.forExport.write(str(run * self.timeInterval) + ', ' + str(obj.XPos) + ', ' + str(obj.YPos) + ', ' + str(obj.getVelocityX()) + ', ' + str(obj.getVelocityY()) + "\n")

                pygame.draw.ellipse(screen, (0,0,0), [250 + xNow/(10 ** 11 * .3), 250 + yNow/(10 ** 11 * .3), obj.mass**(1/25), obj.mass**(1/25)],0)

                if((1.0 * run * self.timeInterval/self.endTimeSecs * 100)%1 <= .001):
                    print(str(1.0 * run * self.timeInterval/self.endTimeSecs * 100) + "% done")

        # for obj in self.grid:
        #     print(str(obj.name) + ":" + "Max acceleration: " + str(obj.maxForce/obj.mass) + ", Min acceleration: " + str(obj.minForce/obj.mass) + " ,Avg accel: " + str(obj.avgForce/(self.endTimeSecs/self.timeInterval)/obj.mass) + " ,Max velocity: " + str(obj.maxVelocity) + " ,Min velocity: " + str(obj.minVelocity) + ", Avg velocity: " + str(obj.avgVelocity/(self.endTimeSecs/self.timeInterval)) + '\n')
        #

        for obj in self.grid:
            self.forExport.write(str(obj.name) + " ," + str(obj.maxDistanceFromSun) + " ," + str(obj.minDistanceFromSun) + " ," + str(obj.avgDistanceFromSun/(self.endTimeSecs/self.timeInterval)) + " ," + str(obj.maxVelocity) + " ," + str(obj.minVelocity) + " ," + str(obj.avgVelocity/(self.endTimeSecs/self.timeInterval)) + " ," + str(obj.maxForce/obj.mass) + " ," + str(obj.minForce/obj.mass) + " ," +  str(obj.avgForce/(self.endTimeSecs/self.timeInterval)/obj.mass) + "\n")

        pygame.display.flip()

        if(len(self.grid) == 9):
            planetX = object("PlanetX", 5.972 * 10 ** 24 * 10, 4.495 * 10 ** 12 * 20, 0, 0, 6)
            self.grid.append(planetX)
            self.forExport.write("\n" + "\n")
            self.calcKinematic()

    def updateForces(self):#need to reset forces for changing radii
        for obj in self.grid:
            obj.resetForces()

        force = 0 #to be reset

        for this in range(len(self.grid)):
            for next in range(this + 1, len(self.grid)):
                obj = self.grid[this]
                other = self.grid[next]

                radius = math.sqrt((obj.XPos - other.XPos) ** 2 + (obj.YPos - other.YPos) ** 2)
                force = (self.g * obj.mass * other.mass)/(radius ** 2)

            #split force into components
                angle = math.atan((obj.YPos - other.YPos)/(obj.XPos - other.XPos))
                magXForce = abs(math.cos(angle)) * force
                magYForce = abs(math.sin(angle)) * force

            #assign signs to vectors
                if(obj.XPos > other.XPos):#obj is farther "right"
                    obj.forceX += -magXForce
                    other.forceX += magXForce
                else:
                    obj.forceX += magXForce
                    other.forceX += -magXForce

                if(obj.YPos > other.YPos):#obj is farther "up"
                    obj.forceY += -magYForce
                    other.forceY += magYForce
                else:
                    obj.forceY += magYForce
                    other.forceY += -magYForce

        # for obj in self.grid:
        #     obj.forExport.write(str(obj.forceX) + "," + str(obj.forceY) + ",")

        for obj in self.grid:
                if(force < obj.minForce):
                    obj.minForce = force
                if(force > obj.maxForce):
                    obj.maxForce = force
                obj.avgForce += abs(force)

pygame.init()

screen = pygame.display.set_mode((500,500))
def main():
    #timeInterval, endTimeYears
    sys = system((60 * 60), 169)

    #name, mass, x0, y0, v0x, v0y
    sun = object("Sun", 1.989 * 10 ** 30, 0, 0, 0, 0)
    mercury = object("Mercury", 3.285 * 10 ** 23, 5.971 * 10 ** 10, 0, 0, 47400)
    venus = object("Venus", 4.867 * 10 ** 24, 1.082 * 10 ** 11,0, 0, 35000)
    earth = object("Earth", 5.972 * 10 ** 24, 1.496 * 10 ** 11, 0, 0, 30000)
    mars = object("Mars", 6.39 * 10 ** 23, 2.279 * 10 ** 11, 0, 0, 24100)
    jupiter = object("Jupiter", 1.898 * 10 ** 27, 7.785 * 10 ** 11, 0, 0, 13100)
    saturn = object("Saturn", 5.683 * 10 ** 26, 1.434 * 10 ** 12, 0, 0, 9600)
    uranus = object("Uranus", 8.681 * 10 ** 25, 2.871 * 10 ** 12, 0, 0, 6800)
    neptune = object("Neptune", 1.024 * 10 ** 26, 4.495 * 10 ** 12, 0, 0, 5430)
    # planetX = object("PlanetX", earth.mass * 10, neptune.XPos * 20, 0, 0, 6)
    #rando = object("Random Object",1.989 * 10 ** 30, 7.785 * 10 ** 11, 0, 0, 100000)

    sys.addObject(sun)
    sys.addObject(mercury)
    sys.addObject(venus)
    sys.addObject(earth)
    sys.addObject(mars)
    sys.addObject(jupiter)
    sys.addObject(saturn)
    sys.addObject(uranus)
    sys.addObject(neptune)
    # sys.addObject(planetX)
    # sys.addObject(rando)

    sys.calcKinematic()



if __name__ == "__main__":
    main()
