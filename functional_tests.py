from selenium import webdriver

# assure ourselves that we understand what it’s doing:
# Starting a Selenium webdriver to pop up a real Firefox browser
# window
# Using it to open up a web page which we’re expecting to be served
# from the local PC
# Checking (making a test assertion) that the page has the word
# "Django" in its title

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title