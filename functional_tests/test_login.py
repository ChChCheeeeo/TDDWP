from selenium.webdriver.support.ui import WebDriverWait
from .base import FunctionalTest
import time

class LoginTest(FunctionalTest):

    def test_login_with_persona(self):
        # Edith goes to the awesome superlists site
        # and notices a "Sign in" link for the first time.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # A Persona login box appears
        # this does some waiting
        self.switch_to_new_window('Mozilla Persona')

        # Edith logs in with her email address
        ## Use mockmyid.com for test email
        # Rather than using a "real" email address and having to
        # click through their authentication screens,
        # use a "fake" provider. MockMyID is one; 
        #also check out Persona Test User. 
        self.browser.find_element_by_id(
            'authentication_email'
        ).send_keys('edith@mockmyid.com')
        self.browser.find_element_by_tag_name('id_button').click()

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # She can see that she is logged in
        # this does some waiting
        self.wait_for_element_with_id('logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('edith@mockmyid.com', navbar.text)

    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            # looking for a particular title
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail('could not find window')

    def wait_for_element_with_id(self, element_id):
        # good for when waiting for an element with a given ID to
        # appear on the page
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id)
        )