from selenium import webdriver

class Unfollower:
    def __init__(self, username):
        self.username = username
        self.driver = webdriver.Firefox()
    
    def login(self):
        if os.path.exists(os.path.join(f"Code/{self.username}", "cookies.pkl")): # check if cookies are already stored
            pass
        else:
            pass
    


if __name__ == "__main__":
    unfollow("cutelovingdogs")
