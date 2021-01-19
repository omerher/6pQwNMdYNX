import pyautogui
import keyboard
import os
import time
import subprocess
import numpy as np
from datetime import datetime

# def click(cords):
#     x = cords[0]
#     y = cords[1]
#     pyautogui.click(x, y)

def click(path, confidence=0.9, grayscale=False):
    counter = 0
    while counter < 3:
        try:
            button = pyautogui.locateOnScreen(path, confidence=confidence, grayscale=grayscale)
            pyautogui.click(pyautogui.center(button))
            return
        except:
            time.sleep(5)
            pass
        counter += 1
    
    button = pyautogui.locateOnScreen(path, confidence=confidence, grayscale=grayscale)
    pyautogui.click(pyautogui.center(button))
    
    

# def uploader(caption, file_names, bb_enabled, path, username, multiple_accounts, fb_name, location):
#     # bb = bookmarks bar
#     if bb_enabled == "True":
#         bb_difference = 0
#     else:
#         bb_difference = 35
    
#     # coords for all buttons to be pressed
#     profile_select = (334, 172-bb_difference)
#     search_profile = (1588, 244-bb_difference)
#     unselect_all = (495, 730-bb_difference)
#     first_profile = (1630, 309-bb_difference)
#     view_btn = (811, 730-bb_difference)
#     create_post_btn = (111, 182-bb_difference)
#     instagram_feed_btn = (121, 227-bb_difference)
#     caption_location = (1200, 334-bb_difference)
#     location_pos = (1300, 500-bb_difference)
#     add_content = (1256, 740-bb_difference)
#     file_upload = (1270, 786-bb_difference)
#     address_bar = (748, 47)
#     file_names_cords = (900, 977)
    
    
#     # open new tab
#     url = "https://business.facebook.com/creatorstudio?tab=instagram_content_posts&mode=instagram&collection_id=all_pages&content_table=INSTAGRAM_POSTS"
#     os.startfile(url)
    
#     # click Create Post
#     time.sleep(4)
#     click(create_post_btn)

#     # click Instagram Feed
#     time.sleep(0.25)
#     click(instagram_feed_btn)

#     time.sleep(1.5)
#     if multiple_accounts:
#         click(search_profile)

#         time.sleep(0.6)
#         keyboard.write(fb_name)

#         time.sleep(0.75)
#         click(first_profile)

#     # enter caption
#     time.sleep(0.25)
#     click(caption_location)
#     time.sleep(0.3)
#     subprocess.run(['clip.exe'], input=caption.encode('utf-16'), check=True) 
#     keyboard.press_and_release('ctrl+v')

#     time.sleep(0.3)
#     click(location_pos)
#     time.sleep(0.2)
#     keyboard.write(location)
#     time.sleep(1)
#     keyboard.press_and_release("enter")
    
#     # click Add Content
#     time.sleep(0.5)
#     click(add_content)

#     # click From File Upload
#     time.sleep(0.3)
#     click(file_upload)

#     # click the file explorer address bar and enter path to media
#     time.sleep(1)
#     click(address_bar)
#     time.sleep(0.3)
#     keyboard.write(path)
#     time.sleep(0.3)
#     keyboard.press_and_release("enter")

#     # select all photos and press enter
#     time.sleep(0.3)
#     click(file_names_cords)
#     time.sleep(0.3)
#     keyboard.write(file_names)
#     time.sleep(0.3)
#     keyboard.press_and_release("enter")

#     # wait a second before repeating
#     time.sleep(1)

def uploader(caption, file_names, path, multiple_accounts, fb_name, location):
    # open new tab
    url = "https://business.facebook.com/creatorstudio?tab=instagram_content_posts&mode=instagram&collection_id=all_pages&content_table=INSTAGRAM_POSTS"
    os.startfile(url)
    
    # click Create Post
    time.sleep(4)
    click("imgs/create_post.png")

    # click Instagram Feed
    time.sleep(0.25)
    click("imgs/instagram_feed.png")

    time.sleep(1.5)
    if multiple_accounts:
        click("imgs/search_profile.png")

        time.sleep(0.6)
        keyboard.write(fb_name)

        # choses first profile
        time.sleep(0.75)
        keyboard.press_and_release("tab")
        time.sleep(0.2)
        keyboard.press_and_release("tab")
        time.sleep(0.2)
        keyboard.press_and_release("enter")

    # enter caption
    time.sleep(0.25)
    click("imgs/caption.png")
    time.sleep(0.3)
    subprocess.run(['clip.exe'], input=caption.encode('utf-16'), check=True) 
    keyboard.press_and_release('ctrl+v')

    time.sleep(0.3)
    click("imgs/location.png")
    time.sleep(0.2)
    keyboard.write(location)
    time.sleep(1.5)
    keyboard.press_and_release("enter")
    
    # click Add Content
    time.sleep(0.5)
    click("imgs/add_content.png")

    # click From File Upload
    time.sleep(0.3)
    click("imgs/file_upload.png")

    # click the file explorer address bar and enter path to media
    time.sleep(1)
    click("imgs/address_bar.png", grayscale=True)
    time.sleep(0.3)
    keyboard.write(path)
    time.sleep(0.3)
    keyboard.press_and_release("enter")

    # select all photos and press enter
    time.sleep(0.5)
    keyboard.press_and_release("tab")
    time.sleep(0.5)
    keyboard.press_and_release("tab")
    time.sleep(0.5)
    keyboard.press_and_release("tab")
    time.sleep(0.5)
    keyboard.press_and_release("tab")
    time.sleep(0.5)
    keyboard.press_and_release("tab")
    time.sleep(0.5)
    keyboard.write(file_names)
    time.sleep(0.5)
    keyboard.press_and_release("enter")

    # wait a second before repeating
    time.sleep(1)


