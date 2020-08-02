from tqdm import tqdm
import pandas as pd
from selenium import webdriver
import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import re
from newspaper import Article
import datetime
from dateutil import parser
from selenium.common.exceptions import NoSuchElementException

main_df=pd.DataFrame()

driver = webdriver.Chrome(r'C:\Users\user\Downloads\chromedriver_win32 (3)/chromedriver.exe')#,chrome_options= chrome_options)
driver.get('https://www.moneycontrol.com/india')


driver.find_element_by_class_name('txtsrchbox').send_keys('yes Bank')
driver.find_element_by_class_name('btn_black').click()
time.sleep(3)

driver.find_element_by_xpath('//*[@id="sec_quotes"]/div[2]/div/div[1]/div[3]/div/div/nav/div/ul/li[7]/a').click()
time.sleep(5)
driver.find_element_by_xpath('//*[@id="sec_newsv"]/div/div/div[1]/div/div/div/div[3]/div[2]/a').click()

#default_handle = driver.current_window_handle
#window_before = driver.window_handles[0]
handles = list(driver.window_handles)
#        time.sleep(2)
#assert len(handles) > 1
#window_after = driver.window_handles[1]
#handles.remove(default_handle)
#        time.sleep(2)
#assert len(handles) > 0
##   
driver.switch_to.window(handles[2])
#driver.refresh()


#driver.find_element_by_xpath('//*[@id="sec_quotes"]/div[2]/div/div[1]/div[3]/div/div/nav/div/ul/li[7]').click()



#driver.refresh()




#driver.find_element_by_xpath('//*[@id="sec_newsv"]/div/div/div[1]/div/div/div/div[3]/div[2]/a').click()

#
# news_links=driver.find_elements_by_class_name('g_14bl')
#news_links=driver.find_elements_by_tag_name('a')
# news_links=driver.find_elements_by_xpath('//*[@id="mc_mainWrapper"]/div[3]/div[2]/div[3]/div[2]/div[2]/div/div[3]/div[1]/div[9]/div[2]')

#links=[i.get_attribute('href') for i in news_links]


#news links
# for i in range(2,9):
#     # i=2
#     driver.find_element_by_xpath('//*[@id="quickLinkPrc"]/table/tbody/tr/td[1]/ul/li[{}]/a'.format(i)).click()
#     x=driver.find_elements_by_tag_name('li')


#
# news = [i.text for i in x]
#links=[]

#
#href="/news/ipo-issues-open/yes-bank-fpo-subscribed-95-so-far-qib-remains-strongfinal-day_14047701.html"
#href in links1
#



#for page_num in range(2,20):
#    print(page_num)
#    page_url='http://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id=YB&scat=&pageno={}&next=0&durationType=M&Year=&duration=6&news_type='.format()

page_ele=driver.find_elements_by_tag_name('a')
links=[]
for i in page_ele:
    # print(i.text)
    try:
        n=i.get_attribute('href')
        links.append(n)
    except:
        continue


page_links=[i for i in links if re.search('http://www.moneycontrol.com/stocks/company_info/stock_news',str(i) )] #get all the hf links
page_links_new=[i  for i in page_links if len(i)>100]
company_name='yes bank'

all_spans = driver.find_elements_by_xpath("//a[@class='g_14bl']")
for span in all_spans:
    print(span.get_attribute('href'))
    
    
for page_link in page_links_new:
    
    dates_ele=driver.find_elements_by_class_name("a_10dgry")
    news_dates=[i.text for i in dates_ele]
    news_dates1=[i.split(' | ')[1] for i in news_dates]    
    news_links_ele_all=[]
#    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#    time.sleep(5)
    try:
        print('ok')
        time.sleep(2)
        
#        for numb in range(1,35):
#            print('going_well')
#            try:
#                news_links_ele=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="mc_mainWrapper"]/div[3]/div[2]/div[3]/div[2]/div[2]/div/div[3]/div[1]/div[{}]/div[2]/a'.format(numb))))
#                news_links_ele_all.append(news_links_ele[0])
#            except:
#                continue
#        driver.refresh()
#        time.sleep(10)
#        news_links_ele=driver.find_elements_by_css_selector('a.g_14bl')
        news_links_ele_all=driver.find_elements_by_xpath("//a[@class='g_14bl']") 
#        news_links_ele_all=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="mc_mainWrapper"]/div[3]/div[2]/div[3]/div[2]/div[2]/div/div[3]/div[1]/div[1]/div[2]/a')))
    except NoSuchElementException:
#        print(e)
#        time.sleep(10)
        print('entered exception')
        news_links_ele_all=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.g_14bl')))
#        news_links_ele=driver.find_elements_by_css_selector('a.g_14bl')
    
    all_news_links=[i.get_attribute('href') for i in news_links_ele_all]

    for num,single_link in enumerate(all_news_links):
#        single_link=all_news_links[6]
    #    driver.get(single_link)
        article = Article(single_link)
        article.download()
    #    article.html
        article.parse()
        news_story=article.text
        news_header=article.title
#        date_ele=driver.find_element_by_class_name('arttidate').text.split(':')[1][:-2]
        news_date=parser.parse(news_dates1[num]).strftime('%d-%m-%Y')
        news_df=pd.DataFrame([{'company_name':company_name,'news_date':news_date,'news_header':news_header,'news_story':news_story}])
        main_df=main_df.append(news_df).reset_index(drop=True)
        print('df appended')
    driver.get(page_link)
    
    
main_df.to_csv(r'C:\Users\user\Desktop\money_control\res/yes_bank_news.csv',index=False)







#x=driver.find_elements_by_tag_name('p')
#
#article=[i.text for i in x]






#
#driver.get(buisness_links[0])
#news=driver.find_elements_by_tag_name('a')
#
#article=[i.get_attribute('href') for i in news]
#article_str=[str(i) for i in article]
#news_story_links=[i for i in article_str if re.match('https://www.moneycontrol.com/news/business/',i) ] #get all the hf links
#
#
#for news_num in range(1,30):
#    news_num=5
#    driver.find_element_by_xpath('//*[@id="newslist-{}"]/h2/a'.format(news_num)).click()
#    story=driver.find_elements_by_id('article-main')
#    main_text=story[0].text
##    main_text.encode('utf-8')
#
#driver.get(by_class[13].text)
#article11=[i.get_attribute('href') for i in by_class]
#
#
#    
#        
#    
#
#
