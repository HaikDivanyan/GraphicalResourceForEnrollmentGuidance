from bs4 import BeautifulSoup
import re
from .ScrapingDataStructures import *
import pickle
import time

class DarsParser:
    def __init__(self):
        with open("apps/GREG/scraping/majors.txt") as f:
            self.majors = set(f.read().split(","))
    
    def parseDar(self, dar: str) -> tuple[list[str], list[Requirement]]:
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

       

        with open("apps/GREG/scraping/registrar.pkl", "rb") as f:
            regData = pickle.load(f)

        allClasses = []
        toRemove = []
        for req in requirements:
            if len(req.subrequirements) == 0:
                toRemove.append(req)
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

                subreq.classes = trueClasses
                allClasses.extend(trueClasses)

        for req in toRemove:
            requirements.remove(req)

        return (list(set(allClasses)), requirements)