from selenium import webdriver
import time
import os
import pickle

class Unfollower:
    def __init__(self, username, password, to_scrape):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()
        self.to_scrape = to_scrape
    
    def login(self):
        if os.path.exists(os.path.join(f"Code/{self.username}", "cookies.pkl")): # check if cookies are already stored
            cookies = pickle.load(open(os.path.join(f"Code/{self.username}", "cookies.pkl"), "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            
            self.driver.get("https://www.instagram.com")

        else:
            self.driver.get("https://www.instagram.com/accounts/login/?hl=en")
            time.sleep(1)
            try:
                user_xpath = '/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div[1]/div/label/input'
                user_button = self.driver.find_element_by_xpath(user_xpath)
                user_button.clear()
                time.sleep(2)
                user_button.send_keys(self.username)
                time.sleep(2)

                pass_xpath = '/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div[2]/div/label/input'
                pass_button = self.driver.find_element_by_xpath(pass_xpath)
                pass_button.clear()
                time.sleep(2)
                pass_button.send_keys(self.password)
                time.sleep(2)

                login_xpath = '/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div[3]'
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

            pickle.dump(self.driver.get_cookies(), open(os.path.join(f"Code/{self.username}", "cookies.pkl"), "wb"))
    

if __name__ == "__main__":
    unfollower = Unfollower("luxurymasterclub", "Messi#10", "cutelovingdogs")
    
    unfollower.login()
