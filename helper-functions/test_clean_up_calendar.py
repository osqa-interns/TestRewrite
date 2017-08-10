import datetime
import inspect
import json
import os
import pytest
import unittest
import random

from random import randint
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from staxing.assignment import Assignment
from time import sleep


# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher

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
        1, 2, 3, 4
    ])
)
class CleanUpCalendar(unittest.TestCase):

    def setUp(self):
        """Pretest settings."""
        self.teacher = Teacher(use_env_vars=True)
        self.teacher.login()
        self.teacher.select_course(appearance='college_biology')

    def tearDown(self):
        """Test destructor."""
        try:
            self.teacher.delete()
        except:
            pass

    @pytest.mark.skipif(str(1) not in TESTS, reason='Excluded')
    def test_clean_up_reading(self):
        """
        Delete all assignment of one type in current and next month from the calendar
        """
        # draft reading cleanup
        drafts = self.teacher.find_all(
            By.XPATH,
            '//div[@data-assignment-type="reading" and not(contains(@class, "is-published") or (@draggable="true"))]')

        # published reading cleanup
        drafts = self.teacher.find_all(
            By.XPATH,
            '//div[@data-assignment-type="reading" and '
            'contains(@class, "is-published") and not(@draggable="true")]'
        )

        num = len(drafts)
        while num > 0:
            draft = self.teacher.find(
                By.XPATH,
                '//div[@data-assignment-type="reading" and '
                'not(contains(@class, "is-published") or (@draggable="true"))]')
            draft.click()
            delete_button = self.teacher.wait.until(
                expect.element_to_be_clickable(
                    (By.XPATH, '//button[contains(@class,"delete-link")]')
                )
            )
            self.teacher.scroll_to(delete_button)
            sleep(1)
            delete_button.click()
            self.teacher.find(
                By.XPATH, '//button[contains(text(),"Yes")]'
            ).click()
            sleep(3)
            self.teacher.driver.refresh()
            num -= 1

        self.teacher.find(
            By.CSS_SELECTOR, '.calendar-header-control.next'
        ).click()
        sleep(5)
        drafts = self.teacher.find_all(
            By.XPATH, '//div[@data-assignment-type="reading" and '
                      'not(contains(@class, "is-published") or (@draggable="true"))]')
        num = len(drafts)
        while num > 0:
            draft = self.teacher.find(
                By.XPATH, '//div[@data-assignment-type="reading" and '
                          'not(contains(@class, "is-published") or (@draggable="true"))]')
            draft.click()
            delete_button = self.teacher.wait.until(
                expect.element_to_be_clickable(
                    (By.XPATH, '//button[contains(@class,"delete-link")]')
                )
            )
            self.teacher.scroll_to(delete_button)
            sleep(1)
            delete_button.click()
            self.teacher.find(
                By.XPATH, '//button[contains(text(),"Yes")]'
            ).click()
            sleep(3)
            self.teacher.driver.refresh()
            num -= 1

    @pytest.mark.skipif(str(2) not in TESTS, reason='Excluded')
    def test_clean_up_homework(self):
        drafts = self.teacher.find_all(
            By.XPATH,
            '//div[@data-assignment-type="homework" and not(contains(@class, "is-published") or (@draggable="true"))]')

        # published reading cleanup
        # drafts = self.teacher.find_all(
        #     By.XPATH,
        #     '//div[@data-assignment-type="homework" and '
        #     'contains(@class, "is-published") and not(@draggable="true")]'
        # )
        num = len(drafts)
        while num > 0:
            draft = self.teacher.find(
                By.XPATH,
                '//div[@data-assignment-type="homework" and '
                'not(contains(@class, "is-published") or (@draggable="true"))]')
            draft.click()
            delete_button = self.teacher.wait.until(
                expect.element_to_be_clickable(
                    (By.XPATH, '//button[contains(@class,"delete-link")]')
                )
            )
            self.teacher.scroll_to(delete_button)
            sleep(1)
            delete_button.click()
            self.teacher.find(
                By.XPATH, '//button[contains(text(),"Yes")]'
            ).click()
            sleep(3)
            self.teacher.driver.refresh()
            num -= 1
        self.teacher.find(
            By.CSS_SELECTOR, '.calendar-header-control.next'
        ).click()
        sleep(5)
        drafts = self.teacher.find_all(
            By.XPATH, '//div[@data-assignment-type="homework" and '
                      'not(contains(@class, "is-published") or (@draggable="true"))]')
        num = len(drafts)
        while num > 0:
            draft = self.teacher.find(
                By.XPATH, '//div[@data-assignment-type="homework" and '
                          'not(contains(@class, "is-published") or (@draggable="true"))]')
            draft.click()
            delete_button = self.teacher.wait.until(
                expect.element_to_be_clickable(
                    (By.XPATH, '//button[contains(@class,"delete-link")]')
                )
            )
            self.teacher.scroll_to(delete_button)
            sleep(1)
            delete_button.click()
            self.teacher.find(
                By.XPATH, '//button[contains(text(),"Yes")]'
            ).click()
            sleep(3)
            self.teacher.driver.refresh()
            num -= 1

    @pytest.mark.skipif(str(3) not in TESTS, reason='Excluded')
    def test_clean_up_external(self):
        # draft external cleanup
        drafts = self.teacher.find_all(
            By.XPATH,
            '//div[@data-assignment-type="external" and not(contains(@class, "is-published") or (@draggable="true"))]')

        # published external cleanup
        drafts = self.teacher.find_all(
            By.XPATH,
            '//div[@data-assignment-type="homework" and '
            'contains(@class, "is-published") and not(@draggable="true")]'
        )
        num = len(drafts)
        while num > 0:
            draft = self.teacher.find(
                By.XPATH,
                '//div[@data-assignment-type="external" and '
                'not(contains(@class, "is-published") or (@draggable="true"))]')
            draft.click()
            delete_button = self.teacher.wait.until(
                expect.element_to_be_clickable(
                    (By.XPATH, '//button[contains(@class,"delete-link")]')
                )
            )
            self.teacher.scroll_to(delete_button)
            sleep(1)
            delete_button.click()
            self.teacher.find(
                By.XPATH, '//button[contains(text(),"Yes")]'
            ).click()
            sleep(3)
            self.teacher.driver.refresh()
            num -= 1
        self.teacher.find(
            By.CSS_SELECTOR, '.calendar-header-control.next'
        ).click()
        sleep(5)
        drafts = self.teacher.find_all(
            By.XPATH, '//div[@data-assignment-type="external" and '
                      'not(contains(@class, "is-published") or (@draggable="true"))]')
        num = len(drafts)
        while num > 0:
            draft = self.teacher.find(
                By.XPATH, '//div[@data-assignment-type="external" and '
                          'not(contains(@class, "is-published") or (@draggable="true"))]')
            draft.click()
            delete_button = self.teacher.wait.until(
                expect.element_to_be_clickable(
                    (By.XPATH, '//button[contains(@class,"delete-link")]')
                )
            )
            self.teacher.scroll_to(delete_button)
            sleep(1)
            delete_button.click()
            self.teacher.find(
                By.XPATH, '//button[contains(text(),"Yes")]'
            ).click()
            sleep(3)
            self.teacher.driver.refresh()
            num -= 1


    @pytest.mark.skipif(str(4) not in TESTS, reason='Excluded')
    def test_clean_up_event(self):
        # draft event cleanup
        drafts = self.teacher.find_all(
            By.XPATH,
            '//div[@data-assignment-type="event" and not(contains(@class, "is-published") or (@draggable="true"))]')

        # published reading cleanup
        drafts = self.teacher.find_all(
            By.XPATH,
            '//div[@data-assignment-type="homework" and '
            'contains(@class, "is-published") and not(@draggable="true")]'
        )
        num = len(drafts)
        while num > 0:
            draft = self.teacher.find(
                By.XPATH,
                '//div[@data-assignment-type="event" and '
                'not(contains(@class, "is-published") or (@draggable="true"))]')
            draft.click()
            delete_button = self.teacher.wait.until(
                expect.element_to_be_clickable(
                    (By.XPATH, '//button[contains(@class,"delete-link")]')
                )
            )
            self.teacher.scroll_to(delete_button)
            sleep(1)
            delete_button.click()
            self.teacher.find(
                By.XPATH, '//button[contains(text(),"Yes")]'
            ).click()
            sleep(3)
            self.teacher.driver.refresh()
            num -= 1
        self.teacher.find(
            By.CSS_SELECTOR, '.calendar-header-control.next'
        ).click()
        sleep(5)
        drafts = self.teacher.find_all(
            By.XPATH, '//div[@data-assignment-type="event" and '
                      'not(contains(@class, "is-published") or (@draggable="true"))]')
        num = len(drafts)
        while num > 0:
            draft = self.teacher.find(
                By.XPATH, '//div[@data-assignment-type="event" and '
                          'not(contains(@class, "is-published") or (@draggable="true"))]')
            draft.click()
            delete_button = self.teacher.wait.until(
                expect.element_to_be_clickable(
                    (By.XPATH, '//button[contains(@class,"delete-link")]')
                )
            )
            self.teacher.scroll_to(delete_button)
            sleep(1)
            delete_button.click()
            self.teacher.find(
                By.XPATH, '//button[contains(text(),"Yes")]'
            ).click()
            sleep(3)
            self.teacher.driver.refresh()
            num -= 1

