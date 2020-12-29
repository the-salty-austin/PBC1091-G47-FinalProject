from googlemaps import GoogleMapsReview
import csv
import time
import logging

SCRAPE_LIM = 100  # 每間店爬文的數量設定
START = 99
STOP = 105

scraper = GoogleMapsReview()
#url = "https://www.google.com.tw/maps/place/McDonald's/@25.0535928,121.5754765,15z/data=!4m7!3m6!1s0x0:0x537de9a82818a5e1!8m2!3d25.0606848!4d121.5792507!9m1!1b1"
with open('cleaned_urls.csv', mode='r', encoding='utf-8') as urls_file:
    # args.i: file name?
    for i, out in enumerate(urls_file):
        try:
            if out.startswith('Center at') or i == 0 or i<=START-1 or i>=STOP:
                continue
            out = out.split(',')

            url = ''
            for idx, urlpart in enumerate(out[0:-3]):
                if idx > 0:
                    url += ','+urlpart
                else:
                    url += urlpart

            urllen = len(url)
            url = url[1:urllen-2]  # remove qutation mark from csv
            category = out[-3]
            price = out[-2]
            name = out[-1].replace('"','').replace('\n','')

            # click_res: [0] Success? [1] total count of review
            click_res = scraper.click_newest_bt(url)

            all_review_res = []
            if click_res[0] == 'Success':
                
                scrape_remaining = SCRAPE_LIM if click_res[1] > SCRAPE_LIM else click_res[1]
                print(f"At {i}, Found: {click_res[1]} Remain: {scrape_remaining}",end=' >>> ')

                google_score = click_res[2]
                
                while True:
                    scraper.expand_all_reviews()

                    res = scraper.read_reviews(scrape_remaining)
                    scrape_remaining = res[1]

                    all_review_res += res[0]  # append the list

                    if scrape_remaining <= 0:
                        break

                    scraper.scroll_down()

            elif click_res[0] == 'Cannot find reviews':
                print(f'Something went wrong at {i}: Reviews Not Found')
                continue

            fname = './review_data/'+str(i)+'.csv'
            with open(fname, mode='w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([name, category, google_score, price])
                for review in all_review_res:
                    csv_writer.writerow([review[0].replace('\n', '').replace('"', ''),review[1]])
            
            #print(all_review_res)
            print(f'review length: {len(all_review_res)}')
        except:
            print(f'Something went wrong at i={i}')
            continue

scraper.driver.close()
scraper.driver.quit()