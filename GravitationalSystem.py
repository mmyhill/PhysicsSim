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

        # self.pastXPos = x0
        # self.pastYPos = y0 #to be reset

        self.vX = v0x
        self.vY = v0y

        self.forceX = 0
        self.forceY = 0
        #need to be given initial y and and x velocities bc can't produce tangent line with 1 point given

        # self.xMax = 0 #used to calculate orbital period of ellipse
        # self.yMax = 0 #to be reset
        # 
        # self.startX = x0
        # self.startY = y0

    def resetForces(self):
        self.forceX = 0
        self.forceY = 0

    def getVelocityX(self):
        return self.vX


    def getVelocityY(self):
        return self.vY

    # def calcOrbitalPeriod(self, time):
    #     circum = abs(self.xMax) * abs(self.yMax) * 3.141592653589793238462643383
    #     period = circum/time
    #
    #     timeStr = "seconds"
    #     if(period > 60):
    #         period = period/60 #minutes
    #         timeStr = "minutes"
    #     if(period > 60):
    #         period = period/60 #minutes
    #         timeStr = "hours"
    #     if(period > 24):
    #         period = period/24 #hours
    #         timeStr = "days"
    #     if(period > 365):
    #         period = period/365
    #         timeStr = "years"
    #
    #     print("\n" + "Full orbital period completed( " + str(period) + " " + timeStr + " )" + "\n")

        # self.forExport.write("\n" + "Full orbital period completed( " + str(period) + " " + timeStr + " )" + "\n")



class system:
    def __init__(self, timeInterval, endTimeYears):
        self.grid = []
        self.g = 6.67 * 10 ** -11
        self.timeInterval = timeInterval #should be in seconds
        self.endTimeSecs = endTimeYears * 365 * 24 * 60 * 60 #put in in years, converted to seconds

    def addObject(self, toAdd):
        self.grid.append(toAdd)
        toAdd.forExport = open(str(toAdd.name) + ".csv","w")
        toAdd.forExport.write("time (seconds)" + ', ' + "x(t)" + ', ' + "y(t)" + ', ' + "vX(t)" + ', ' + "vY(t)" + ', ' + "v(t)" + '\n')
        #toAdd.forExport.write("0" + ', ' + str(toAdd.YPos) + ', ' + str(toAdd.YPos) + ', ' + str(toAdd.getVelocityX()) + ', ' + str(toAdd.getVelocityY())  + ', ' + str(toAdd.magV) + "\n" )

    def calcKinematic(self):
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

                #V = Vi + at
                newVx = obj.getVelocityX() + obj.forceX/obj.mass * self.timeInterval
                newVy = obj.getVelocityY() + obj.forceY/obj.mass * self.timeInterval

                obj.vX = newVx
                obj.vY = newVy
                # vMagNow = math.sqrt(newVx ** 2 + newVy ** 2)#should remain relatively constant
                #
                # obj.vMag = vMagNow

                # obj.pastX = obj.XPos
                # obj.pastY = obj.YPos

                # if(sign(obj.XPos - obj.startX) != sign(xNow - obj.startX) and run != 0): #full orbital rotation completed
                #     obj.calcOrbitalPeriod(run * self.timeInterval)

                obj.XPos = xNow
                obj.YPos = yNow

                if(abs(xNow) > obj.xMax):
                    obj.xMax = abs(xNow)
                if(abs(yNow) > obj.yMax):
                    obj.yMax = abs(yNow)


                obj.forExport.write(str(run * self.timeInterval) + ', ' + str(obj.XPos) + ', ' + str(obj.YPos) + ', ' + str(obj.getVelocityX()) + ', ' + str(obj.getVelocityY()) + "\n")
                #+ ', ' + str(obj.magV) +


                pygame.draw.ellipse(screen, (0,0,0), [500 + xNow/(10 ** 10 * .7), 500 + yNow/(10 ** 10 * .7), obj.mass**(1/25), obj.mass**(1/25)],0 )
                # pygame.draw.ellipse(screen, (0,0,0), [250 + xNow/10 ** 15, 250 + yNow/10 ** 15, 10, 10],2)

                #"time (seconds)" + ', ' + "x(t)" + ', ' + "y(t)" + ', ' + "vX(t)" + ', ' + "vY(t)" + ', ' + "v(t)"
            pygame.display.flip()

    def updateForces(self):#need to reset forces for changing radii
        for obj in self.grid:
            obj.resetForces()

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




pygame.init()

screen = pygame.display.set_mode((1000,1000))
def main():
    #timeInterval, endTimeYears
    sys = system((60 * 60 * 24), 80)

    #name, mass, x0, y0, v0x, v0y
    sun = object("Sun", 1.989 * 10 ** 30, 0, 0, 0, 0)
    mercury = object("Mercury", 3.285 * 10 ** 23, 5.971 * 10 ** 10, 0, 0, 47400)
    venus = object("Venus", 4.867 * 10 ** 24, 1.082 * 10 ** 11,0, 0, 35000)
    earth = object("Earth", 5.972 * 10 ** 24, 1.496 * 10 ** 11, 0, 0, 35000)
    mars = object("Mars", 6.39 * 10 ** 23, 2.279 * 10 ** 11, 0, 0, 24100)
    jupiter = object("Jupiter", 1.898 * 10 ** 27, 7.785 * 10 ** 11, 0, 0, 13100)
    saturn = object("Saturn", 5.683 * 10 ** 26, 1.434 * 10 ** 12, 0, 0, 9600)
    uranus = object("Uranus", 8.681 * 10 ** 25, 2.871 * 10 ** 12, 0, 0, 6800)
    neptune = object("Neptune", 1.024 * 10 ** 26, 4.495 * 10 ** 11, 0, 0, 5430)

    sys.addObject(sun)
    sys.addObject(mercury)
    sys.addObject(venus)
    sys.addObject(earth)
    sys.addObject(mars)
    sys.addObject(jupiter)
    sys.addObject(saturn)
    sys.addObject(uranus)
    sys.addObject(neptune)

    sys.calcKinematic()



if __name__ == "__main__":
    main()
