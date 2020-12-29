from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium
from bs4 import BeautifulSoup
import time

WAIT = 0.3
RETRY_LIM = 20


class GoogleMapsReview():

    def __init__(self):
        self.driver = self.set_driver_options()

    def set_driver_options(self):
        option = Options()

        option.add_argument('--window-size=1920,1080')
        option.add_argument("--disable-notifications")
        option.add_argument("--lang=en-GB")

        driver = webdriver.Chrome(chrome_options=option)
        driver.maximize_window()
        return driver

    def click_newest_bt(self, url):
        '''
        First click on "Sort"
        Then click on "Newest"
        '''
        #sort_bt_xpath = '//button[@aria-label=\'排序評論\'][@data-value=\'排序\']'

        self.driver.get(url)
        score = self.get_google_score()
        totalcnt = self.get_total_review_count()
        time.sleep(WAIT)
        for i in range(RETRY_LIM):
            try:
                allreviews_bt_xpath = '//button[@jsaction=\'pane.rating.moreReviews\'][@class=\'widget-pane-link\']'
                allreviews_bt = self.driver.find_element_by_xpath(allreviews_bt_xpath)
                allreviews_bt.click()
                break
            except:
                time.sleep(WAIT)
                errormsg = 'Cannot find reviews'
                continue

        if i == RETRY_LIM-1:
            return errormsg, -1, -1

        return 'Success', totalcnt, score

    def scroll_down(self):
        scrollable_xpath = "//div[@class=\'section-layout section-scrollbox scrollable-y scrollable-show\']"
        for i in range(RETRY_LIM):
            try:
                scrollable = self.driver.find_element_by_xpath(scrollable_xpath)
                self.driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollHeight', scrollable)
            except:
                time.sleep(WAIT)
                continue

    def expand_all_reviews(self):
        '''
        expands long reviews which require clicking on "More"
        '''
        for i in range(RETRY_LIM):
            try:
                all_expands_xpath = "//button[@class=\'section-expand-review blue-link\']"
                all_expands = self.driver.find_elements_by_xpath(
                    all_expands_xpath)  # returns a list
                time.sleep(0.5)
            except:
                time.sleep(WAIT)
                continue

        if len(all_expands) > 0:
            for expand in all_expands:
                expand.click()
            time.sleep(0.5)

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
            # Clean up text and get rating score
            raw = review.find('span', class_='section-review-text').text
            parsed = raw.replace('(原始評論)', '').replace('(由 Google 提供翻譯)', '')
            parsed = parsed.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
            rating = float(review.find(
                'span', class_='section-review-stars')['aria-label'].split(' ')[1])
            # print(parsed, rating) # <<<<<<<<<<<<< 印出來自己看看是啥

            parsed_reviews.append((parsed, rating))  # 存進去list的東西是 tuple
            if remaining <= 0:
                return parsed_reviews, remaining

        return parsed_reviews, remaining

    def get_total_review_count(self):
        count = 100000
        for i in range(RETRY_LIM):
            try:
                time.sleep(0.2)
                count_xpath = "//span[@class=\'reviews-tap-area reviews-tap-area-enabled\']"
                count = self.driver.find_element_by_xpath(count_xpath)
                count = int(count.text.split(' ')[0])
                break
            except:
                time.sleep(WAIT)
                continue
        if type(count) != int:
            count = 10000
        return count

    def get_google_score(self):
        for i in range(RETRY_LIM):
            try:
                time.sleep(0.2)
                score_xpath = "//div[@class=\'gm2-display-2\'][@jsan=\'7.gm2-display-2\']"
                score = self.driver.find_element_by_xpath(score_xpath)
                score = float(score.text)
                #print(score)
                break
            except:
                time.sleep(WAIT)
                continue
        if type(score) != float:
            #print('nope..............')
            score = -1
        return score

