    # Page patterns involves having objects represent different pages on
    # your site, and to be the single place to store information about how
    # to interact with them.
    # The idea behind the Page pattern is that it should capture all the
    # information about a particular page in your site, so that if, later, you want
    # to go and make changes to that page—even just simple tweaks to its HTML layout
    # for example—you have a single place to go and look for to adjust your functional
    # tests, rather than having to dig through dozens of FTs.
class HomePage(object):
    # Page objects for the home page
    def __init__(self, test):
        # initialize with an object that represents the current test.
        # so it can make assertions, access the browser instance via
        # self.test.browser, and use the wait_for function.
        self.test = test


    def go_to_home_page(self):
        # Most Page objects have a "go to this page" function.
        # It implements the interaction/wait pattern
        # First get the page URL
        # then wait for a known element on the home page.
        self.test.browser.get(self.test.server_url)
        self.test.wait_for(self.get_item_input)
        # Returning self is just a convenience.
        # It enables method chaining
        return self


    def get_item_input(self):
        return self.test.browser.find_element_by_id('id_text')


    def start_new_list(self, item_text):
        # Function starts a new list.
        # Go to the home page
        # find the input box
        # send the new item text to it and a carriage return.
        # Use a wait to check that the interaction has completed
        # but the wait is actually on a different Page object (ListPage)
        self.go_to_home_page()
        inputbox = self.get_item_input()
        inputbox.send_keys(item_text + '\n')
        list_page = ListPage(self.test)
        # Use ListPage'swait_for_new_item_in_list and specify the expected
        # text of the item, and its expected position in the list
        list_page.wait_for_new_item_in_list(item_text, 1)
        # return the list_page object to the caller
        # because they will probably find it useful
        return list_page


class ListPage(object):

    def __init__(self, test):
        self.test = test


    def get_list_table_rows(self):
        return self.test.browser.find_elements_by_css_selector(
            '#id_list_table tr'
        )


    def wait_for_new_item_in_list(self, item_text, position):
        expected_row = '{}: {}'.format(position, item_text)
        self.test.wait_for(lambda: self.test.assertIn(
            expected_row,
            [row.text for row in self.get_list_table_rows()]
        ))

    def get_share_box(self):
        return self.test.browser.find_element_by_css_selector(
            'input[name=email]'
        )


    def get_shared_with_list(self):
        return self.test.browser.find_elements_by_css_selector(
            '.list-sharee'
        )


    def share_list_with(self, email):
        self.get_share_box().send_keys(email + '\n')
        self.test.wait_for(lambda: self.test.assertIn(
            email,
            [item.text for item in self.get_shared_with_list()]
        ))