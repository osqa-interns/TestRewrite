"""Course cloning and copying past assignments | Tutor: Teachers"""

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
from helper import Teacher

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
class TestTutorTeacher(unittest.TestCase):
    """Tutor | Teacher"""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        if not LOCAL_RUN:
            self.teacher = Teacher(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.teacher = Teacher(
                use_env_vars=True
            )
        self.teacher.login()
        #self.teacher.select_course(appearance='college_physics')

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.teacher.delete()
        except:
            pass

    @pytest.mark.skipif(str(58279) not in TESTS, reason='Excluded')
    def test_course_cloning_and_copying_past_assignments(self):
        """
        Clone courses and copy past assignments from the courses you cloned from.

        Go to tutor-qa.openstax.org
        Log in to a teacher account 
        In the dashboard, click "Add a Course"
        Select a Course
        Select a Semester
        Select Copy a past course
        Select a course to copy
        Enter a name for the tutor course 
        ***Text should be able to be entered into box***

        Specify the number of sections for a new course 
        ***Number could be entered. Page won't proceed if anything else is entered***

        Specify the number of students for the course
        ***Number could be entered. Page won't proceed if anything else is entered***

        Press "Continue"
        ***A course dashboard appears with the name and section number user entered***
        Copy a homework 
        ***When user clicks on a past assignment on the left panel, An auto-filled assignment creation form appeared***

        Copy an event 
        ***When user clicks on a past Event on the left panel, An auto-filled event creation form appeared***

        Copy a reading 
        ***When user clicks on a past Reading on the left panel, An auto-filled event creation form appeared***
        Copy an external assignment 

        EXPECTED RESULT:
        When user clicks on a past External Assignment on the left panel, An auto-filled event creation form appeared

        Corresponding test cases: T3.09 004, 005, 006, 007, 008, 010, 011, 012, 013
        """

        self.ps.test_updates['name'] = 't1.13.001' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.001', '7978']
        self.ps.test_updates['passed'] = False

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.CSS_SELECTOR, '.user-actions-menu')
            )
        ).click()
        self.teacher.wait.until(
                expect.element_to_be_clickable((By.CSS_SELECTOR, '#menu-option-createNewCourse'))
            ).click()
        self.teacher.wait.until(
                expect.element_to_be_clickable((By.XPATH, ".//*[@data-appearance='micro_economics' and contains(text(), 'Econ')]"))
            ).click()
        self.teacher.find(
            By.CSS_SELECTOR, '.next.btn.btn-primary').click()
        self.teacher.wait.until(
                expect.element_to_be_clickable((By.XPATH, ".//*[contains(text(), 'summer')]"))
            ).click()
        self.teacher.find(
            By.CSS_SELECTOR, '.next.btn.btn-primary').click()


        self.teacher.sleep(3)

    @pytest.mark.skipif(str(58279) not in TESTS, reason='Excluded')
    def test_tutor_help_center(self):
        """
        Go to tutor-qa.openstax.org and log in as a teacher
        Click on a Tutor course
        Click "Get Help" from the "Help" dropdown in the upper right corner 
        ***User is presented with the Tutor Help Center***

        Enter a question or search words into search engine
        Click "search"
        ***User is presented with search results***

        Scroll to the bottom of the screen
        ***Email Us link works***

        Click on an article
        ***Article should pop up/be able to be viewed***
        Scroll to "Feedback"
        Click "Yes"
        ***Message that says "Thanks for your feedback!" is displayed***

        Click "<Back to search results"
        Click on another article
        Scroll to "Feedback"
        Click "No"
        ***User is presented with a popup box that allows them to input feedback***

        Click "Cancel"
        ***Popup box closes***

        Under "Feedback", Click "No"
        Enter feedback, click "Submit"
        ***Message that says "Thanks for your feedback!" is displayed in the box***

        Click "Close window"
        ***The popup box closes and the message "Thanks for your feedback" displays beneath "Feedback"***

        Scroll to bottom, under "Related Articles", click an article

        Expected Result:

        ***User is presented with the related article***

        Corresponding test cases: T2.18 004-013, 014
        """
        self.ps.test_updates['name'] = 't2.18.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.18', 't2.18.003', '58279']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        #goes to a random course
        self.teacher.find(By.XPATH, '//p[@data-is-beta="true"]').click()
        #opens help menu and clicks Help Articles
        self.teacher.open_help_menu()
        self.teacher.find(By.LINK_TEXT, 'Help Articles').click()

        #switches active windows
        window_with_help = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_help)
        self.teacher.page.wait_for_page_load()
        #in search bar, search 'getting started'
        self.teacher.find(By.ID, 'searchAskInput') \
            .send_keys('getting started')
        self.teacher.find(By.ID, 'searchAskButton').click()
        self.teacher.page.wait_for_page_load()
        #check that Email Us button exists
        self.teacher.find(By.XPATH, '//a[contains(text(),"Email Us")]')
        #click on the FIRST article. Not random because for this test, I'm choosing 2
        #different articles. Want them to be different, so choosing 1st then 2nd articles
        self.teacher.find(By.CSS_SELECTOR,'.article a').click()
        #click feedback yes button
        self.teacher.find(By.XPATH, ".//*[@value='Yes']").click()
        #checks that "Thanks for your feedback" mesasge is displayed
        self.teacher.page.wait_for_page_load()
        self.teacher.find(
            By.XPATH, ".//*[contains(text(),'Thanks for your feedback!')]")
        #Back to search results
        self.teacher.find(
            By.XPATH, ".//*[contains(text(), 'Back to search results')]").click()
        #Click on second article
        relatedArticles = self.teacher.find_all(
            By.CSS_SELECTOR, '.article a')
        relatedArticles[randint(1,len(relatedArticles)-1)].click()
        self.teacher.sleep(5)
        #self.teacher.find_all(By.CSS_SELECTOR, '.article a')[1].click()
        #Click No
        self.teacher.find(By.XPATH, ".//*[@value='No']").click()
        self.teacher.find(By.CSS_SELECTOR, "#feedbackTextArea").send_keys('testing')
        self.teacher.find(By.XPATH, ".//*[@value='Submit']").click()
        self.teacher.find(By.XPATH, ".//*[contains(text(), 'Thanks for your feedback')]")
        self.teacher.find(By.XPATH, ".//*[contains(text(), 'close window')]").click()
        self.teacher.find(By.XPATH, ".//*[contains(text(),'Thanks for your feedback!')]")
        relatedlinks = self.teacher.find_all(
            By.CSS_SELECTOR, ".relatedLink")
        print(len(relatedlinks))
        relatedlinks[randint(1,len(relatedlinks)-1)].click()
        self.teacher.find(By.CSS_SELECTOR, ".mainTitle")
        self.teacher.sleep(3)
        #elf.teacher.page.wait_for_page_load()
        #self.teacher.send_keys('AUTOMATION TESTING. DISREGARD')
        self.ps.test_updates['passed'] = True

    #@pytest.mark.skipif(str(58279) not in TESTS, reason='Excluded')
    def test_setting_open_and_due_times(self):
        """
        Go to https://tutor-qa.openstax.org
        Log in as a teacher
        Click on a Tutor course name
        Click "Add Assignment"
        Click "Add Event"
        Click on the text box for the open time
        Enter desired time
        Click on the forward arrow to rotate the calendar to the course end date
        Click on the text box for the due time
        Enter desired time
        Click on the forward arrow to rotate the calendar to the course end date
        ***User is able to set open and due time. A due or open date cannot be set 
        to after the end of term. The end of term can be viewed in Course Settings 
        and Roster. The calendars cannot be rotated to view months after to 
        the end of the course***

        Expected result:
        ***User is able to set open and due time. A due or open date cannot be 
        set to after the end of term. The end of term can be viewed in Course 
        Settings and Roster. The calendars cannot be rotated to view months after
         to the end of the course***

        Corresponding test cases: T3.09 023
        """
        self.teacher.page.wait_for_page_load()
        #self.teacher.find(By.CSS_SELECTOR, '.my-courses-item-title>a').click()
        #self.teacher.sleep(4)
        length = self.teacher.get_course_list()
        courses = self.teacher.find_all(By.CSS_SELECTOR,
            '.my-courses-item-title>a')
        courses[randint(0,len(courses)-1)].click()
        """self.teacher.find_all(
            By.CSS_SELECTOR, 
            '.my-courses-item-title>a')[randint(0,length)].click()"""
        try:
            self.admin.find(By.XPATH,
                './/*[contains(text(),"I don’t know yet")]')
        except:
            pass
        self.teacher.find(By.CSS_SELECTOR,"a[href*='event']").click()
        

        #relatedArticles[randint(1,len(relatedArticles)-1)].click()






