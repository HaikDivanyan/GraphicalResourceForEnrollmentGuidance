from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import pickle
from pathlib import Path

class HotSeatController:
    URL = 'https://hotseat.io/faq'

    def __init__(self):
        with (Path(__file__).parent / "hotseat.pkl").open("rb") as f:
            self.hotseatData = pickle.load(f)
    
    def get_chart_element(self,current_instructor,driver):
        dropdown = driver.find_element(By.CSS_SELECTOR,".mt-2.lg\\:flex.lg\\:space-x-4")
        flex = dropdown.find_element(By.CLASS_NAME,"flex-1")
        try:
            enrollement_card = flex.find_element(By.ID,"EnrollmentCard")
        except:
            return None
        enrollment_progress = enrollement_card.find_element(By.ID,"enrollment-progress")
        chart = enrollment_progress.find_element(By.CLASS_NAME,"Chart")
        chart_outer_html = chart.get_attribute('outerHTML')
        # with open('chart_complete_html.html', 'w', encoding='utf-8') as file:
        #     file.write(chart_outer_html)
        return chart_outer_html
    
    def if_match_instructor_names(self,prof_name,current_instructor_name_element):
        current_instructor_name = current_instructor_name_element.text.splitlines()[0]
        if prof_name == current_instructor_name:
            return True
        if prof_name == None:
            return False
        before_comma = prof_name.split(',')[0]
    
        pattern = re.compile(r'\b' + re.escape(before_comma) + r'\b', re.IGNORECASE)

        
        # Search for the pattern in the other string
        if pattern.search(current_instructor_name.strip()):
            return True
        else:
            return False
        
        
    def getClassGraph(self,class_id,prof_name):
        if (class_id, prof_name) in self.hotseatData:
            return self.hotseatData[(class_id, prof_name)]

        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
            driver.get(self.URL)
            input_field = driver.find_element(By.ID, "search-downshift-input-input")
            input_field.send_keys(class_id)
            wait = WebDriverWait(driver, 10)

            # Wait until the suggestion is clickable
            first_suggestion = wait.until(EC.element_to_be_clickable((By.ID, "search-downshift-input-item-0")))
            first_suggestion.click()

            next_page_element_selector = 'instructor-nav'  # e.g., '#content', '.header', etc.
            wait.until(EC.visibility_of_element_located((By.ID, next_page_element_selector)))
            wait = WebDriverWait(driver, 10)
            # Get course instructors
            instructor_nav = driver.find_element(By.ID,"instructor-nav")
            gateway_instructor = instructor_nav.find_element(By.CSS_SELECTOR, ".hidden.sm\\:block.border-b.border-gray-200.dark\\:border-gray-700")
            gateway_instructor_child = gateway_instructor.find_element(By.CSS_SELECTOR,".-mb-px.flex.space-x-8.overflow-x-auto")
            try:
                current_course_instructor = gateway_instructor_child.find_element(By.CSS_SELECTOR,".course-instructor-tab.tab-selected")
            except:
                self.hotseatData[(class_id, prof_name)] = None

                with (Path(__file__).parent / "hotseat.pkl").open("wb") as f:
                    pickle.dump(self.hotseatData, f)

                return None
            
            other_instructors = gateway_instructor_child.find_elements(By.CLASS_NAME,"course-instructor-tab")

            cur_instructor_element = current_course_instructor
            
            other_instructors.append(current_course_instructor)
            for inst in other_instructors:
                if self.if_match_instructor_names(prof_name,inst):
                    # print(self.if_match_instructor_names(prof_name,inst))
                    cur_instructor_element = inst
                    break
                    
            prof_name_from_hotseat = cur_instructor_element.text.splitlines()[0]
            # Click on that insturctor's graph
            
            cur_instructor_element.click()
            
            instructor_text_element = wait.until(EC.visibility_of_element_located((By.XPATH, f"//a[contains(@class, 'course-instructor-tab') and contains(@class, 'tab-selected') and contains(text(), '{prof_name_from_hotseat}')]")))

            # Get the text and compare
            instructor_text = instructor_text_element.text.strip().splitlines()[0]
            # print(f"instructor_text: {instructor_text}")
            # print(f"prof name from hotseat: {prof_name_from_hotseat}")
            # if instructor_text == prof_name_from_hotseat:
            #     print("Found the instructor with the correct name.")
            # else:
            #     print("The instructor name does not match.")

            graph = self.get_chart_element(cur_instructor_element,driver)
            
            self.hotseatData[(class_id, prof_name)] = graph

            with (Path(__file__).parent / "hotseat.pkl").open("wb") as f:
                pickle.dump(self.hotseatData, f)

            return graph
        
        except TimeoutException:
            # print("exception")
            self.getClassGraph(class_id,prof_name)
        
        
        
        # wait = WebDriverWait(driver, 20)
        # driver.save_screenshot('/Users/anushtadevosyan/Desktop/CS130/full_page_screenshot.png')
        # print(driver.page_source)