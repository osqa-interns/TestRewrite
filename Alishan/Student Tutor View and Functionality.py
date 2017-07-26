"""Student Tutor View and Functionality"""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.helper import Student
from selenium.common.exceptions import TimeoutException

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': 'latest',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
LOCAL_RUN = os.getenv('LOCALRUN', 'false').lower() == 'true'
TESTS = os.getenv(
    'CASELIST',
    str([
        8268, 8287, 8254, 8255, 8290
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestViewTheListDashboard(unittest.TestCase):
    """T1.45 - View the list dashboard."""

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
        self.student.login()


    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.student.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.student.delete()
        except:
            pass

    # Case C8268 - 001 - Student | View Various Aspects of Tutor
    @pytest.mark.skipif(str(8268) not in TESTS, reason='Excluded')
    def test_student_view_the_assignemnt_list_8268(self):
        """
        #STEPS
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student user account [ ] in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, select a Tutor course
        ***The user is presented with their list of assignments.*** 
        ***Assignments for the current week are displayed.*** 
        ***Upcoming assignments are displayed under the table titled 'Coming Up'***
        ***You can see the recent topics under the "Performance Forecast" on the dashboard***(

        Click "Get Help" from the user menu in the upper right corner of the screen
        ***The user is presented with the Tutor Help Center***

        Click the 'View All Topics'
        ***The user is presented with their performance forecast.*** 

        Open the drop down menu by clicking on the menu link with the user's name
        Click on 'Performance Forecast'
        ***The user is presented with their performance forecast.*** 

        Click the button that says "Return to Dashboard"
        Click the button that says 'All Past Work'
        ***The student's past work is displayed.***
        ***Late assignments have a red clock displayed next to their 'Progress' status.***

        Click the 'Browse The Book' button
        # EXPECTED RESULT 
        ***The user is taken to the book in a new tab.*** 

        
        """
        self.ps.test_updates['name'] = 't1.45.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.45', 't1.45.001', '8268']
        self.ps.test_updates['passed'] = False

        # View Dashboard
        self.student.select_course(appearance='intro_sociology')
        self.student.page.wait_for_page_load()

        # View the Assignments for the current week
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'This Week')
            )
        )

        # View the Upcoming Assignments
        try:
            self.student.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class,"-upcoming")]')
                )
            )
        except TimeoutException:
            self.student.driver.find_element(
                By.XPATH, '//div[contains(text(),"No upcoming events")]')


        # View Recent Performance Forecast Topics
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h2[contains(@class, "recent")]')
            )
        )
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class, "guide-group")]')
            )
        )

        # View Performance Forecast Using Dashboard Button
        performance = self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//button[contains(@class,"view-performance-forecast")]')
            )
        )
        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();', performance)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        performance.click()
        assert('guide' in self.student.current_url()), \
            'Not viewing the performance forecast'


        # View Performance Forecast Using the Menu

        self.student.open_user_menu()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'viewPerformanceGuide')
            )
        ).click()
        assert('guide' in self.student.current_url()), \
            'Not viewing the performance forecast'


        self.student.open_user_menu()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'dashboard')
            )
        ).click()

        # # View the Student's Past Work
        # self.student.wait.until(
        #     expect.visibility_of_element_located(
        #         (By.LINK_TEXT, 'All Past Work')
        #     )
        # ).click()
        # assert(past_work.get_attribute('aria-selected') == 'true'),\
        #     'not viewing past work'

        # # Late Assignments have a red clock displayed next to their "Progress" tab

        # late = self.student.wait.until(
        #     expect.visibility_of_element_located(
        #         (By.XPATH, '//i[contains(@class,"info late")]')
        #     )
        # )
        # self.student.driver.execute_script(
        #     'return arguments[0].scrollIntoView();', late)
        # self.student.driver.execute_script('window.scrollBy(0, -80);')
        # late.click()

        # Click Browse The Book button

        self.student.open_user_menu()
        book = self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'view-reference-guide')
            )
        )

        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();', book)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        book.click()
        window_with_book = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_book)
        assert('book' in self.student.current_url()), \
            'Not viewing the textbook PDF'


        self.ps.test_updates['passed'] = True



    # Case C8287 - 002 - Student | View the Performance Forecast and its functions
    @pytest.mark.skipif(str(8287) not in TESTS, reason='Excluded')
    def test_student_view_personal_performance_forecast_8287(self):
        """
        #STEPS
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student user account [  |  ] in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name

        Click on the user menu in the upper right corner 
        Click on "Performance Forecast"
        ***The user is presented with personal Performance Forecast***
        ***The performance color key is presented to the user (next to the 'Return to Dashboard' button)***
        ***The user is presented with up to four problematic sections under My Weaker Areas***

        Hover the cursor over the info icon that is next to the "Performance Forecast" header
        ***Info icon shows an explanation of the data.*** 

        Scroll to Individual Chapters section
        ***The user is presented with chapters listed on the left and their sections on the right.***
        ***The user is presented with the "Practice More To Get Forecast" button under a section without 
        enough data instead of a color bar.***


        Click on a chapter bar
        # EXPECTED RESULT 
        ***The user is presented with up to five practice assessments for that chapter***

        """
        self.ps.test_updates['name'] = 't1.50.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.50',
            't1.50.001',
            '8287'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='intro_sociology')
        self.student.page.wait_for_page_load()        

        # View Personal Performance Forecast
        self.student.open_user_menu()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'viewPerformanceGuide')
            )
        ).click()
        assert('guide' in self.student.current_url()), \
            'Not viewing the performance forecast'

        # View Performance Color Key
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'guide-key')
            )
        )

        self.student.sleep(5)


        # User is presented with 4 problematic sections
        weak = self.student.driver.find_elements_by_xpath(
            "//div[@class='chapter-panel weaker']/div[@class='sections']" +
            "/div[@class='section']")

        self.student.sleep(5)

        assert(len(weak) <= 4), \
            'More than four weaker sections'


        # Info icon shows an explanation of data
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'info-link')
            )
        ).click()

        self.student.sleep(5)


        # User is presented with chapters listed on the left and their sections on the right
            # Get all the chapter panels
        panels = self.student.driver.find_elements_by_class_name(
            'chapter-panel')

            # Should be one chapter button for each panel, at least one section
            # button per panel
        for panel in panels:
            chapter = panel.find_elements_by_class_name('chapter')
            sections = panel.find_elements_by_class_name('sections')
            assert(len(sections) > 0), \
                'no sections found'
            assert(chapter[0].location.get('x') <=
                   sections[0].location.get('x')), \
                'section to the left of chapter'
        self.student.sleep(5)


        # User is presented with the "Practice More To Get Forecast" button under a section without
        # enough data instead of a color bar

        self.student.open_user_menu()
        self.student.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
        assert('guide' in self.student.current_url()), \
            'Not viewing performance forecast'
        self.student.find(By.CLASS_NAME, 'no-data')


        # User is presented with up to five practice assesments for that chapter

        self.student.wait.until(
            expect.presence_of_element_located((
                By.XPATH,
                "//div[@class='chapter']/button"
            ))
        ).click()

        assert('practice' in self.student.current_url()), \
            'Not presented with practice problems'

        self.student.sleep(5)
        breadcrumbs = self.student.find_all(
            By.XPATH,
            '//span[contains(@class,"breadcrumb-exercise")]')
        assert(len(breadcrumbs) <= 5), \
            "more than 5 questions"



        self.ps.test_updates['passed'] = True




    # Case C8290 - 003 - Student | View more Performance Forecast functions
    @pytest.mark.skipif(str(8290) not in TESTS, reason='Excluded')
    def test_student_return_to_dashboard_button_8290(self):
        """
        #STEPS
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student user account [ | ] in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name

        Click on the user menu in the upper right corner 
        Click on "Performance Forecast"
        Click on "Return To Dashboard"
        ***The user is presented with the list dashboard.***

        Click on the user menu in the upper right corner 
        Click on "Performance Forecast"
        Scroll to the Individual Chapters section
        Click on a section bar.
        # EXPECTED RESULT 
        ***The user is presented with up to five practice assessments for that section.***


        """
        self.ps.test_updates['name'] = 't1.50.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.50',
            't1.50.004',
            '8290'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='intro_sociology')
        self.student.page.wait_for_page_load()       

        # The User is presented with the list dashboard
        self.student.open_user_menu()
        self.student.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
        assert('guide' in self.student.current_url()), \
            'Not viewing performance forecast'
        self.student.sleep(5)
        self.student.open_user_menu()
        self.student.wait.until(
            expect.presence_of_element_located(
                (By.LINK_TEXT, 'Dashboard')
            )
        ).click()

        self.student.sleep(5)

        self.student.find(By.CSS_SELECTOR, '.student-dashboard')



        # The User is presented with up to five practice assessments for that section

        self.student.open_user_menu()
        self.student.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
        assert('guide' in self.student.current_url()), \
            'Not viewing performance forecast'
        self.student.find(
            By.XPATH,
            "//div[@class='chapter-panel']/div[@class='sections']" +
            "/div[@class='section']/button"
        ).click()

        assert('practice' in self.student.current_url()), \
            'Not presented with practice problems'

        self.student.sleep(5)
        breadcrumbs = self.student.find_all(
            By.XPATH,
            '//span[contains(@class,"breadcrumb-exercise")]')
        assert(len(breadcrumbs) <= 5), \
            "more than 5 questions"


        self.ps.test_updates['passed'] = True



    #     # Case C8255 - 004 - Student | Using a student with one Tutor course with no work done
    # @pytest.mark.skipif(str(8255) not in TESTS, reason='Excluded')
    # def test_student_bypass_the_course_picker_8255(self):
    #     """
    #     #STEPS
    #     Go to https://tutor-qa.openstax.org/
    #     Click on the 'Login' button
    #     Enter the student user account [  |  ] in the username and password text boxes
    #     Click on the 'Sign in' button
    #     ***The user bypasses the course picker and is presented with the dashboard***

    #     If the user has more than one course, click on a Tutor course name
    #     Click on the user menu in the upper right corner 
    #     Click on "Performance Forecast"
    #     ***The user is presented with blank performance forecast with no section breakdowns and the words 
    #     "You haven't worked enough problems for Tutor to predict your weakest topics."***

    #     Click the OpenStax logo
    #     # EXPECTED RESULT 
    #     ***The user is returned to their dashboard.***


    #     """
    #     self.ps.test_updates['name'] = 't1.38.002' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.38',
    #         't1.38.002',
    #         '8255'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #         # ***The user bypasses the course picker and is presented with the
    #         # dashboard (because student532 is only enrolled in one course)***

    #     self.user = Student(
    #         use_env_vars=True,
    #         pasta_user=self.ps,
    #         capabilities=self.desired_capabilities
    #     )
    #     self.user.login(username="qas_01")
    #     assert('list' in self.user.current_url()), \
    #         'Not in a course'


    #     # The user is presented with blank performance forecast with no section breakdowns and the words 
    #     # "You haven't worked enough problems for Tutor to predict your weakest topics."
    #     self.student.logout()
    #     self.student.driver.get("https://tutor-qa.openstax.org/")
    #     self.student.login(username=os.getenv('STUDENT_NO_WORK'),
    #                        url="https://tutor-qa.openstax.org/")
    #     self.student.select_course(appearance='college_physics')
    #     self.student.find(By.CSS_SELECTOR, '.student-dashboard')
    #     self.student.open_user_menu()
    #     self.student.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
    #     assert('guide' in self.student.current_url()), \
    #         'Not viewing performance forecast'
    #     self.student.find(By.CLASS_NAME, "no-data-message")
    #     self.student.sleep(5)

    #     # Click on the OpenStax logo to return to the dashboard

    #     self.student.logout()
    #     student2 = Student(
    #         username=os.getenv('STUDENT_USER_ONE_COURSE'),
    #         password=os.getenv('STUDENT_PASSWORD'),
    #         existing_driver=self.student.driver,
    #         pasta_user=self.ps,
    #         capabilities=self.desired_capabilities
    #     )
    #     student2.login()
    #     student2.page.wait_for_page_load()
    #     student2.open_user_menu()
    #     student2.wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH,
    #              '//a[contains(text(),"Performance Forecast") ' +
    #              'and @role="menuitem"]')
    #         )
    #     ).click()
    #     self.student.driver.find_element(
    #         By.XPATH,
    #         '//i[contains(@class,"ui-brand-logo")]'
    #     ).click()
    #     assert('list' in self.student.current_url()), \
    #         'Not viewing the list dashboard 011'

    #     self.ps.test_updates['passed'] = True



    # Case C8254 - 005 - Student | Navigation Shortcuts
    @pytest.mark.skipif(str(8254) not in TESTS, reason='Excluded')
    def test_student_select_a_course_8254(self):
        """
        #STEPS
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student username [  ] in the username text box
        Click 'Next'
        Enter the student password [  ] in the password text box
        Click on the 'Login' button
        ***The user logs into Tutor and is presented with a list of courses if they 
        have multiple courses, or their dashboard for a course if they are only enrolled in one course***

        Click on a Tutor course name
        ***The user selects a course and is presented with the dashboard.*** 

        Open the drop down menu by clicking the menu link containing the user's name
        Click the 'Performance Forecast' button
        Click on the name of the course
        ***The user is returned to their dashboard.***

        Click on the OpenStax logo
        ***The user is returned to the course picker.*** 

        Click on the user menu on the right of the header
        Click 'Log Out'
        # EXPECTED RESULT 
        ***User is logged out of tutor***

        """
        self.ps.test_updates['name'] = 't1.38.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.38',
            't1.38.001',
            '8254'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        # Select a Course
        self.student.select_course(appearance='intro_sociology')
        self.student.page.wait_for_page_load()    



        # Click on course name to return to the dashboard

        self.student.open_user_menu()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'viewPerformanceGuide')
            )
        ).click()

        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'course-name')
            )
        ).click()

        # Click on logo to return to course picker

        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'ui-brand-logo')
            )
        ).click()

        self.ps.test_updates['passed'] = True