@PastaDecorator.on_platforms(BROWSERS)
class TestDemoTeacher(unittest.TestCase):
    
    """Tests for demo_teacher a teacher with 0 courses"""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        if not LOCAL_RUN:
            self.teacher = Teacher(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.teacher = Teacher(
                use_env_vars=True
            )
        self.teacher.login(username='demo_teacher', password='staxly16')
        #self.teacher.select_course(appearance='college_physics')

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.teacher.delete()
        except:
            pass
    
    @pytest.mark.skipif(str(58279) not in TESTS, reason='Excluded')
    def test_no_course_page_and_tutor_guides(self):
        """
        Go to tutor-qa.openstax.org as a teacher with 0 courses. demo_teacher works
        ***See message "We cannot find an Openstax course associated with your account"***

        Click "Tutor Instructors. Get help >"

        Expected Result:

        ***Tutor Help Center opens in another tab with the Getting Started guide***

        Corresponding test cases: T2.18 002, 003
        """
        self.ps.test_updates['name'] = 't1.13.001' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.001', '7978']
        self.ps.test_updates['passed'] = False

        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, ".//*[@class='lead' and contains(text(), 'cannot find')]")))
        self.teacher.wait.until(
                expect.element_to_be_clickable((By.XPATH, ".//*[@target and contains(text(), 'Instructors.')]"))
            ).click()
        self.teacher.sleep(3)



    







