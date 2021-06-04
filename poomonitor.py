# Generate EXE with pyinstaller --onefile webscraper.py --hidden-import jinja2 --add-data C:\Users\RemCa\AppData\Local\Programs\Python\Python38-32\Lib\site-packages\pandas\io\formats\templates\html.tpl;pandas\io\formats\templates
import json
import os
import time
import smtplib
import ssl
import threading
import pygetwindow
import keyboard
from os import system
from decimal import *
from datetime import datetime
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

try:
    # Setting up window and colors
    system("title "+ "Poomonitor")
    color = "\033[1;31;40m"

    # Getting data from options file
    current_dir = os.path.dirname(os.path.realpath(__file__))
    with open(current_dir + "\options.json") as file:
        data = json.load(file)
    refresh_delay = data['refresh_delay']
    if data['autoload'] != "none":
        autoload_item = input("Select (0) for no autoload or (1-5) to select a preset from options.txt file: ")
        print("Selected option " + autoload_item + ": " +  data['saved'][int(autoload_item)-1]['name'])

    # Getting input from user
    if data['autoload'] != "none" and data['saved'][int(autoload_item)-1]['static_link'] == "none":
        poo_coin_link = input("Enter a poocoin link to monitor: ")
    else:
        poo_coin_link = data['saved'][int(autoload_item)-1]['static_link']
        print("(AUTO) Enter a poocoin link to monitor: " + data['saved'][int(autoload_item)-1]['static_link'])

    if data['autoload'] != "none" and data['saved'][int(autoload_item)-1]['static_direction'] == "none":
        above_or_below = input("Enter either 'above' or 'below': ")
    else:
        above_or_below = data['saved'][int(autoload_item)-1]['static_direction']
        print("(AUTO) Enter either 'above' or 'below': " + data['saved'][int(autoload_item)-1]['static_direction'])

    if data['autoload'] != "none" and data['saved'][int(autoload_item)-1]['static_price'] == "none":
        desired_price = input("Enter price notification value (EX: $0.023): ")
    else:
        desired_price = data['saved'][int(autoload_item)-1]['static_price']
        print("(AUTO) Enter price notification value (EX: $0.023): " + data['saved'][int(autoload_item)-1]['static_price'])

    # Loading the chrome driver
    print("Loading chrome driver...")
    coptions = Options()
    coptions.add_argument('--headless')
    coptions.add_argument('--disable-gpu')  # Last I checked this was necessary.
    coptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(current_dir + "/chromedriver.exe", options=coptions)

    # Loading the webpage itself
    print("Loading webpage...")
    while True:
        try:
            driver.get(poo_coin_link)
            myElem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='mb-1 d-flex flex-column lh-1']")))
            break
        except TimeoutException:
            print("Page didn't load after 30 seconds, trying again!")
            continue
    print("Done, starting the monitor...")
    time.sleep(3.0)

    # Resize the window
    win = pygetwindow.getWindowsWithTitle('Poomonitor')[0]
    win.size = (800, 155)
    cls = lambda: system('cls')
    cls()
    if data['autoload'] != "none":
        system("title "+ "Poomonitor: (AUTO) " + data['saved'][int(autoload_item)-1]['name'])
    
    # Initialize email stuff
    dont_be_scummy = """nicetry"""
    sender_email = "pythonautosend@gmail.com"
    receiver_email = data['saved'][int(autoload_item)-1]['emails']
    context = ssl.create_default_context()
    pass_threshhold = False
    pass_threshhold_prev = False
    send_email = False
    message = ""

    # Main loop to scrape from webpage
    counter = 0
    fails = 0
    
    while True:
        # Waiting for data to be scraped
        if keyboard.is_pressed('x') and keyboard.is_pressed('z'):
            break

        time.sleep(float(refresh_delay))
        
        try:
            # Preparing data for printing
            now = datetime.now()
            scraped_time = now.strftime("%H:%M:%S")
            tempData = driver.find_element_by_xpath("//div[@class='mb-1 d-flex flex-column lh-1']").text.splitlines()
            name = tempData[0]
            price = tempData[1]
            counter += 1

            # Doing calculations if goal was met 
            if above_or_below == "above" and float(desired_price[1:]) <= float(price[1:]):
                color = "\033[1;32;40m"
                wav_file = current_dir + "/above.wav"
                threading.Thread(target=playsound, args=(wav_file,), daemon=True).start()

                # Prepare an email, notifying that the coin should now be sold
                if receiver_email != "none" and pass_threshhold == False:
                    pass_threshhold = True
                    send_email = True
                    message = "Subject: SELL - " + name + "\n\n(ABOVE) Coin: " + name + " has risen above\n" + desired_price + "\nand is currently at\n" + price + "\nat time: " + scraped_time + "\ncontract: " + poo_coin_link.rsplit('/', 1)[-1]
            elif above_or_below == "below" and float(desired_price[1:]) >= float(price[1:]):
                color = "\033[1;32;40m"
                wav_file = current_dir + "/below.wav"
                threading.Thread(target=playsound, args=(wav_file,), daemon=True).start()

                # Prepare an email, notifying that the coin should now be bought
                if receiver_email != "none" and pass_threshhold == False:
                    pass_threshhold = True
                    send_email = True
                    message = "Subject: BUY - " + name + "\n\n(BELOW) Coin: " + name + " has dipped below\n" + desired_price + "\nand is currently at\n" + price + "\nat time: " + scraped_time + "\ncontract: " + poo_coin_link.rsplit('/', 1)[-1]
            else:
                color = "\033[1;31;40m"
                pass_threshhold = False
            
            # Printing data
            print(color + "\n\nContract: " + poo_coin_link.rsplit('/', 1)[-1] + "\nAt " + scraped_time + ", checked " +  above_or_below + " " + desired_price + " " + str(counter-fails) + " times (" + str(fails) + " errors)\n" + name + "\n" + price)

            # Prepare an email, notifying that the coin has no longer satisfied the condition
            if receiver_email != "none" and pass_threshhold == False and pass_threshhold_prev == True:
                send_email = True
                message = "Subject: IGNORE - " + name + "\n\n(IGNORE) Coin: " + name + " no longer fits criteria\n" + desired_price + "\nand is currently at\n" + price + "\nat time: " + scraped_time + "\ncontract: " + poo_coin_link.rsplit('/', 1)[-1]

            # Send email notifying to buy or sell, if the user chooses
            if send_email == True:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, dont_be_scummy)
                    server.sendmail(sender_email, receiver_email, message)
            pass_threshhold_prev = pass_threshhold
            send_email = False
        except Exception as e2:
            fails += 1
            send_email = False
            print("Unknown Exception'", e2, "'caught, trying again!\n")
            continue
    driver.quit()

except Exception as e:
    print("Unknown Exception", e, "caught, library error is likely")
    os.system('pause')
