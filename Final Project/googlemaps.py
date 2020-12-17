from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expt_cond
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

WAIT_LIM = 10
RETRY_LIM = 5

class GoogleMapsReview():

    def __init__(self):
        self.driver = self.set_driver_options()

    def set_driver_options(self):
        option = Options()
        
        option.add_argument('--window-size=1920,1080')
        option.add_argument("--disable-notifications")
        option.add_argument("--lang=en-GB")
        
        driver = webdriver.Chrome(chrome_options = option)
        driver.maximize_window()
        return driver

    def click_newest_bt(self, url):
        '''
        First click on "Sort"
        Then click on "Newest"
        '''
        sort_bt_xpath = '//button[@aria-label=\'Sort reviews\'][@data-value=\'Sort\']'

        self.driver.get(url)
        wait = WebDriverWait(self.driver, WAIT_LIM)

        clicked = False
        for attempt in range(RETRY_LIM):
            try:
                sort_bt = wait.until(expt_cond.element_to_be_clickable((By.XPATH,sort_bt_xpath)))
                sort_bt.click()
                #print('sort clicked')
                clicked = True
                time.sleep(3)  # wait page to load
            except:
                clicked = False
                continue

            if clicked:
                break
            elif attempt==RETRY_LIM and not clicked:
                return 'Fail'

        newest_bt_xpath = "//li[@role=\'menuitemradio\']"
        newest_bt = self.driver.find_elements_by_xpath(newest_bt_xpath)[1]
        newest_bt.click()
        #print('newest clicked')
        time.sleep(3)  # wait page to load
        return 'Success'

    def scroll_down(self):
        scrollable_xpath = "//div[@class=\'section-layout section-scrollbox scrollable-y scrollable-show\']"
        scrollable = self.driver.find_element_by_xpath(scrollable_xpath)
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable)

    def expand_all_reviews(self):
        '''
        expands long reviews which require clicking on "More"
        '''
        all_expands_xpath = "//button[@class=\'section-expand-review blue-link\']"
        all_expands = self.driver.find_elements_by_xpath(all_expands_xpath)  # returns a list
        
        if len(all_expands) > 0:
            for expand in all_expands:
                expand.click()
            time.sleep(1.5)

    def read_reviews(self, remaining):
        '''
        returns a tuple:
        [0] parsed_reviews (list containing tuples) tuple -> (review, rating)
        [1] remaining
        '''
        response = BeautifulSoup(self.driver.page_source, 'html.parser')
        reviews = response.find_all('div', class_='section-review-content')

        parsed_reviews = list()
        for review in reviews:
            remaining -= 1
            if remaining < 0:
                return parsed_reviews, remaining
            
            # Clean up text and get rating score
            raw = review.find('span', class_='section-review-text').text
            parsed = raw.replace('(Original)','').replace('(Translated by Google)', '')
            parsed = parsed.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
            rating = float(review.find('span', class_='section-review-stars')['aria-label'].split(' ')[1])
            
            #print(parsed, rating) # <<<<<<<<<<<<< 印出來自己看看是啥
            
            parsed_reviews.append((parsed, rating))  # 存進去list的東西是 tuple

        return parsed_reviews, remaining

    