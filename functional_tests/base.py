#from django.test import LiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from pyvirtualdisplay import Display
from .server_tools import reset_database
from django.conf import settings
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


import sys

import os
from datetime import datetime
import time

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)
DEFAULT_WAIT = 5
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


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
            self.display = Display(visible=0, size=(800, 600))
            self.display.start()
            self.binary = FirefoxBinary('/usr/bin/firefox', log_file=sys.stdout)
            self.browser = webdriver.Firefox(firefox_binary=self.binary)
        else:
            self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(DEFAULT_WAIT)

    def tearDown(self):
            if self._test_has_failed():
                if not os.path.exists(SCREEN_DUMP_LOCATION):
                    os.makedirs(SCREEN_DUMP_LOCATION)
                for ix, handle in enumerate(self.browser.window_handles):
                    self._windowid = ix
                    self.browser.switch_to_window(handle)
                    self.take_screenshot()
                    self.dump_html()
            self.browser.quit()
            if self.against_staging:
                self.display.stop()
            super().tearDown()

    def _test_has_failed(self):
        # for 3.4. In 3.3, can just use self._outcomeForDoCleanups.success:
        for method, error in self._outcome.errors:
            if error:
                return True
        return False

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )


    def wait_for(self, function_with_assertion, timeout=DEFAULT_WAIT):
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    return function_with_assertion()
                except (AssertionError, WebDriverException):
                    time.sleep(0.1)
            # one more try, which will raise any errors if they are outstanding
            return function_with_assertion()


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


    def create_pre_authenticated_session(self, email):
        if self.against_staging:
            session_key = create_session_on_server(self.server_host, email)
        else:
            session_key = create_pre_authenticated_session(email)
        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))