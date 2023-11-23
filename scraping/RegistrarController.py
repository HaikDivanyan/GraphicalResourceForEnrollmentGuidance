from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ScrapingDataStructures import *
from selenium.common.exceptions import NoSuchElementException 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
import re
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager
import pickle

class RegistrarController:
    def __init__(self):
        with open("registrar.pkl", "rb") as f:
            self.registrarData = pickle.load(f)
    
    def getClassData(self, currClass: ClassObject) -> RegistrarData:
        if currClass.id in self.registrarData:
            return self.registrarData[currClass.id]
        else:
            return None

    def get_discussions_for_lecture(self,main_lecture,driver,class_id,class_name):
        enroll_column = main_lecture.find_element(By.CLASS_NAME,"enrollColumn")
        try:
            toggle = enroll_column.find_element(By.CLASS_NAME, "toggle")
            driver.execute_script("arguments[0].setAttribute('aria-expanded', 'true');", toggle)
            toggle_button = toggle.find_element(By.CLASS_NAME,"transparentButton")
            toggle_button.click()

            secondary_section = WebDriverWait(main_lecture, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "secondarySection"))
                )

            discussion_children = []
            pattern = re.compile(r"(\d{9})_" + re.escape(class_id) + r"-children")
            elements = secondary_section.find_elements(By.XPATH, "./*[@id]")
            for element in elements:
                element_id = element.get_attribute('id')
                if pattern.match(element_id):
                    discussions = secondary_section.find_element(By.ID,element_id)
                    discussion_children = discussions.find_elements(By.CSS_SELECTOR,".row-fluid.data_row.secondary-row.class-info.class-not-checked")
            
            # Looping over each discussion for the given class
            discussions = []
            for d in range(len(discussion_children)):
                disc_id = self.get_lecture_id(discussion_children[d])
                disc_time = self.get_lecture_day_time(discussion_children[d],class_name,driver)
                if disc_time != self.STATUS_ERROR:
                    # disc time is a list
                    disc = DiscussionSection(disc_id,disc_time)
                    discussions.append(disc)
            
            return discussions
        # No discussions for lecture 
        except NoSuchElementException:
            empty_discussions = []
            return empty_discussions
        
    def get_lecture_id(self,main_lecture):
        section_column = main_lecture.find_element(By.CLASS_NAME,"sectionColumn")
        class_section_info = section_column.find_element(
                By.CSS_SELECTOR,
                '.cls-section.click_info'
            )
        lecture_name_tag = class_section_info.find_element(By.CLASS_NAME,"hide-small")
        return lecture_name_tag.text

    def get_lecture_units(self,main_lecture):
        class_units_column = main_lecture.find_element(By.CLASS_NAME,"unitsColumn")
        class_units = class_units_column.text
        if '/' in class_units:
            value = class_units.split('/')[0]
            return value.strip()  
        else:

            return class_units


    def get_lecture_day_time(self,main_lecture,class_name,driver):
        class_days_column = main_lecture.find_element(By.CSS_SELECTOR,
            ".dayColumn.hide-small.beforeCollapseHide")
        class_days_column_nested = class_days_column.find_element(By.XPATH, "./*")


        class_times_column = main_lecture.find_element(By.CLASS_NAME,
        "timeColumn")

        day_and_time = class_times_column.text.split("\n")
        lecture_time_list = []
        if len(day_and_time) == 7 and day_and_time[0]=='Varies':
            lecture_time_1 = Time(day_and_time[1],day_and_time[4])
            lecture_time_list.append(lecture_time_1)
            lecture_time_2 = Time(day_and_time[2],day_and_time[5])
            lecture_time_list.append(lecture_time_2)
            lecture_time_3 = Time(day_and_time[3],day_and_time[6])
            lecture_time_list.append(lecture_time_3)
            return lecture_time_list
        if len(day_and_time) == 4:
            lecture_time_1 = Time(day_and_time[0],day_and_time[2])
            lecture_time_2 = Time(day_and_time[1],day_and_time[3])
            lecture_time_list.append(lecture_time_1)
            lecture_time_list.append(lecture_time_2)
            return lecture_time_list
        if len(day_and_time)==3 and day_and_time[1]=='Varies':
            lecture_time = Time(day_and_time[0],day_and_time[2])
            lecture_time_list.append(lecture_time)
            return lecture_time_list
        if len(day_and_time)==3 and day_and_time[0]=='Varies':
            lecture_time = Time(day_and_time[1],day_and_time[2])
            lecture_time_list.append(lecture_time)
            return lecture_time_list
        if day_and_time[0] == 'Not scheduled' or day_and_time[0] == 'Varies':
            return self.STATUS_ERROR
        if len(day_and_time[0]) == 0:
            return self.STATUS_ERROR   
        

        lecture_time = Time(day_and_time[0],day_and_time[1])
        lecture_time_list.append(lecture_time)
        return lecture_time_list

    def get_prof_name(self,main_lecture):
        try:
            class_instructor_column = main_lecture.find_element(By.CSS_SELECTOR,
                ".instructorColumn.hide-small")
            prof_name = class_instructor_column.text
            prof_name_list = [name.strip('.') for name in prof_name.split('\n')]
            if len(prof_name_list) > 1:
                for prof in prof_name_list:
                    if prof == 'The Staff' or prof == 'No instructors':
                        prof = None
            elif len(prof_name_list)==1 and prof_name_list[0] == 'The Staff' or prof_name_list[0] == 'No instructors':
                prof_name_list[0] = None
            return prof_name_list
        except NoSuchElementException:
            class_instructor_column = main_lecture.find_element(By.CLASS_NAME,
            "instructorColumn ")
            prof_name = class_instructor_column.text
            prof_name_list = [name.strip('.') for name in prof_name.split('\n')]
            if len(prof_name_list) > 1:
                for prof in prof_name_list:
                    if prof == 'The Staff' or prof == 'No instructors':
                        prof = None
            elif len(prof_name_list)==1 and prof_name_list[0] == 'The Staff' or prof_name_list[0] == 'No instructors':
                prof_name_list[0] = None
            return prof_name_list
        
        
    def get_all_subject_areas(self):
        majors_txt_file_path = 'GraphicalResourceForEnrollmentGuidance/scraping/majors.txt'
        with open(majors_txt_file_path, 'r') as file:
            contents = file.read()
            self.subject_area_list = contents.split(',')

    def get_registar_URL_for_subject_area(self,subject_area):
        contains_whitespace = any(char.isspace() for char in subject_area)
        contains_ampersand = '&' in subject_area
    
        if contains_whitespace:
            subject_area = subject_area.replace(" ", "+")
        if contains_ampersand:
            subject_area = subject_area.replace("&","%26")
        registrar_winter_24_url = 'https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Computer+Science+(COM+SCI)&t=24W&sBy=subject&subj={subject_area}&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex'
        formatted_url = registrar_winter_24_url.format(subject_area=subject_area)
        return formatted_url

    def scraper_helper(self,driver,url,subject_area):
        driver.get(url) 
        main = driver.find_element(By.ID, "main")
        container_class = main.find_element(By.CLASS_NAME, "container")
        page_class = container_class.find_element(By.CLASS_NAME, "page")
        app_embed_container = page_class.find_element(By.CLASS_NAME, "app-embed-container")
        ucla_sa_soc_app = app_embed_container.find_element(By.TAG_NAME,"ucla-sa-soc-app")
        shadow_root = shadow_root = driver.execute_script("return arguments[0].shadowRoot", ucla_sa_soc_app)
        web_component_wrapper = shadow_root.find_element(By.ID, "webComponentWrapper")
        layout_content_area = web_component_wrapper.find_element(By.ID,"layoutContentArea")
        search_results = layout_content_area.find_element(By.CLASS_NAME,"search_results")

        div_search_results = search_results.find_element(By.ID,"divSearchResults")
        div_class_names = div_search_results.find_element(By.ID,"divClassNames")
        div_results = div_class_names.find_element(By.CLASS_NAME,"results")
        div_results_title = div_results.find_element(By.ID, "resultsTitle")

        all_classes = div_results_title.find_elements(By.CSS_SELECTOR,".row-fluid.class-title")
        return all_classes

    def if_process_class(self,class_element):
        class_id = class_element.get_attribute('id')
        head_of_class = class_element.find_element(By.CLASS_NAME,"head")
        class_name_button = head_of_class.find_element(By.ID, class_id+"-title")
        class_name = class_name_button.text
        class_number_code = class_name.split('-')
        pattern = r'((3[0-9]{2}|4\d{2}|5\d{2}|600|195|196|197|198|199|89HC?\/189HC?)(\w*))'
        match = re.match(pattern, class_number_code[0])
        
        if match:
            return class_name, self.STATUS_ERROR
        else:
            return class_name, self.STATUS_PROCEED

    def process_each_class(self,subject_area, class_element,driver,class_name):
        class_id = class_element.get_attribute('id')
        self.class_id_list.append(class_id)
        head_of_class = class_element.find_element(By.CLASS_NAME,"head")
        class_name_button = head_of_class.find_element(By.ID, class_id+"-title")
        
        class_name = class_name_button.text
        driver.execute_script("arguments[0].setAttribute('aria-expanded', 'true')", class_name_button)
        class_name_button.click()
        main_info_container = None

        try: 
            main_info_container = WebDriverWait(class_element, 30).until(
                    EC.presence_of_element_located((By.ID, class_id+"-container"))
                )

            if main_info_container.text=='No results available based off your filter criteria.':
                return 

            # lecture gateway
            class_children_info_gate = main_info_container.find_element(By.ID,class_id+"-children")

            # Get all main lectures 
            main_lectures = class_children_info_gate.find_elements(
                    By.CSS_SELECTOR,
                    '.row-fluid.data_row.primary-row.class-info.class-not-checked'
                )
            
            units = 0
            lect_object_list = []
            for lect in range(len(main_lectures)): 
                try:
                    lecture_time = self.get_lecture_day_time(main_lectures[lect], class_name,driver)
                    if lecture_time != self.STATUS_ERROR:
                        
                        lect_id = self.get_lecture_id(main_lectures[lect])
                        prof_name = self.get_prof_name(main_lectures[lect])
                        units = self.get_lecture_units(main_lectures[lect])
                        discussions = self.get_discussions_for_lecture(main_lectures[lect],driver,class_id,class_name)
                        lect_obj = Lecture(lect_id,lecture_time,discussions, prof_name)
                        lect_object_list.append(lect_obj)
                        
                except NoSuchElementException:
                    print(f"exception occured on class name: {class_name}")
            if len(lect_object_list) != 0:
                return lect_object_list, units,class_id,class_name
            else:
                return self.STATUS_ERROR
        except TimeoutException:
            print(f'time out exception on {subject_area}')
            
    def process_class_id(self,subject_area,class_name):
        print(class_name)
        number = class_name.split()[0]
        class_id = subject_area + ' ' + number
        return class_id
       
    def print_reg_object(self, registar_data_obj: RegistrarData):
        print(f"class_id: {registar_data_obj.classId}")    
        print(f"class name: {registar_data_obj.className}")  
        print(f"units: {registar_data_obj.units}")  
        print(f"subject area: {registar_data_obj.subjectArea}")    
        lectures = registar_data_obj.lectures
        for lect in lectures:
            print(f"lecture id: {lect.id}")  
            for lect_times in lect.times:
                print(f"lect time: {lect_times.days}, lect hours: {lect_times.hours}")
            for p in lect.professors:
                print(f"prof name: {p}")
            for d in lect.discussions:
                print(f"disc id: {d.id}")
                for dd in d.times:
                 print(f"disc days: {dd.days}, disc hours: {dd.hours}")
    # Main function
    def scrapeNewData(self):
        self.subject_area_list = []
        self.STATUS_ERROR = 1
        self.STATUS_PROCEED = 0
        # temp list
        self.class_id_list = []
        self.regitsrar_data_objects_dict = {}
        
        self.get_all_subject_areas()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

        for subject_area in self.subject_area_list:
            URL = self.get_registar_URL_for_subject_area(subject_area)
            all_classes_per_subject_area = self.scraper_helper(driver,URL,subject_area)

            for clss in all_classes_per_subject_area:
                class_name, status = self.if_process_class(clss)
                if status == self.STATUS_PROCEED:
                    result = self.process_each_class(subject_area,clss,driver,class_name)
                    if isinstance(result,tuple):
                        lect_object_list, units, class_id, cls_name = result
                        class_id = self.process_class_id(subject_area,class_name)
                        registrar_data_obj = RegistrarData(class_id, cls_name,units,subject_area, lect_object_list)
                        self.regitsrar_data_objects_dict[class_id] = registrar_data_obj
        with open("registrar.pkl", "wb") as f:
            pickle.dump(self.regitsrar_data_objects_dict, f)