import PySimpleGUI as sg
import threading
import os
import re

from start import start
from setup import setup
from caption import caption_setup
from main import main
import utils, overnight
from unfollower import unfollow

WINDOW_TITLE = 'IG Upload Helper'
x = 650
y = 750

sg.theme('Dark')   # Add a touch of color
# All the stuff inside your window.

base_path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]


# creates accounts.txt if it doesn't exist
accounts_path = os.path.join(base_path, "accounts.txt")
utils.create_file(accounts_path, "")
accounts = [account for account in open("accounts.txt", "r").read().split("\n") if account]  # gets all accounts

accounts_visible = False
if len(accounts) > 1:
    accounts_visible = True

barrier = sg.Text("|", font=("Ariel 15"))
barrier_visible = sg.Text("|", font=("Ariel 15"), visible=accounts_visible)

if len(accounts) > 1:
    default_account = accounts[0]
else:
    default_account = "No Accounts Found"
layout = [ 
            [sg.Text("IG Upload Helper", font=("Ariel 16 bold"), justification='center', size=(x,1))],
            [sg.Text("")],
            [sg.Text("First Time (for each account)", font=("Ariel 14 bold"))],
            [sg.Button("Setup", size=(8,2)), ],
            [sg.Text("Select account:", visible=accounts_visible), sg.DropDown(accounts, key='-SELECT_ACCOUNT-', default_value=default_account, visible=accounts_visible), barrier_visible, sg.Text("Setup files:"), sg.Button("Descriptions"), sg.Button("Hashtags"), sg.Button("Caption")],
            [sg.Text("")],
            [sg.Text("Run Bot", font=("Ariel 14 bold"))],
            [sg.Text("Scrape and upload", font="Ariel 11 bold")],
            [sg.Text('Enter the username of the account you want to scrape:'), sg.InputText(key='-SCRAPE_USERNAME-', size=(41,0))],
            [sg.Text("Enter the timestamp of your last post (if nothing is entered, it will be taken from the 'last_timestamp.txt' file):")],
            [sg.InputText(key = '-TIMESTAMP-', size=(11,0)), sg.Button('epochconverter.com')],
            [sg.Text("Enter how many posts you want to posts from the user:"), sg.InputText(key='-NUM_POSTS-', default_text='25', size=(6,0))],
            [sg.Text("Select your account:"), sg.DropDown(accounts, key='-ACCOUNT-', default_value=default_account), sg.Button('Start')],
            [sg.Text("-------------------------------------------------------------------------------------------------------------------------------------------------------")],
            [sg.Text("Scrape without uploading", font="Ariel 11 bold")],
            [sg.Text("Scrape multiple accounts to use for later:")],
            [sg.Text("Enter the accounts separated by a comma (e.g., 'instagram,cristiano,jlo')")],
            [sg.InputText(key='-ACCOUNTS-', size=(25,0))],
            [sg.Text("Select your account:"), sg.DropDown(accounts, key='-OVERNIGHT_ACCOUNT-', default_value=default_account, visible=accounts_visible), sg.Button('Scrape')],
            [sg.Text("-------------------------------------------------------------------------------------------------------------------------------------------------------")],
            [sg.Button("Unfollow", size=(8,2))],
            [sg.Text("")],
            [sg.Button('Cancel', size=(8,2))]
            ]

# Create the Window
window = sg.Window(WINDOW_TITLE, layout, size=(x, y))

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # "Start" portion of Run
    if event == 'epochconverter.com':
            os.startfile('https://www.epochconverter.com/')

    if event == 'Start':
        account = values['-ACCOUNT-']
        
        scrape_username = values["-SCRAPE_USERNAME-"]
        while not scrape_username:
            if scrape_username is None:
                quit()
            scrape_username = sg.popup_get_text("Username cannot be blank.")

        # checks
        with open(os.path.join(account, "scraped_accounts.txt"), "a+") as f:
            f.seek(0)
            scraped_accounts = f.read().split("\n")

            if scrape_username in scraped_accounts:
                is_continue = sg.popup_yes_no("Warning", "You have already scraped posts from that user. Are you sure you want to scrape them again?")
                while not is_continue:
                    if is_continue is None:
                        quit()
                    is_continue = sg.popup_yes_no("Warning", "You have already scraped posts from that user. Are you sure you want to scrape them again?")
        scrape_username = scrape_username.strip()

        input_timestamp = values["-TIMESTAMP-"]
        
        num_posts = values["-NUM_POSTS-"]
        regex = r"\b([1-9]|[1-8][0-9]|9[0-9]|100)\b"
        while not re.search(regex, num_posts):
            if num_posts is None:
                quit()
            num_posts = sg.popup_get_text("Input must be a number between 1-100.")
        num_posts = int(num_posts)

        main(scrape_username, input_timestamp, num_posts, account)
    
    if event == "Setup":
        username = setup()
    
    if event == "Descriptions":
        accounts = [account for account in open("accounts.txt", "r").read().split("\n") if account]
        if len(accounts) < 1:
            sg.Popup("No accounts added")
            break
        if len(accounts) == 1:
            username = accounts[0]
        else:
            username = values["-SELECT_ACCOUNT-"]
            
        description_path = os.path.join(base_path, f"{username}/descriptions.txt")
        os.startfile(description_path)
    
    if event == "Hashtags":
        accounts = [account for account in open("accounts.txt", "r").read().split("\n") if account]
        if len(accounts) < 1:
            sg.Popup("No accounts added")
            break
        if len(accounts) == 1:
            username = accounts[0]
        else:
            username = values["-SELECT_ACCOUNT-"]
        
        hashtags_path = os.path.join(base_path, f"{username}/hashtags.json")
        utils.setup_hashtags(hashtags_path)
    
    if event == "Caption":
        accounts = [account for account in open("accounts.txt", "r").read().split("\n") if account]
        if len(accounts) < 1:
            sg.Popup("No accounts added")
            break
        if len(accounts) == 1:
            username = accounts[0]
        else:
            username = values["-SELECT_ACCOUNT-"]

        caption_setup(username)
    
    if event == "Scrape":
        utils.overnight_scrape(values["-ACCOUNTS-"], values["-OVERNIGHT_ACCOUNT-"])

    if event == "Unfollow":
        unfollow()

    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break

window.close()
