# Kane isntall thn python kai vale to pip san PATH variable, tha sto proteinei sthn egkatastasi prepei na pathseis to koumpi
# anoixe cmd kai pata pip install selenium gia na egkatastisei to eslenium
# alaxe ot einai, vale cmd pata python BotToB.py kai an trexei ola uperoxa

from selenium import webdriver
import time
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Dose ena timer pou prepei na perimenei, exartatai apo to poso grigora/arga kanei laod to page
#vale username kai password anamesa apo ta autakia " "
timer = 5
username =""
password =""

driver = webdriver.Firefox() # Gia Chrome allaxe thn grammh se: driver = webdriver.Chrome() | den xero an tha doylepsei
driver.get("https://www.instagram.com/")
time.sleep(timer) # Sleep, waits for page to load try a lower timer if loads quickly
#Finds all buttons and forms that needs to be pressed
try:
    driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/button[1]").click() #Cookies, if raises exception, comment this line
driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input').send_keys(username) 
driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input').send_keys(password)
driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button').click()
#Login should have finished by here
url = "https://www.instagram.com/p/CH-MgQOn-7E/" # Chagent this with any other competition " "
#We go to the url
time.sleep(timer)
driver.get(url) 
time.sleep(timer)
#Technical things
counter = 0
friendList = ['@','@','@'] # Vale ta onomata ton filon sou opos vlepeis edo me komma endiamesa '@','@','@', ..


while(True):
    try:
        # Create the comment
        send = friendList[random.randint(0,len(friendList)-1)] + " " + friendList[random.randint(0,len(friendList)-1)] + " " + friendList[random.randint(0,len(friendList)-1)]
        # lETS TRY
        comment_box = ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.Ypffh")))
        comment_box.send_keys(send)
        comment_box.send_keys(Keys.ENTER)
        time.sleep(timer)
        driver.refresh() # Doesnt sleep so this is an alternative

        #Counter increase and wait 5 seconds
        counter+=1
        if(counter>=100): # If more than 20 comments, sleep
            time.sleep(60*20)
    except Exception as e:
        #If exception continue
        print(e)
        continue
    
    
