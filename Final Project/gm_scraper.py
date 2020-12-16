from googlemaps import GoogleMapsReview
import csv
import time

'''
def csv_writer(source_field, path='review_data/', outfile='gm_reviews.csv'):

    #source_field: to determine whether extra category in csv is needed.

    #HEADER = ['caption', 'rating']
    HEADER_SOURCE = ['caption', 'rating']

    targetfile = open(path + outfile, mode='w', encoding='utf-8', newline='\n')
    writer = csv.writer(targetfile, quoting=csv.QUOTE_MINIMAL)
    header = HEADER_SOURCE
    
    writer.writerow(header)

    return writer
'''


SCRAPE_LIM = 500  # 每間店爬文的數量設定

scraper = GoogleMapsReview()

url = "https://www.google.com.tw/maps/place/McDonald's/@25.0535928,121.5754765,15z/data=!4m7!3m6!1s0x0:0x537de9a82818a5e1!8m2!3d25.0606848!4d121.5792507!9m1!1b1"
click_res = scraper.click_newest_bt(url)

all_review_res = []
if click_res == 'Success':
    #scraper.scroll_down()
    scrape_remaining = SCRAPE_LIM
    
    while scrape_remaining > 0:
        time.sleep(3)
        scraper.expand_all_reviews()

        res = scraper.read_reviews(scrape_remaining)
        scrape_remaining = res[1]
        if len(res[0]) == 0:
            break

        all_review_res += res[0]  # append the list

        scraper.scroll_down()

elif click_res == 'Fail':
    print('Oops! Something went wrong :(')

print(all_review_res)
print(len(all_review_res))

scraper.driver.close()
scraper.driver.quit()