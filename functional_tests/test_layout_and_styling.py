from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            # assertAlmostEqual helps us to deal with rounding errors
            # by letting us specify that we want our arithmetic to work
            # to within plus or minus five pixels
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        # self.get_item_input_box().send_keys('testing\n')
        inputbox.send_keys('testing\n')
        inputbox = self.get_item_input_box()

        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )