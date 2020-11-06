from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
import random
import sys


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()


class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        #self.driver = webdriver.Chrome()
        self.driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.
        self.follower = []
        self.follows = []

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        accept_btn = driver.find_element_by_css_selector("button.aOOlW.bIiDR")
        accept_btn.click()
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(4)
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        notice_btn = driver.find_element_by_css_selector("button.aOOlW.HoLwm")
        if(notice_btn): notice_btn.click()
        time.sleep(2)      
        
    def getSpecificFollower(self,account):
        driver = self.driver
        account_url = "https://www.instagram.com/" + str(account) + "/"
        driver.get(account_url)
        time.sleep(3)
        #find followers button
        abonent_btn = driver.find_elements_by_tag_name('a') 
        for elem in abonent_btn: 
            if '/followers/' in elem.get_attribute('href'):
                abonent_btn = elem
        abonent_btn.click()
        time.sleep(5)
        #add scroll agent here
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='isgrP']")))
        toScrollElement = driver.find_element_by_xpath("//div[@class='isgrP']")
        toScrollElement.click()
        seconds = 0
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.PAGE_DOWN)
        actions.perform()
        time.sleep(1)
        #we have to click one more time since the element looses focus the first time for some unknown reason
        toScrollElement.click()
        time.sleep(1)
        #too lazy to program a check if the list is scrolled to completion, so we just scroll for a long time
        while seconds < 150:                       
            actions.send_keys(Keys.PAGE_DOWN)
            actions.perform()
            seconds += 1
            time.sleep(1)
        
        followerList = driver.find_element_by_css_selector("ul.jSC57._6xe7A")
        followsNames = followerList.find_elements_by_tag_name('a')
        print("Follower list:")        
        for elem in followsNames:
            followName = elem.get_attribute("title")
            #we get some empty results, so filter them
            if(followName != ""):
                print(followName)
                self.follower.append(followName)
        with open("abonnenten.txt", "w") as f:
            for s in self.follower:
                f.write(str(s) +"\n")
        time.sleep(5)
        
    def getSpecificFollows(self,account):
        driver = self.driver
        account_url = "https://www.instagram.com/" + str(account) + "/"
        driver.get(account_url)
        time.sleep(10)
        abonent_btn = driver.find_elements_by_tag_name('a') 
        for elem in abonent_btn: 
            if '/following/' in elem.get_attribute('href'):
                abonent_btn = elem
        abonent_btn.click()
        time.sleep(2)
        #add scroll agent here
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='isgrP']")))
        toScrollElement = driver.find_element_by_xpath("//div[@class='isgrP']")
        toScrollElement.click()
        seconds = 0
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.PAGE_DOWN)
        actions.perform()
        time.sleep(1)
        toScrollElement.click()
        time.sleep(1)
        while seconds < 150:                       
            actions.send_keys(Keys.PAGE_DOWN)
            actions.perform()
            seconds += 1
            time.sleep(1)
            
        followsList = driver.find_element_by_css_selector("ul.jSC57._6xe7A")
        followsNames = followsList.find_elements_by_tag_name('a')
        print("Follows list:")
        for elem in followsNames:
            followName = elem.get_attribute("title")
            if(followName != ""):
                print(followName)
                self.follows.append(followName)
        #print(follwerList.get_attribute("innerHTML"))
        with open("abonniert.txt", "w") as f:
            for s in self.follows:
                f.write(str(s) +"\n")
        
        time.sleep(5)        
        
    def compareFollows(self):
        follows = self.follows
        follower = self.follower
        
        print("abonnenten ist ", len(follower))
        print("abonniert ist " , len(follows))

        print("abonniert die nicht in abonnenten sind:")
        new_list = []
        for element in follows:
            if element not in follower:
                print(element)
                new_list.append(element)
        print("das resultat ist: ", len(new_list))
        with open("resultat.txt", "w") as f:
            for s in new_list:
                f.write(str(s) +"\n")
        

if __name__ == "__main__":

    username = "USERNAME"
    password = "PASSWORD"
    
    account = "benksy"

    ig = InstagramBot(username, password)
    ig.login()
    ig.getSpecificFollower(account)
    ig.getSpecificFollows(account)
    ig.compareFollows()
    ig.closeBrowser()   