# def scheduler(timestamp, bb_enabled, dt_format, format_24h):
#     # bb = bookmarks bar
#     if bb_enabled:
#         bb_difference = 0
#     else:
#         bb_difference = 35

#     schedule_caret = (1860, 990-bb_difference)
#     schedule_btn = (1591, 890-bb_difference)
#     date_cords = (1615, 858-bb_difference)

#     dt = datetime.fromtimestamp(timestamp)

#     formatted = dt.strftime(dt_format)

#     # Takes care of the hour
#     hour = dt.hour
#     # If not 24h format, get AM/PM
#     if format_24h == "False":
#         is_pm = False
#         if hour == 0:
#             hour = 12
#         elif hour == 12:
#             is_pm = True
#         elif hour > 12:
#             hour = hour % 12
#             is_pm = True
    
#     # Takes care of the mintues
#     minutes = str(dt.minute)
#     if len(minutes) == 1:
#         minutes = "0" + minutes

#     time.sleep(0.3)
#     click(schedule_caret)

#     time.sleep(0.3)
#     click(schedule_btn)

#     time.sleep(0.3)
#     click(date_cords)

#     time.sleep(0.3)
#     keyboard.write(formatted)
#     time.sleep(0.3)
#     keyboard.press_and_release("enter")
#     time.sleep(0.3)
#     keyboard.press_and_release("tab")

#     time.sleep(0.3)
#     str_hour = "00" + str(hour)
#     for c in str_hour:
#         keyboard.write(c)
#         time.sleep(0.2)
#     time.sleep(0.2)
#     keyboard.press_and_release("tab")

#     time.sleep(0.3)
#     for minute in minutes:
#         time.sleep(0.3)
#         keyboard.write(minute)
#     time.sleep(0.3)
#     keyboard.press_and_release("tab")

#     if format_24h == "False":
#         time.sleep(0.3)
#         if is_pm:
#             keyboard.write("p")
#         else:
#             keyboard.write("a")
#     time.sleep(0.3)

def scheduler(timestamp, dt_format, format_24h):
    dt = datetime.fromtimestamp(timestamp)

    formatted = dt.strftime(dt_format)

    # Takes care of the hour
    hour = dt.hour
    # If not 24h format, get AM/PM
    if format_24h == "False":
        is_pm = False
        if hour == 0:
            hour = 12
        elif hour == 12:
            is_pm = True
        elif hour > 12:
            hour = hour % 12
            is_pm = True
    
    # Takes care of the mintues
    minutes = str(dt.minute)
    if len(minutes) == 1:
        minutes = "0" + minutes

    time.sleep(0.3)
    click("imgs/schedule_caret.png")

    time.sleep(0.3)
    click("imgs/schedule_btn.png")

    time.sleep(0.3)
    click("imgs/date_cords.png")

    time.sleep(0.3)
    keyboard.write(formatted)
    time.sleep(0.3)
    keyboard.press_and_release("enter")
    time.sleep(0.3)
    keyboard.press_and_release("tab")

    time.sleep(0.3)
    str_hour = "00" + str(hour)
    for c in str_hour:
        keyboard.write(c)
        time.sleep(0.2)
    time.sleep(0.2)
    keyboard.press_and_release("tab")

    time.sleep(0.3)
    for minute in minutes:
        time.sleep(0.3)
        keyboard.write(minute)
    time.sleep(0.3)
    keyboard.press_and_release("tab")

    if format_24h == "False":
        time.sleep(0.3)
        if is_pm:
            keyboard.write("p")
        else:
            keyboard.write("a")
    time.sleep(0.3)
