from ScrapingDataStructures import *
from BruinwalkController import BruinwalkController
from DarsParser import DarsParser
from RegistrarController import RegistrarController

class DataController:
    def __init__(self):
        self.darsParser = DarsParser()
        self.BwController = BruinwalkController()
        self.regController = RegistrarController()

    def parseDar(self, dar: str) -> Dars:
        tempClasses, requirements = self.darsParser.parseDar(dar)
        classes = []
        professors = []

        for currClass in tempClasses:
            data = self._getClassInfo(currClass)
            if data == None:
                continue 
            for lec in data.lectures:
                for prof in lec.professors:
                    professors.append(self._getProfessorInfo(prof))
            classes.append(data)
        
        return Dars(requirements, classes, professors)

    def _getClassInfo(self, cid) -> ClassObject:

        currClass = ClassObject(id=cid)
        regData = self.regController.getClassData(currClass)

        if regData == None:
            return None
        
        currClass.lectures = regData.lectures
        currClass.units = regData.units
        currClass.name = regData.className
        currClass.subjectArea = regData.subjectArea

        currClass.rating = self.BwController.getClassRating(currClass)

        return currClass
    
    def _getProfessorInfo(self, profName: str) -> Professor:
        p = Professor(profName)
        p.rating = self.BwController.getProfessorRating(p)
        return p