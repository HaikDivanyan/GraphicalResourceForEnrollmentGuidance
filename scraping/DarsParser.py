from bs4 import BeautifulSoup
import re
from ScrapingDataStructures import *

class DarsParser:
    def __init__(self):
        with open("majors.txt") as f:
            self.majors = set(f.read().split(","))
    
    def parseDar(self, dar: str) -> tuple[list[tuple[str, str]], list[Requirement]]:
        dar = BeautifulSoup(dar, features='html.parser')
        requirements = []
        for reqHTML in dar.findAll("div", "Status_NO"):
            req = Requirement()
            req.name = re.sub('[ \n]+', " ", str(reqHTML.find("div", "reqTitle").get_text()).strip())
            for subreqHTML in reqHTML.findAll("div", "subrequirement"):
                statHTML = subreqHTML.find("span", "Status_NO")
                if (statHTML is not None):
                    subreq = SubRequirement()
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


        classes = []
        for req in requirements:
            for subreq in req.subrequirements:
                classes.extend(subreq.classes)
        return (list(set(classes)), requirements)