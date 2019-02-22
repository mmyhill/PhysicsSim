import math

class object:
    def __init__(self, mass, v0, name, posX, posY): #input initial velocities
        self.name = name
        self.mass = mass
        # self.pastVz = v0z
        self.xPos = posX
        self.yPos = posY
        # self.zPos = posZ
        self.forExport = None
        if(posX != 0 or posY != 0):
            self.pastVx = v0 * (posX/ math.sqrt(posX ** 2 + posY ** 2))
            self.pastVy = v0 * (posY/ math.sqrt(posX ** 2 + posY ** 2))

        else: #should only be used for sun
            self.pastVx = 0
            self.pastVy = 0

        self.pastV = math.sqrt(self.pastVx ** 2 + self.pastVy ** 2)

    # def calcOrbitalPeriod(self):
    #     #use T^2/A^3 approx = 1 (in AU's!)
    #     if(not self.semiMajor == -1):
    #         toPrint = ''
    #         orbital = math.sqrt(self.semiMajor ** 3 * self.thirdLawK)
    #         if(orbital > 60):
    #             orbital = orbital/60 #minutes
    #             toPrint = "minutes"
    #         if(orbital > 60): #hours
    #             orbital = orbital /60
    #             toPrint = "hours"
    #         if(orbital > 24):
    #             orbital = orbital/24 #days
    #             toPrint = "days"
    #         if(orbital > 365):
    #             orbital = orbital/365 #years
    #             toPrint = "years"
    #
    #         return str(orbital) + toPrint
    #     else:
    #         return "N/A"
    #         self.thirdLawK = (365 * 24 * 60 * 60) ** 2/(1.496 * 10 ** 11) ** 3


class system:
    def __init__(self, timeInterval, endTime):
        self.g = 6.674 * 10 ** -11
        self.timeInterval = timeInterval
        self.endTime = endTime
        self.grid = [] #will have keys for each obj
        #should I assume objects start from rest??????
        self.forExport = open("System.txt" ,"w")


    def calcEnergy(self):
        #Ug = -G * m1 * m2/ r
        sumGravit = 0
        sumKinetic = 0

        for num in range(len(self.grid) - 1):
            obj = self.grid[num]
            sumKinetic += (1/2) * obj.mass * obj.pastV ** 2
            for x in range(len(self.grid) - 2 - num):
                other = self.grid[num + x + 1]

                xDif = obj.xPos - other.xPos
                yDif = obj.yPos - other.yPos

                distance = math.sqrt(xDif ** 2 + yDif ** 2)

                sumGravit += self.g * obj.mass * other.mass / (distance)

        self.forExport.write("Gravitational Potential Energy: " + str(sumGravit) + "\n" + "Kinetic Potential Energy: " + str(sumKinetic))

    def addObject(self, obj):
        self.grid.append(obj)
        obj.forExport = open(str(obj.name) + ".csv","w")
        # obj.forExport.write("orbital period: " + str(obj.calcOrbitalPeriod()) + "\n")
        # obj.forExport.write("time" + ', ' + "x(t)" + ', ' + "y(t)" + ', ' + "z(t)" + ', ' + "vX(t)" + ', ' + "vY(t)" +  ', ' + "vZ(t)" + '\n')
        obj.forExport.write("time" + ', ' + "x(t)" + ', ' + "y(t)" + ', ' + "v(t)" + '\n')

    def calcVelocity(self, thisTime): #recursive
        if(not thisTime >= self.endTime): #base case
            for obj in self.grid:
                for other in self.grid:
                    xDif = obj.xPos - other.xPos
                    yDif = obj.yPos - other.yPos
                    # zDif = obj.zPos - other.zPos

                    forceX = 0
                    forceY = 0

                    # forceZ = 0
                    if(xDif > 0):
                        forceX += self.g * obj.mass * other.mass / (xDif ** 2)
                    if(yDif > 0):
                        forceY += self.g * obj.mass * other.mass / (yDif ** 2)
                    # if(zDif > 0):
                    #     forceZ += self.g * obj.mass * other.mass / (zDif ** 2)

                #V = Vi + at
                velX = obj.pastVx + (forceX/obj.mass) * self.timeInterval
                velY = obj.pastVy + (forceY/obj.mass) * self.timeInterval
                # velZ = obj.pastVz + (forceZ/obj.mass) * self.timeInterval

                obj.pastVx = velX
                obj.pastVy = velY
                # obj.pastVz = velZ

                #xf = Vit + 1/2at^2 + xi
                posX = velX * self.timeInterval + (1/2) * (forceX/obj.mass) * self.timeInterval ** 2 + obj.xPos
                posY = velY * self.timeInterval + (1/2) * (forceY/obj.mass) * self.timeInterval ** 2 + obj.yPos
                # posZ = velZ * self.timeInterval + (1/2) * (forceY/obj.mass) * self.timeInterval ** 2 + obj.zPos

                obj.xPos = posX
                obj.yPos = posY
                # obj.zPos = posZ

                vel = math.sqrt(velX ** 2 + velY ** 2)

                 # obj.forExport.write(str(thisTime) + ', ' + str(posX) + ', ' + str(posY) + ', ' + str(posZ) + ', ' + str(velX) + ', ' + str(velY) + ', ' + str(velZ) + '\n')
                obj.forExport.write(str(thisTime) + ", " + str(posX) + ", " + str(posY) + ", " + str(vel) + "\n")

            self.calcVelocity(thisTime + self.timeInterval)

def main():
    s = system(.01, .10)

        # mass, v0, name, posX, posY
    sun = object(1.989 * 10 ** 30, 0, "sun", 0, 0)
    s.addObject(sun)

    mercury = object(3.825 * 10 ** 23, 5.791 * 10 ** 10, "Mercury", -5.89235045, -0.5019410229)
    s.addObject(mercury)

    venus = object(4.867 * 10 ** 24, 3.5 * 10 ** 4, "Venus", 1.362990944, -11.38197745)
    s.addObject(venus)

    earth = object(5.972 * 10 ** 24, 30000 , "Earth", -2.43548936, 14.06829145)
    s.addObject(earth)

    mars = object(6.39 * 10 ** 23, 24000, "Mars", -23.91450692, -6.054663588)
    s.addObject(mars)

    jupiter = object(1.898 * 10 ** 27, 13100, "Jupiter", -64.00015193, -50.77156684)
    s.addObject(jupiter)

    saturn = object(5.683 * 10 ** 26, 9600, "Saturn", -0.12165467, -67.96667391)
    s.addObject(saturn)

    uranus = object(8.681 * 10 ** 25, 6800, "Uranus", 118.9592587, 60.83889755)
    s.addObject(uranus)

    neptune = object(1.024 * 10 ** 26, 5430, "Neptune", 193.5715885, -57.66846262)
    s.addObject(neptune)

    s.calcVelocity(0.0)
    s.calcEnergy()

if __name__ == "__main__":
    main()
