import requests
import json
import datetime
import re
import time
import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import yaml

def get_media_type(string):
    if string == "GraphImage":
        return "Photo"
    elif string == "GraphVideo":
        return "Video"
    elif string == "GraphSidecar":
        return "Carousel"

def get_post_media(info):
    response = []
    
    # handle different paths for different media type
    if info["__typename"] == "GraphImage":
        media = info["display_url"]
        suffix = ".jpg"
        response.append({'media': media, 'suffix': suffix})
    elif info["__typename"] == "GraphVideo":
        media = info["video_url"]
        suffix = ".mp4"
        response.append({'media': media, 'suffix': suffix})
    elif info["__typename"] == "GraphSidecar":
        for content in info["edge_sidecar_to_children"]["edges"]:
            if content["node"]["__typename"] == "GraphImage":
                media = content["node"]["display_url"]
                suffix = ".jpg"
                response.append({'media': media, 'suffix': suffix})
            elif content["node"]["__typename"] == "GraphVideo":
                media = (content["node"]["video_url"])
                suffix = ".mp4"
                response.append({'media': media, 'suffix': suffix})

    return response


class InstagramScaper:
    def __init__(self):
        self.data = []
        self.account = ""
        self.driver = webdriver.Firefox()

    def get_json(self, url):
        counter = 0
        while (counter < 3):
            try:
                self.driver.get(url)
                el = self.driver.find_element_by_tag_name('body')

                return json.loads(el.text)
            except:
                counter += 1
                time.sleep(2)
        
        self.driver.get(url)
        el = self.driver.find_element_by_tag_name('body')

        return json.loads(el.text)

    def get_id(self, username):
        url = f"https://www.instagram.com/web/search/topsearch/?context=user&count=0&query={username}"
        respJSON = self.get_json(url)

        username_id = str(respJSON['users'][0].get("user").get("pk"))
        return username_id

    def get_user_info(self, id, max_id):
        scrape_url = 'https://www.instagram.com/graphql/query/?query_hash=003056d32c2554def87228bc3fd9668a&variables={"id":' + id + ',"first":12,"after":"' + max_id + '"}'

        return self.get_json(scrape_url)

    def get_user_posts(self, account, num_posts):
        self.account = account
        account_id = self.get_id(account)
        self.data = []

        max_id = ""
        counter = 0
        while len(self.data) < num_posts:
            counter += 1
            sg.one_line_progress_meter(f"Scraping posts of user {account}...", counter*12, num_posts, f"Scraping posts of user {account}...", orientation='h')
            info = self.get_user_info(account_id, max_id)  # get targeted user's posts

            # parse through all posts
            try:
                posts = [post['node'] for post in info["data"]["user"]["edge_owner_to_timeline_media"]["edges"]]
            except KeyError:
                return {"error": True, "response": "An error has occurred. Please try again later.", "code": 3}
            for post in posts:
                likes = post["edge_media_preview_like"]["count"]
                
                link = "https://instagram.com/p/{}/".format(post['shortcode'])
                
                media_type = get_media_type(post["__typename"])
                
                media = get_post_media(post)
                
                try:
                    caption = post["edge_media_to_caption"]["edges"][0]["node"]["text"]
                except IndexError:
                    caption = ""

                post_dict = {
                    "link": link,
                    "likes": likes,
                    "media_type": media_type,
                    "caption": caption,
                    "media": media,
                    "op": self.account
                                }
                self.data.append(post_dict)
            
            if not info["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]:  # check if more posts are available
                break
            
            max_id = info["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]  # get max id for next batch

            time.sleep(1)
        
        self.data = self.data[:num_posts]  # removes last posts to match number of posts requested
        self.sort_posts()

    def sort_posts(self):
        # reverse = True (Sorts in descending order)
        # key is set to sort using second element of
        # sublist lambda has been used
        sub_li = self.data
        sub_li.sort(key=lambda x: int(x["likes"]), reverse=True)
        self.data = sub_li
    
    def handle_login(self):
        self.driver.get("https://www.instagram.com/")
        with open("creds.yml", "r") as f:
            y = yaml.load(f, Loader=yaml.FullLoader)

        time.sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input").send_keys(y["username"])
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input").send_keys(y["password"])
        time.sleep(0.2)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button").click()
        time.sleep(5)


def scrape(acc, num_posts):
    scraper = InstagramScaper()
    scraper.handle_login()
    scraper.get_user_posts(acc, num_posts)
    scraper.driver.close()
    return scraper.data

if __name__ == "__main__":
    pass