
import math
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

        # self.magV= v0Magnitude

        self.vX = v0x
        self.vY = v0y

        self.forceX = 0
        self.forceY = 0
        #need to be given initial y and and x velocities bc can't produce tangent line with 1 point given

    def resetForces(self):
        self.forceX = 0
        self.forceY = 0

    def getVelocityX(self):
        # if(self.XPos - self.pastXPos != 0):
        #     slope = (self.YPos - self.pastYPos)/(self.XPos - self.pastXPos)
        #     angle = math.atan(slope)
        #     return math.cos(angle) * self.magV
        # else:
        #     return 0
        return self.vX


    def getVelocityY(self):
        # if(self.XPos - self.pastXPos != 0):
        #     slope = (self.YPos - self.pastYPos)/(self.XPos - self.pastXPos)
        #     angle = math.atan(slope)
        #     return math.sin(angle) * self.magV
        # else:
        #     return self.magV
        return self.vY


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
        for run in xrange(int(self.endTimeSecs / self.timeInterval)):
            self.updateForces()
        #calculate velocities, update position values
            for obj in self.grid:
                #xf = Vit + 1/2at^2 + xi
                xNow = obj.getVelocityX() * self.timeInterval + (1.0/2) * obj.forceX/obj.mass * self.timeInterval ** 2 + obj.XPos
                yNow = obj.getVelocityY() * self.timeInterval + (1.0/2) * obj.forceY/obj.mass * self.timeInterval ** 2 + obj.YPos

                #V = Vi + at
                print(str(obj.forceX/obj.mass * self.timeInterval))
                print(str(obj.forceY/obj.mass * self.timeInterval))
                newVx = obj.getVelocityX() + obj.forceX/obj.mass * self.timeInterval
                newVy = obj.getVelocityY() + obj.forceY/obj.mass * self.timeInterval

                obj.vX = newVx
                obj.vY = newVy
                # vMagNow = math.sqrt(newVx ** 2 + newVy ** 2)#should remain relatively constant
                #
                # obj.vMag = vMagNow

                # obj.pastX = obj.XPos
                # obj.pastY = obj.YPos

                obj.XPos = xNow
                obj.YPos = yNow

                #"time (seconds)" + ', ' + "x(t)" + ', ' + "y(t)" + ', ' + "vX(t)" + ', ' + "vY(t)" + ', ' + "v(t)"
                obj.forExport.write(str(run * self.timeInterval) + ', ' + str(obj.XPos) + ', ' + str(obj.YPos) + ', ' + str(obj.getVelocityX()) + ', ' + str(obj.getVelocityY()) + "\n")
                #+ ', ' + str(obj.magV) +

    def updateForces(self):#need to reset forces for changing radii
        for obj in self.grid:
            obj.resetForces()

        for this in xrange(len(self.grid)):
            for next in xrange(1, len(self.grid) - this):
                obj = self.grid[this]
                other = self.grid[this + next]

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
def main():
    #timeInterval, endTimeYears
    sys = system((60 * 60), 1)

    #name, mass, x0, y0, v0x, v0y
    earth = object("Earth", 5.972 * 10 ** 24, 1.496 * 10 ** 11, 0, 0, 30000)
    sun = object("Sun", 1.989 * 10 ** 30, 0, 0, 0, 0)

    sys.addObject(earth)
    sys.addObject(sun)

    sys.calcKinematic()



if __name__ == "__main__":
    main()
