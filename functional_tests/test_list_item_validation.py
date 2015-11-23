from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank

        # She tries again with some text for the item, which now works

        # Perversely, she now decides to submit a second blank list item

        # She receives a similar warning on the list page

        # And she can correct it by filling some text in
        self.fail('write me!')

        # Satisfied, they both go back to sleep

# if __name__ == '__main__':
#     # launches the unittest test runner, which will
#     # automatically find test classes and methods in the file
#     # and run them. 
#     # warnings='ignore' suppresses a superfluous ResourceWarning
#     # which was being emitted at the time of writing. 
#     unittest.main(warnings='ignore')