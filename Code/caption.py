import random
import os
import json
import subprocess
import requests
import PySimpleGUI as sg

class Caption:
    def __init__(self, og_caption, username, og_poster, caption_format):
        self.caption = og_caption
        self.username = username
        self.poster = og_poster
        self.caption_format = caption_format
    
    def get_description(self):
        with open(f"accounts/{self.username}/descriptions.txt", "r", encoding="utf-8") as f:
            descriptions = f.read().split("\n")
        
        return random.choice(descriptions)

    def get_credits(self):
        usernames = [username for username in self.caption.split() if "@" in username]

        for username in usernames:
            if username.strip("@") != self.poster:
                url = f"https://www.instagram.com/{username.strip('@')}/?__a=1"
                try: # if request error
                    json_data = requests.get(url).json()
                except:
                    return username
                
                try:  # check if username exists, else return unknown credit
                    json_data['graphql']
                    return username
                except KeyError:
                    return "unknown (DM for credit)"
                
        return "unknown (DM for credit)"

    def get_hashtags(self):
        path = os.path.join("accounts/" + self.username, "hashtags.json")
        tiers = ["bottom", "middle", "top"]
        
        with open(path, "r") as f:
            file_nums = json.load(f)["num_hashtags"].split()
            num_hashtags = {
                "bottom": int(file_nums[0]),
                "middle": int(file_nums[1]),
                "top": int(file_nums[2])
            }

        # check if there are enough hashtags in file
        with open(path, "r") as f:
             file_hashtags = json.load(f)
             for hashtag_tier in file_hashtags:
                 if len(file_hashtags[hashtag_tier].split()) < num_hashtags.get(hashtag_tier, 0):
                     sg.popup_error(f"You have less '{hashtag_tier}' tier hashtags in hashtags.json than configured in caption.py line 32-34. Please change them and press OK.")

        hashtag_str = ""

        # opens the file and gets all the hashtags
        with open(path, "r") as f:
            json_f = json.load(f)
            for tier in tiers:
                hashtags = json_f[tier].replace("#", "").split()  # gets the hashtags from tier and converts to list
                scoped_hashtags = []
                while len(scoped_hashtags) < num_hashtags[tier]:
                    choice = random.choice(hashtags)
                    if choice not in scoped_hashtags:
                        scoped_hashtags.append(choice)
                hashtag_str += " #" + " #".join(scoped_hashtags)

            return hashtag_str[1:]

    def create_caption(self):
        variables = {
        "description": self.get_description(),
        "credit": self.get_credits(),
        "hashtags": self.get_hashtags(),
        "self_username": self.username
        }
        
        return self.caption_format.format(**variables)

def get_caption(og_caption, username, og_poster, caption_format):
    cap = Caption(og_caption, username, og_poster, caption_format)

    return cap.create_caption()

def caption_setup(username):
    sg.theme('Dark')

    if os.path.exists(os.path.join("accounts/" + username, "caption.txt")):
        with open(os.path.join(username, "caption.txt"), "r", encoding="utf-8") as f:
            default_text = f.read()
    else:
        default_text = """{description}
FOLLOW 👉👉 @{self_username} 👈👈 FOR MORE
__
📸: {credit}
__
This photo is for entertainment purposes only, if the owner would like the photo taken down or if credit was not given please DM @{self_username} and l will sort it out ASAP!
__
{hashtags}"""

    layout = [
        [sg.Text("Enter the format for your caption (emojis do not actually look like this):")],
        [sg.Text("{description} = random line from the descriptions you configured.\n{credit} = username of the account the post is taken from (if none is found, it will be 'unknown'.\n{hashtags} = generated hashtags from those you configured.\n{self_username} = your IG account username.\n", text_color="#f03434")],
        [sg.Multiline(default_text=default_text, size=(100,20), key="-CAPTION-")],
        [sg.Button("Save")]]

    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        if event == "Save":
            with open (f"accounts/{username}/caption.txt", "w", encoding="utf-8") as f:
                if check_legal_caption(values["-CAPTION-"]):
                    f.write(values["-CAPTION-"])
                    sg.popup("Saved caption!")
                else:
                    sg.popup("Not valid!")
                
                window.close()
        

    window.close()

def check_legal_caption(string):
    try:
        variables = {
        "description": 1,
        "credit": 2,
        "hashtags": 3,
        "self_username": 4
        }

        string.format(**variables)

        return True
    except KeyError:
        return False

if __name__ == "__main__":
    pass