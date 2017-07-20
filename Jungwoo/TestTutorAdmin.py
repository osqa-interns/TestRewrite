"""Tutor: Admin"""

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
from selenium.webdriver.common.keys import Keys
# from staxing.assignment import Assignment

########################
"""from staxing.helper import Teacher"""
##########################
from helper import Admin

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
class TestTutorAdmin(unittest.TestCase):
    """Tutor | Teacher"""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        if not LOCAL_RUN:
            self.admin = Admin(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.admin = Admin(
                use_env_vars=True
            )
        #self.admin.login(url="https://tutor-qa.openstax.org/admin")
        #self.teacher.select_course(appearance='college_physics')

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.admin.delete()
        except:
            pass

    #@pytest.mark.skipif(str(58279) not in TESTS, reason='Excluded')
    def test_admin_change_course_start_end_dates_(self):
        """
        Log in as an Admin
        Go to the course management page
        Edit a course
        Change the term and course year
        Click Save
        ***Start and end dates should reflect the new term's timeframe***

        Edit a course
        Change the Starts at date and Ends at date
        Click Save 

        Expected Result:

        ***Start and end dates are changed***
        """
        
        self.ps.test_updates['name'] = 't1.13.001' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.001', '7978']
        self.ps.test_updates['passed'] = False

        #go to courses admin page directly and log in
        self.admin.login(url="https://tutor-qa.openstax.org/admin/courses")
        #search 'preview' in the search bar
        self.admin.find(By.CSS_SELECTOR, "#search-courses").send_keys('preview\n')
        self.admin.page.wait_for_page_load()
        pages = self.admin.find_all(By.CSS_SELECTOR, ".pagination>a")
        #go to very last page
        self.admin.scroll_to(pages[-2])
        self.admin.sleep(1)
        pages[-2].click()
        #click on Edit button for very last course
        edit = self.admin.find_all(By.XPATH, ".//*[contains(text(),'Edit')]")
        self.admin.scroll_to(edit[-1])
        edit[-1].click()
        #change year field by adding 1 
        yearfield = self.admin.find(By.CSS_SELECTOR, "#course_year")
        year = yearfield.get_attribute('value')
        newyear = str(int(year) + 1)
        yearfield.send_keys(len(year) * Keys.DELETE)
        yearfield.send_keys(newyear)
        #change start date and end date
        oldstartdatefield = self.admin.find(By.CSS_SELECTOR, "#course_starts_at")
        oldenddatefield = self.admin.find(By.CSS_SELECTOR, "#course_ends_at")  
        #get start date and end date values
        oldstartdate = oldstartdatefield.get_attribute('value')
        oldenddate = oldenddatefield.get_attribute('value')
        change = datetime.timedelta(days=400)
        #converts start date and end date values into datetime objects and adds the change
        newstartdate = datetime.datetime.strptime(oldstartdate, '%Y-%m-%d %X %Z' ) + change
        #converts into a string format accepted by the form
        oldstartdatefield.send_keys(datetime.datetime.strftime(newstartdate, '%Y/%m/%d %X')[:-3])
        #converts start date and end date values into datetime objects and adds change ( 400 days)
        newenddate = datetime.datetime.strptime(oldenddate, '%Y-%m-%d %X %Z') + change
        #converts into a string format accepted by teh form
        #newenddate = datetime.datetime.strftime(newenddate1, '%Y/%m/%d %X')[:-3]
        oldenddatefield.send_keys(datetime.datetime.strftime(newenddate, '%Y/%m/%d %X')[:-3])
        #saves changes
        self.admin.sleep(3)
        self.admin.find(By.CSS_SELECTOR, "#edit-save").click()
        self.admin.sleep(3)
        #updated start date and end date fields, get their values
        updatedstartdate = self.admin.find(
            By.CSS_SELECTOR, "#course_starts_at").get_attribute('value')
        updatedstartdatetime = datetime.datetime.strptime(updatedstartdate, '%Y-%m-%d %X %Z')
        updatedenddate = self.admin.find(
            By.CSS_SELECTOR, "#course_ends_at").get_attribute('value')
        updatedenddatetime = datetime.datetime.strptime(updatedenddate, '%Y-%m-%d %X %Z')
        #assert that the datetime objects I put into it are the ones in the updated field
        assert(newstartdate.isocalendar() == updatedstartdatetime.isocalendar())
        assert(newenddate.isocalendar() == updatedenddatetime.isocalendar())
        #change start date and end date to what it was
        yearfield = self.admin.find(By.CSS_SELECTOR, "#course_year")
        yearfield.send_keys(len(year) * Keys.DELETE)
        yearfield.send_keys(year)
        startdatefield = self.admin.find(By.CSS_SELECTOR, "#course_starts_at")
        startdatefield.send_keys(datetime.datetime.strftime(
            datetime.datetime.strptime(oldstartdate, '%Y-%m-%d %X %Z'),
            '%Y/%m/%d %X')[:-3]
        )
        enddatefield = self.admin.find(By.CSS_SELECTOR, "#course_ends_at")
        enddatefield.send_keys(datetime.datetime.strftime(
            datetime.datetime.strptime(oldenddate, '%Y-%m-%d %X %Z'),
            '%Y/%m/%d %X')[:-3]
        )
        self.admin.find(By.CSS_SELECTOR, "#edit-save").click()
        self.ps.test_updates['passed'] = True

    @pytest.mark.skipif(str(58279) not in TESTS, reason='Excluded')
    def test_notification_and_faulty_url(self):
        """
        Go to tutor-qa
        Log in as admin
        Click "Admin" from the user menu
        Click "System Setting" 
        Click "Notifications"
        Enter a new notification into the text box
        Click "Add"

        Log out of admin account
        Log in as a teacher
        ***An orange header with the notification pops up when you sign in***

        Go to https://tutor-qa.openstax.org/not_a_real_page

        Expected result:

        ***a styled error page is displayed***

        Corresponding test case: T2.18 001, 030
        """

        self.ps.test_updates['name'] = 't1.13.001' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.001', '7978']
        self.ps.test_updates['passed'] = False

        self.admin.login(url="https://tutor-qa.openstax.org/admin")
        self.admin.find(By.XPATH,".//*[contains(text(),'System Setting')]").click()
        self.admin.find(By.CSS_SELECTOR,"a[href*='notification']").click()
        self.admin.find(By.CSS_SELECTOR, "#message").send_keys('test_notification')
        self.admin.find(By.CSS_SELECTOR, ".btn.btn-default").click()
        #logout
        self.admin.find(By.XPATH,".//*[contains(text(),'admin')]").click()
        self.admin.find(By.CSS_SELECTOR, 'a[href*="logout"]').click()
        #log into teacher account
        self.admin.login(username=os.getenv('TEACHER_USER'),
            password=os.getenv('TEACHER_PASSWORD'))
        self.admin.find(By.CSS_SELECTOR, '.my-courses-item-title>a').click()
        try:
            self.admin.find(By.XPATH,
                './/*[contains(text(),"I don’t know yet")]')
        except:
            pass
        #checks if notification is there
        self.admin.wait.until(
            expect.visibility_of_element_located((
                By.XPATH,
                '//div[contains(@class,"notifications-bar")]' +
                '//span[text()="test_notification"]'
            ))
        )
        self.admin.find(
            By.XPATH,
            '//div[contains(@class,"notifications-bar")]' +
            '//span[text()="test_notification"]'
        )
        #log out of teacher
        self.admin.logout()
        #log into admin
        self.admin.login(url="https://tutor-qa.openstax.org/admin")
        self.admin.find(By.XPATH, '//a[text()="System Setting"]').click()
        self.admin.find(By.XPATH, '//a[text()="Notifications"]').click()
        #remove general notification
        self.admin.find(By.XPATH, '//a[text()="Remove"]').click()
        self.admin.driver.switch_to_alert().accept()
        #go to invalid website
        self.admin.get('https://tutor-qa.openstax.org/not_a_real_page')
        #confirm styling of webpage
        self.admin.wait.until(
            expect.presence_of_element_located((
                By.CSS_SELECTOR,
                '.invalid-page'
            ))
        )
        self.ps.test_updates['passed'] = True
        
















