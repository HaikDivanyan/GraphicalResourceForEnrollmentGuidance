import pickle

from .BruinwalkController import BruinwalkController
from .DarsParser import DarsParser
from .RegistrarController import RegistrarController
from .ScrapingDataStructures import *
from .HotSeatController import HotSeatController
from pathlib import Path


class DataController:
    """
    Main class that coordinates the parsing of Dars with the creation of ClassObjects, Requirement objects and Professor objects.
    """
    def __init__(self):
        """
        Initializes a DataController object with instiated DarsParser, BruinwalkController, RegistrarController, and HotseatController objects along with loading the grade distribution cache.
        """
        self.darsParser = DarsParser()
        self.BwController = BruinwalkController()
        self.regController = RegistrarController()
        self.hotseatController = HotSeatController()
        with (Path(__file__).parent / "distro.pkl").open("rb") as f:
            self.distributions = pickle.load(f)

    def parseDar(self, dar: str) -> Dars:
        """
        Parses a Dar file and returns a Dars object.
        :param dar: The html dar to parse
        :return: Returns the built Dars object
        """
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

    def _getClassInfo(self, cid) -> ClassObject:
        """
        A helper class to create and build a class object from the classid string. Concentrates data from hotseat, bruinwalk, registrar, and grad distribution cache.
        :param cid: The class id of the class to get the data for
        :return: Returns a class object
        """

        currClass = ClassObject(id=cid)
        regData = self.regController.getClassData(currClass)

        if regData == None:
            return None
        
        currClass.lectures = regData.lectures
        currClass.units = int(float(regData.units))
        currClass.name = regData.className
        currClass.subjectArea = regData.subjectArea

        currClass.rating = self.BwController.getClassRating(currClass)

        currClass.gradeDistributions = self._getGradeDistributions(currClass)

        currClass.hosteatGraph = self.hotseatController.getClassGraph(currClass.id, currClass.lectures[0].professors[0])

        return currClass
    
    def _getProfessorInfo(self, profName: str) -> Professor:
        """
        A helper class to create and build a professor object from the professor name string. Concentrates data from bruinwalk..
        :param profName: The name of the professor to get the data for
        :return: returns a professor object
        """
        p = Professor(profName)
        p.rating = self.BwController.getProfessorRating(p)
        return p
    
    def _getGradeDistributions(self, currClass: ClassObject) -> dict[list[int]]:
        """
        A helper class to get the grade distribution for a class.
        :param currClass: ClassObject for which to retrieve the grade distributions.
        :return: Returns a dict of the form {(profname, quarter): grade distribution}
        """
        if currClass.id not in self.distributions:
            return None
        else:
            return self.distributions[currClass.id]