from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

import pandas as pd
import json, re

try:
    linkedin_email = os.environ['LINKEDIN_EMAIL']
    linkedin_password = os.environ['LINKEDIN_PASSWORD']
except:
    with open('linkedin.json') as f:
        data = json.load(f)
        linkedin_email = data['LINKEDIN_EMAIL']
        linkedin_password = data['LINKEDIN_PASSWORD']

global students
students = pd.read_csv('students.csv')

global feed_url
feed_url = "https://www.linkedin.com/feed/"

def get_soup(driver, url):
	'''
	Helper function to get soup from a live url, as opposed to a local copy
	INPUT:
	-url: str
	OUTPUT: soup object
	'''
	driver.get(url)
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	return soup

def search_for_student(driver, name, school=' galvanize'):
    """
    This function uses the selenium web driver object to search using text input box at the top of feed page. search string is the name of a student + the name of the school at the time they attended, in this case either galvanize or zipfian. Returns a selenium element object called search_results.

    inputs: object driver, string name, string school
    return: object search_results
    """
    driver.get(feed_url)
    sleep(5)
    search = driver.find_element_by_class_name('ember-text-field')
    search.click()
    search.send_keys(name + school)
    button = driver.find_element_by_class_name('nav-search-button')
    button.click()
    sleep(5)
    search_results = driver.find_elements_by_class_name('search-result__wrapper')
    return search_results

def get_students_data(driver):

    for name in students.name[:5]:
        search_results = search_for_student(driver, name)
        try:
            link = search_results[0].find_element_by_css_selector('span.name')
            print("'{}' a match".format(name + ' galvanize'))
            link.click()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        except IndexError:
            search_results = search_for_student(driver, name, school=' zipfian')
            try:
                link = search_results[0].find_element_by_css_selector('span.name')
                print("'{}' a match".format(name + ' zipfian'))
                link.click()
                soup = BeautifulSoup(driver.page_source, 'html.parser')
            except IndexError:
                pass
        if soup:
            student = OrderedDict()
            student['name'] = name
            student['graduated']




class LinkedInScraper(object):
    def __init__(self, linkedin_email, linkedin_password):
        self.linkedin_email = linkedin_email
        self.linkedin_password = linkedin_password
        self.driver = None

    def log_in_linkedin(self):
        """
        The log_in_linkedin method uses a selenium webdriver to open and maintain a secure connect with LinkedIn. It returns the driver object.
        Input: None
        Output: webdriver object
        """
        chromeOptions = webdriver.ChromeOptions()
        # prefs = {"profile.managed_default_content_settings.images":2}
        # chromeOptions.add_experimental_option("prefs",prefs)

        print("logging in...")
        print("")
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        url = "https://www.linkedin.com/"
        driver.get(url)
        user = driver.find_element_by_name('session_key')
        user.click()
        user.send_keys(self.linkedin_email)
        pwrd = driver.find_element_by_name('session_password')
        pwrd.click()
        pwrd.send_keys(self.linkedin_password)
        driver.find_element_by_id('login-submit').click()
        sleep(10)
        print("complete!")
        return driver

    def main(self):
        self.driver = self.log_in_linkedin()


if __name__ == '__main__':
    scraper = LinkedInScraper(linkedin_email, linkedin_password)
    scraper.main()
    get_students_data(scraper.driver)
