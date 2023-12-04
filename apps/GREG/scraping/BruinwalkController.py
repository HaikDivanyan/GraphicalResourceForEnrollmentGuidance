import pickle
from .ScrapingDataStructures import ClassObject
from .ScrapingDataStructures import Professor
import urllib.request
from pathlib import Path

class BruinwalkController:
    def __init__(self):
        with (Path(__file__).parent / "bruinwalk.pkl").open("rb") as f:
            self.classData = pickle.load(f)

    def getClassRating(self, registrarClass: ClassObject) -> float:
        if registrarClass.id in self.classData:
            return self.classData[registrarClass.id]
        
        try:
            html = str(urllib.request.urlopen("https://bruinwalk.com/search/?q=" + registrarClass.id.replace(" ", "+")).read())
            i = html.find("<b class=\"rating\"> ") + 19
            rating = float(html[i:i+3])
        except:
            rating = None

        self.classData[registrarClass.id] = rating
        with (Path(__file__).parent / "bruinwalk.pkl").open("wb") as f:
            pickle.dump(self.classData, f)

        return rating
    
    def getProfessorRating(self, professor: Professor) -> float:
        if professor.name in self.classData:
            return self.classData[professor.name]
        
        try:
            last = professor.name.split(", ")[0].replace(" ", "+")
            html = str(urllib.request.urlopen("https://bruinwalk.com/search/?q=" + last).read())
            i = html.find("<b class=\"rating\"> ") + 19
            rating = float(html[i:i+3])
        except Exception as e:
            rating = None

        self.classData[professor.name] = rating

        with (Path(__file__).parent / "bruinwalk.pkl").open("wb") as f:
            pickle.dump(self.classData, f)

        return rating