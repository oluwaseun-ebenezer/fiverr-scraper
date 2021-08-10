from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os

class Fiverr:

    query = '?ref=seller_location%3ANG'

    def __init__(self,link):
        root_dir = 'Fiverr'
        try:
            os.mkdir(root_dir)
        except FileExistsError:
            pass

        self.link = link
        self.dir = f'{root_dir}/' + link[0].split('/')[-2]
        self.filename = link[0].split('/')[-1]
        
        try:
            os.mkdir(self.dir)
        except FileExistsError:
            pass
        
        return

    def scrape(self):

        usernames = []
        username_profile = []
        username_contact = []
        
        try:
            driver0 = webdriver.Firefox()
            driver0.get(f'{self.link[0]}{self.query}')

            tabs_sele = driver0.find_elements_by_xpath('//li[@class="page-number"]')

            tabs = []

            tabs.append('')
            for tab in tabs_sele:
                tabs.append(tab.text)

            driver0.quit()

            for tab in tabs:
                driver = webdriver.Firefox()
                driver.get(f'{self.link[0]}{self.query}&page={tab}')
                sellers = driver.find_elements_by_xpath('//div[@class="seller-name"]')
                for seller in sellers:
                    usernames.append(seller.text)
                    username_profile.append('https://www.fiverr.com/'+seller.text)
                    username_contact.append('https://www.fiverr.com/inbox/'+seller.text)
                
                driver.quit()
        except Exception:
            pass
        finally:
            usernames_pd = pd.DataFrame({'USERNAME': usernames, 'PROFILE': username_profile, 'CONTACT': username_contact})
            usernames_pd = usernames_pd.sort_values('USERNAME')


            usernames_pd.to_csv(f'{self.dir}/{self.filename}.csv')