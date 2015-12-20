#from django.test import LiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from .server_tools import reset_database

import sys

class FunctionalTest(StaticLiveServerTestCase):

    # LiveServerTestCase had certain limitations? Well, one is that it always
    # assumes you want to use its own test server. I still want to be able to do
    # that sometimes, but I also want to be able to selectively tell it not to
    # bother, and to use a real server instead.
    @classmethod
    def setUpClass(cls):
        # setUpClass is a similar method to setUp, also provided by unittest,
        # which is used to do test setup for the whole class—that means it only
        # gets executed once, rather than before every test method. This is where
        # LiveServerTestCase/StaticLiveServerTestCase usually starts up its test
        # server. 
        for arg in sys.argv:
            if 'liveserver' in arg:
                # Instead of just storing cls.server_url, we also store the
                # server_host and against_staging attributes if we detect the
                # liveserver command-line argument. 
                cls.server_host = arg.split('=')[1]
                cls.server_url = 'http://' + cls.server_host
                cls.against_staging = True
                return
        # if the for loop completes without finding a liveserver argument on the
        # command-line, we do the normal superclass setup, and use the normal
        # live_server_url.
        super().setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url


    @classmethod
    def tearDownClass(cls):
        if not cls.against_staging:
            super().tearDownClass()

    def setUp(self):
        if self.against_staging:
            #  resetting the server database in between each test.
            reset_database(self.server_host)
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()


    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id),
            'Could not find element with id {}. Page text was:\n{}'.format(
                element_id, self.browser.find_element_by_tag_name('body').text
            )
        )

    def wait_to_be_logged_in(self, email):
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)


    def wait_to_be_logged_out(self, email):
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)