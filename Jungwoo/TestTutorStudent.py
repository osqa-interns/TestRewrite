"""Tutor: Students"""

import inspect
import json
import os
import pytest
import unittest
import datetime

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment

########################
"""from staxing.helper import Teacher"""
##########################
from helper import Student

# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.action_chains import ActionChains


basic_test_env = json.dumps([
    {
        'platform': 'Windows 10',
        'browserName': 'chrome',
        'version': 'latest',
        'screenResolution': "1024x768",
    }
])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
LOCAL_RUN = os.getenv('LOCALRUN', 'false').lower() == 'true'
TESTS = os.getenv(
    'CASELIST',
    str([
        #7978, 7979, 7980, 7981, 7982,
        #7983, 7984, 7985, 7986, 7987,
        #7988, 7989, 7990
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestTutorStudent(unittest.TestCase):
    """Tutor | Teacher"""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        if not LOCAL_RUN:
            self.student = Student(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.student = Student(
                use_env_vars=True
            )
        
        #self.teacher.select_course(appearance='college_physics')

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.student.delete()
        except:
            pass

    @pytest.mark.skipif(str(58279) not in TESTS, reason='Excluded')
    def test_not_in_any_courses_directed_to_no_courses_page_and_tutor_guide(self):
        """
        Go to tutor-qa.openstax.org
        Log in as a student with no courses, qa_student_37003 works
        ***Message "We cannot find an OpenStax course associated with your account displays with help links***

        Click "Tutor Students. Get help >"
        ***Tutor Help Center opens in another tab with the Getting Started guide*** click "Add a Course"       
        """
        
        self.ps.test_updates['name'] = 't1.13.001' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.001', '7978']
        self.ps.test_updates['passed'] = False

        self.student.login(
            username='qa_student_37003', 
            password=os.getenv('CONTENT_PASSWORD')
        )
        self.student.page.wait_for_page_load()
        self.student.wait.until(
            expect.visibility_of_element_located((
                By.CSS_SELECTOR,
                '.panel-body .lead:first-of-type'
                ))
        )
        self.student.find(By.XPATH, ".//*[contains(text(),'Tutor Students')]").click()
        window_with_help = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_help)
        
        self.ps.test_updates['passed'] = True

    @pytest.mark.skipif(str(58279) not in TESTS, reason='Excluded')
    ############################NOT DONE#############################
    def test_student_questions_why_info_icon_reporting_errata(self):
        """
        Prerequisite: Student needs a homework/reading assignment

        Go to https://tutor-qa.openstax.org/
        Log in as a student
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on a homework or reading assignment
        Click on the "Report an error" link in the bottom right corner
        ***A new tab with the assessment errata form appears, with the assessment ID already filled in***

        Enter text into the free response text box
        Click "Answer"
        Click on "Why?" next to the message "Now choose from one of the following options"
        ***The user is presented with information about why two-step problems***

        Then continue working the homework until a spaced practice question comes up
        Click on the info icon in the top right of the question box next to spaced practice
        ***User is presented with a separate message for spaced practice***

        Expected result:

        ***At the bottom of a homework question there should be a link back to the content***

        Corresponding test cases: T2.10 006, 008, T2.11 008

        """
        
        self.ps.test_updates['name'] = 't1.13.001' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.001', '7978']
        self.ps.test_updates['passed'] = False

        self.student.login()
        #pick course. Would want to be random; issue is making sure course has assignments
        #thus, just chose course 353 for this as it has some assignments. Subject to change
        #code for random tutor course is as follows:
        #courses = self.student.find_all(
            #By.XPATH,".//*[@class='course-branding my-courses-item-brand' and contains(text(),'Tutor')]")
        #courses[randint(0,len(courses)-1)].click()
        course = self.student.find(By.CSS_SELECTOR, "a[href*='353']")
        self.student.scroll_to(course)
        course.click()
        try:
            homeworks = self.student.find_all(By.XPATH, 
                ".//*[@class='-this-week panel panel-default']//*[@class='icon icon-lg icon-homework']")
            homeworks[randint(0,len(homeworks)-1)].click()
            assignment = 'homework'
            self.student.sleep(5)
        except:
            readings = self.student.find_all(By.XPATH,
                ".//*[@class='-this-week panel panel-default']//*[@class='icon icon-lg icon-reading']")
            readings[randint(0,len(readings)-1)].click()
            assignment = 'reading'
        if assignment == 'homework':
            try:
                self.student.find(By.CSS_SELECTOR,
                    ".openstax-question>textarea").send_keys('testing')
                self.student.find(By.CSS_SELECTOR,".async-button").click()
                self.student.page.wait_for_page_load()
                self.student.find(By.XPATH,
                    ".//*[@class='text-info' and contains(text(),'Why?')]")
                self.student.find(By.CSS_SELECTOR, "a[href*='errata']").click()
                self.student.sleep(3)
                self.student.driver.switch_to().window(handles[1])
                self.student.sleep(3)
                self.student.browser.driver.close();
                self.student.sleep(3)
                self.student.browser.driver.switch_to().window(handles[0])
                self.student.sleep(3)
            except:
                self.student.find(By.XPATH,
                    ".//*[@class='text-info' and contains(text(),'Why?')]")
                self.student.scroll_to(report)
                report = self.student.find(By.CSS_SELECTOR, "a[href*='errata']")
                report.click()
                self.student.sleep(3)
                self.student.driver.switch_to.window(handles[1])
                self.student.sleep(3)
                self.student.browser.driver.close();
                self.student.sleep(3)
                self.student.browser.driver.switch_to.window(handles[0])
                self.student.sleep(3)




        self.student.sleep(3)
    @pytest.mark.skipif(str(58279) not in TESTS, reason='Excluded')
    def test_student_late_icons(self):
        """
        Go to tutor-qa.openstax.org
        Log in as a student with late assignments(homework, reading, external assignment)

        Expected result:

        ***Observe the late icons (this is the red clock) for homework, reading, and external assignment***

        Corresponding test cases: T2.10 021,023,025
        """
        self.ps.test_updates['name'] = 't1.13.001' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.001', '7978']
        self.ps.test_updates['passed'] = False

        self.student.login()
        self.student.find(By.CSS_SELECTOR, ".info.late")

        self.ps.test_updates['passed'] = True


#@pytest.mark.skipif(str(58279) not in TESTS, reason='Excluded')
    def test_reading_assingments_progress_bar_milestones_section_number_header(self):
        """
        Login as student
        Click on a tutor course
        Click "Browse the Book" or select "Browse the Book" from the user menu
        Select a section from the contents
        ***Section numbers listed in the header***

        Go to tutor-qa.openstax.org
        Log in as a student
        Click on a course that has a reading assignment
        Click on a reading assignment
        ***Section numbers listed in the header***

        Click on the right arrow
        ***The progress bar at the top reflects how far along you are as you read***

        ***At the start of each new section, the section number is displayed***

        Click on the icon next to the calendar on the header

        Expected result:
         
        ***The user is presented with prior milestones***

        Corresponding test cases: T2.13 001, 002, 004, 006
        """
        self.ps.test_updates['name'] = 't1.13.001' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.001', '7978']
        self.ps.test_updates['passed'] = False

        self.student.login()
        self.student.random_course()
        self.student.browse_book()
        self.student.sleep(3)
        book = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(book)
        sections = self.student.find_all(By.CSS_SELECTOR,".section")
        num = randint(0,len(sections))
        sections[num].click()
        self.student.sleep(3) 



    


















