from bs4 import BeautifulSoup
import re
from .ScrapingDataStructures import *
import pickle
import time
from pathlib import Path

class DarsParser:
    """
    Handles the parsing of Dars html objects into a list of classes, professors, and requirements.
    """
    def __init__(self):
        """
        Initializes the DarsParser object by loading a list of provided majors.
        """
        with (Path(__file__).parent / "majors.txt").open("r") as f:
            self.majors = set(f.read().split(","))

        if __debug__:
            assert len(self.majors) > 0
    
    def parseDar(self, dar: str) -> tuple[list[str], list[Requirement]]:
        """
        The function that parses a Dar string and returns a list of classes, professors, and requirements.
        :param dar: The html string to parse
        :return: tuple[list[str], list[Requirement]]: list of classes and list requirements
        """

        if __debug__:
            assert type(dar) == type("")
            assert len(dar) > 0

        dar = BeautifulSoup(dar, features='html.parser')
        requirements = []
        takenClasses = []

        for takenHTML in dar.findAll("table", "completedCourses"):
            for completedHTML in takenHTML.findAll("td", "course"):
                takenClasses.append(completedHTML.text)

        takenClasses = set(takenClasses)
        for reqHTML in dar.findAll("div", "Status_NO"):
            req = Requirement()
            req.subrequirements = []
            req.name = re.sub('[ \n]+', " ", str(reqHTML.find("div", "reqTitle").get_text()).strip())
            for subreqHTML in reqHTML.findAll("div", "subrequirement"):
                statHTML = subreqHTML.find("span", "Status_NO")
                if (statHTML is not None):
                    subreq = SubRequirement()
                    subreq.classes = []
                    if subreqHTML.find("span", "subreqTitle") == None:
                        continue
                    subreq.name = re.sub('[ \n]+', " ", str(subreqHTML.find("span", "subreqTitle").get_text()).strip())

                    needsHTML = subreqHTML.find("table", "subreqNeeds")
                    if (needsHTML is not None):
                        if (needsHTML.find("td", "hours") is not None):
                            subreq.units = int(float(str(needsHTML.find("td", "hours").next)))
                        if (needsHTML.find("td", "count") is not None):
                            subreq.count = int(float(str(needsHTML.find("td", "count").next)))

                        selectHTML = subreqHTML.find("table", "selectcourses")
                        if (selectHTML is not None):
                            ht = selectHTML.find("td", "fromcourselist")
                            a = re.sub('[ \n]+', " ", ht.get_text())
                            parts = a.split(",")
                            area = None
                            for part in parts:
                                part = part.strip()
                                part = re.sub("(\(.*\))", "", part)
                                for major in self.majors:
                                    if major in part:
                                        area = major
                                        part = re.sub(major, "", part).strip()
                                subreq.classes.append((area, part))
                            req.subrequirements.append(subreq)
            requirements.append(req)

       

        with (Path(__file__).parent / "registrar.pkl").open("rb") as f:
            regData = pickle.load(f)

        if __debug__:
            assert type(regData) == dict
            assert len(regData) > 0

        allClasses = []
        toRemove = []
        for req in requirements:
            subreqsToRemove = []
            for subreq in req.subrequirements:
                trueClasses = []
                for classes in subreq.classes:
                    if "TO" in classes[1]:
                        ps = classes[1].split(" TO ")
                        temp = re.findall("([A-Za-z]+)\d+", ps[0])
                        if len(temp) > 0:
                            prefix = temp[0]
                        else:
                            prefix = ""
                        frm = int(re.findall("(\d+)", ps[0])[0])
                        to = int(re.findall("(\d+)", ps[1])[0])
                        for i in range(frm, to + 1):
                            for post in ["", "A", "B", "C", "D", "E", "F", "G", "EW", "XP"]:
                                cid = classes[0] + " " + prefix + str(i) + post
                                if cid in regData and cid not in takenClasses:
                                    trueClasses.append(cid)
                    else:
                        if classes[0] + " " + classes[1] in regData and classes[0] + " " + classes[1] not in takenClasses:
                            trueClasses.append((classes[0] + " " + classes[1]))

                if len(trueClasses) > 0:
                    subreq.classes = trueClasses
                    allClasses.extend(trueClasses)
                else:
                    subreqsToRemove.append(subreq)
            
            for subreq in subreqsToRemove:
                req.subrequirements.remove(subreq)

            if len(req.subrequirements) == 0:
                toRemove.append(req)

        for req in toRemove:
            requirements.remove(req)

        if __debug__:
            for req in requirements:
                for subreq in req.subrequirements:
                    assert len(subreq.classes) > 0
                assert len(req.subrequirements) > 0

        return (list(set(allClasses)), requirements)