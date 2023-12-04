import pickle
from types import NoneType

from .BruinwalkController import BruinwalkController
from .DarsParser import DarsParser
from .RegistrarController import RegistrarController
from .ScrapingDataStructures import *
from .HotSeatController import HotSeatController
from pathlib import Path


class DataController:
    def __init__(self):
        self.darsParser = DarsParser()
        self.BwController = BruinwalkController()
        self.regController = RegistrarController()
        self.hotseatController = HotSeatController()
        with (Path(__file__).parent / "distro.pkl").open("rb") as f:
            self.distributions = pickle.load(f)

        if __debug__:
            assert type(self.distributions) == dict

    def parseDar(self, dar: str) -> Dars:
        if __debug__:
            assert type(dar) == str
            assert len(dar) > 0

        tempClasses, requirements = self.darsParser.parseDar(dar)
        classes = []
        professors = []

        for currClass in tempClasses:
            data = self._getClassInfo(currClass)
            if data == None:
                continue 
            for lec in data.lectures:
                for prof in lec.professors:
                    if prof not in professors:
                        professors.append(self._getProfessorInfo(prof))
            classes.append(data)
        
        return Dars(requirements, classes, professors)

    def _getClassInfo(self, cid: str) -> ClassObject:
        if __debug__:
            assert type(cid) == str

        currClass = ClassObject(id=cid)
        regData = self.regController.getClassData(currClass)

        if __debug__:
            assert type(regData) == RegistrarData or type(regData) == NoneType
            assert type(regData.units) == str or type(regData.units) == NoneType


        if regData == None:
            return None
        
        currClass.lectures = regData.lectures
        currClass.units = int(float(regData.units))
        currClass.name = regData.className
        currClass.subjectArea = regData.subjectArea

        currClass.rating = self.BwController.getClassRating(currClass)

        if __debug__:
            assert type(currClass.rating) == float or type(currClass.rating) == NoneType

        currClass.gradeDistributions = self._getGradeDistributions(currClass)

        currClass.hosteatGraph = self.hotseatController.getClassGraph(currClass.id, currClass.lectures[0].professors[0])

        if __debug__:
            assert type(currClass.hosteatGraph) == str or type(currClass.hosteatGraph) == NoneType

        return currClass
    
    def _getProfessorInfo(self, profName: str) -> Professor:
        if __debug__:
            assert type(profName) == str or type(profName) == NoneType
        p = Professor(profName)
        p.rating = self.BwController.getProfessorRating(p)
        if __debug__:
            assert type(p.rating) == float or type(p.rating) == NoneType
        return p
    
    def _getGradeDistributions(self, currClass: ClassObject) -> dict[list[int]]:
        if currClass.id not in self.distributions:
            return None
        else:
            return self.distributions[currClass.id]