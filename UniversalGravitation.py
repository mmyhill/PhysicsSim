# # # import math
# # #
# # # class UniversalGravitationSim:
# # #     def __init__(self, mPlanet, mStar, rPlanet, rStar): #radius taken from center of system
# # #         self.pMass = mPlanet
# # #         self.sMass = mStar
# # #         self.pRad = rPlanet
# # #         self.sRad = rStar
# # #         # self.sumForce = to be used when
# # #         self.g = 6.674 * 10 ** -11
# # #
# # #     def starOrbitVelocity(self):
# # #         velocity = math.sqrt(self.g * self.pMass/(self.pRad - self.sRad))
# # #         return velocity
# # #
# # #     def planetOrbitVelocity(self):
# # #         velocity = math.sqrt(self.g * self.sMass/(self.pRad - self.sRad))
# # #         return velocity
# #
# class bcMrSaundersSaid:
#     def __init__(self, rOrbit, rThis, massOrbit, massThis, v0x, v0y, y0, x0): #assuming no force at t = 0?
#     #radius is taken from center of system != center of star/planet being orbited!
#         # self.vals = open("timesAndForces.txt", "r").read() #preparing for force to be inconstant
#         self.forExport = open("ForExport.csv","w")
#         self.forExport.write("t" + ',' + "x(t)" + ',' + "v(t)" + '\n')
#         self.massOrbit = massOrbit
#         self.massThis = massThis
#         self.rOrbit = rOrbit
#         self.rThis = rThis
#         #to be reset
#         self.pastX = x0
#         self.pastY = y0
#         self.pastVx = v0x
#         self.pastVy = v0y
#         self.pastT = 0
#
#         self.g = 6.674 * 10 ** -11
#         self.force = self.g * self.massOrbit * self.massThis / (rThis - rOrbit) ** 2
#
#         self.AcOrbit = self.force/self.massOrbit
#         self.AcThis = self.force/self.massThis
#
#
#         self.calc()
#
#     # def calc(self): #recursive
#     #     time = float(self.vals[0 : self.vals.find(' ')])
#     #     accel = int(self.vals[self.vals.find(' ') + 1 : self.vals.find('\n')])/self.mass
#     #     self.vals = self.vals[self.vals.find('/n') + 1 : len(self.vals)] #remove first line of file
#     #
#     #     #V = Vi + at
#     #     deltaT = time - self.pastT
#     #     velNow = self.pastV + accel * deltaT
#     #     #xf = Vit + 1/2at^2 + xi
#     #     posNow = (self.pastV * deltaT) + ((1/2) * accel * deltaT ** 2) + self.pastX
#     #
#     #     self.forExport.write(str(time) + ',' + str(velNow) + ',' + str(posNow) + '\n')
#     #
#     #     self.pastX = posNow
#     #     self.pastV = velNow
#     #     self.PastT = time
#     #
#     #     if(not len(self.vals) == 0): #recurse
#     #         self.calc()
#
#     def calc(self): #recursive
#         time = float(self.vals[0 : self.vals.find(' ')])
#         accel = int(self.vals[self.vals.find(' ') + 1 : self.vals.find('\n')])/self.mass
#         self.vals = self.vals[self.vals.find('/n') + 1 : len(self.vals)] #remove first line of file
#
#         #V = Vi + at
#         deltaT = time - self.pastT
#         velNow = self.pastV + accel * deltaT
#         #xf = Vit + 1/2at^2 + xi
#         posNow = (self.pastV * deltaT) + ((1/2) * accel * deltaT ** 2) + self.pastX
#
#         self.forExport.write(str(time) + ',' + str(velNow) + ',' + str(posNow) + '\n')
#
#         self.pastX = posNow
#         self.pastV = velNow
#         self.PastT = time
#
#         if(not len(self.vals) == 0): #recurse
#             self.calc()
#
# def main():
#     bcMrSaundersSaid(2, 0, 0)
#
# if __name__ == "__main__":
#         main()
class obj:
    def __init__(self, mass, xPos, yPos):
        self.mass = mass
        self.xPos = xPos
        self.yPos = yPos

    def calcForce(self):




class systemInfo:
    def __init__(self):
        self.grid = {} #stores all object and their current x & y positions

    def addObjs(self,objArr): #only to be done at beginning
        for obj in objArr:
            self.grid[obj] = [obj.xPos, obj.yPos]

    
