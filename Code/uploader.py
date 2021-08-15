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


def tab(x):
    time.sleep(0.5)
    for i in range(x):
        keyboard.press_and_release("tab")
        time.sleep(0.2)
    time.sleep(0.3)


def shift_tab(x):
    time.sleep(0.5)
    for i in range(x):
        keyboard.press_and_release("shift+tab")
        time.sleep(0.2)
    time.sleep(0.3)


def uploader(caption, file_names, path, multiple_accounts, fb_name, location):
    # open new tab
    url = "https://business.facebook.com/creatorstudio?tab=instagram_content_posts&mode=instagram&collection_id=all_pages&content_table=INSTAGRAM_POSTS"
    os.startfile(url)
    
    # click Create Post
    time.sleep(4)
    try:
        click("imgs/create_post_new.png", grayscale=True)
    except:
        tab(7)
        keyboard.press_and_release("enter")

    # click Instagram Feed
    time.sleep(0.25)
    click("imgs/instagram_feed.png")

    time.sleep(1.5)
    if multiple_accounts:
        click("imgs/search_profile.png")

        time.sleep(0.6)
        keyboard.write(fb_name)

        # choses first profile
        tab(2)
        keyboard.press_and_release("enter")

    # enter caption
    
    # time.sleep(0.25)
    # click("imgs/caption.png")
    tab(2)
    subprocess.run(['clip.exe'], input=caption.encode('utf-16'), check=True) 
    keyboard.press_and_release('ctrl+v')

    # time.sleep(0.3)
    # click("imgs/location.png")
    # time.sleep(0.2)
    tab(2)
    keyboard.write(location)
    time.sleep(1.5)
    keyboard.press_and_release("enter")
    
    # click Add Content
    # time.sleep(0.5)
    # click("imgs/add_content.png")
    tab(1)
    keyboard.press_and_release("enter")

    # click From File Upload
    # time.sleep(0.3)
    # click("imgs/file_upload.png")
    shift_tab(2)
    keyboard.press_and_release("enter")

    time.sleep(1)
    keyboard.write(f"{path}\\{file_names}")
    time.sleep(0.5)
    keyboard.press_and_release("enter")

    # wait a second before repeating
    time.sleep(1)


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
