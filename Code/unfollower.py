from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import pickle

class Unfollower:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()
        self.following_accounts = []
    
    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/?hl=en")
        time.sleep(3)
        try:
            user_xpath = '/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[1]/div/label/input'
            user_button = self.driver.find_element_by_xpath(user_xpath)
            user_button.clear()
            time.sleep(2)
            user_button.send_keys(self.username)
            time.sleep(2)

            pass_xpath = '/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label/input'
            pass_button = self.driver.find_element_by_xpath(pass_xpath)
            pass_button.clear()
            time.sleep(2)
            pass_button.send_keys(self.password)
            time.sleep(2)

            login_xpath = '/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button/div'
            login_button = self.driver.find_element_by_xpath(login_xpath)
            login_button.click()
            time.sleep(2)
        except:
            user_xpath = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input'
            user_button = self.driver.find_element_by_xpath(user_xpath)
            user_button.clear()
            time.sleep(2)
            user_button.send_keys(self.username)
            time.sleep(2)

            pass_xpath = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input'
            pass_button = self.driver.find_element_by_xpath(pass_xpath)
            pass_button.clear()
            time.sleep(2)
            pass_button.send_keys(self.password)
            time.sleep(2)

            login_xpath = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button'
            login_button = self.driver.find_element_by_xpath(login_xpath)
            login_button.click()
            time.sleep(2)
    
    def find_followings(self): # this functions finds the accounts who are followed by us
        self.driver.get(f"https://www.instagram.com/{self.username}/")
        time.sleep(1)
        buttons = self.driver.find_elements_by_xpath("//a[@class='-nal3 ']")
        
        following_button = [button for button in buttons if 'following' in button.get_attribute('href')]
        following_button[0].click()
        time.sleep(2)
        following_window = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        following_number = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span").text
        counter = 0
        while counter < int(following_number) / 5:  # scrolls 5 account each time approximately, if in your browser it differs, change the value with the passed account per scrolling
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', following_window)
            counter += 1
            time.sleep(0.2)
        self.following_accounts = self.driver.find_elements_by_class_name("_0imsa")
        self.following_accounts = [account.get_attribute('title') for account in self.following_accounts]  # the array of the accounts who we follow

    def find_target_users(self):
        self.find_followings()
        print(self.following_accounts)

if __name__ == "__main__":
    unfollower = Unfollower("luxurymasterclub", "Messi#10")
    
    unfollower.login()
    time.sleep(3)
    unfollower.find_followings()
