

from pyvirtualdisplay import Display

import time
import json 
from fastapi.responses import JSONResponse
import os
from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from typing import List
import uvicorn
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi import FastAPI, File, UploadFile
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import shutil
import pandas as pd
import subprocess
from fastapi.logger import logger as fastapi_logger
import psutil
# display = Display(visible=0, size=(800, 600))
# display.start()
def get_driver(profile):
    
    try:
        shutil.rmtree(profile)
        # os.makedirs(profile)
        # os.rmdir(profile)
    except OSError:
        pass
    #    print ("Already  created the directory %s" % profile)
    # else:
    #     print ("Successfully created the directory %s" % profile)
        
    destination = shutil.copytree(os.path.join(os.getcwd(), 'data/orgin'), profile, copy_function = shutil.copy)

    try:
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == "chrome" or proc.name() == "chromedriver":
                proc.kill()    
    except:
        print('::::::::::::::::::::::::::::::::')

    option = webdriver.ChromeOptions()
    option.add_argument("--user-data-dir={}".format(profile))
    if os.name=='nt' :   
        driver = webdriver.Chrome('chromedriver.exe',options=option) 
    else:
        driver = webdriver.Chrome('./chromedriver',options=option) 
    driver.maximize_window()

    driver.get("https://razerid.razer.com/")
    

    return driver


def login(email,password,driver):
    try:
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//input[@name="email"]'))).clear()
        driver.find_element_by_xpath('//input[@name="password"]').clear()
        driver.find_element_by_xpath('//input[@name="email"]').send_keys(email)
        driver.find_element_by_xpath('//input[@name="password"]').send_keys(password)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '#btn-log-in')))

        # driver.find_element_by_id("btn-log-in").click()
        print('Successful login')
    except Exception as e:
        print(e)        
    return driver

def get_session(email,password,profile) :   
    print("create session for user:%s" % email)
    
    try:
    
        driver=get_driver(profile)
    except Exception as e:
        print(e)
    
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@href="/account/photo/edit"]')))
        print ("Already  login  .....")

    except:
        print('login in the RAZER....')

        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login"]/div[2]/button'))).click()
        except:
            pass    
    
    driver=login(email,password,driver)
    
    

    return driver

def select_product_topup(email,password,catalog_url,User_ID,amount,driver):
    status='Error'         

    driver.get(catalog_url)
    driver.execute_script("window.scrollTo(0, 300)")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-labelledby="{}"]'.format(amount)))).click()  
 
    try:
        driver.find_element_by_css_selector('a.text--black.rzr-icon-cross.standalone-icon-24.cta--no-underline').click()  

    except:
        pass


    
    driver.find_element_by_xpath('//div[@aria-labelledby="{}"]'.format(amount)).click() 
    driver.execute_script("window.scrollTo(0, 300)")
    time.sleep(1)
    
    
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.selection-tile__img'))).click()  

    
    
    element=driver.find_element_by_xpath('//input[@name="PlayerId"]')    
    driver.execute_script("arguments[0].value = '';", element)     
    element.send_keys(User_ID)    


    driver.find_element_by_css_selector('button.btn-loader.btn-block-mobile.btn.btn-primary').click()  

    return driver
  
def RELOAD_account(email,password,pincode):

    driver.get('https://gold.razer.com/gold/reload')
    driver.find_element_by_css_selector('div.selection-tile__img').click()  
    driver.find_element_by_css_selector('a.btn.btn-primary.btn-sm.btn-block-mobile.btn-width--fixed.btn-grp__btn.order-sm-last').click()
    return driver




    
 
    
def TOPUP_product(email,password,catalog_url,User_ID,amount):
    try:
            if os.name!='nt' : 
                display = Display(visible=0, size=(800, 600))
                display.start()
                
            profile=os.path.join(os.getcwd(), "data", email) 
            start_time = time.time()
            driver=get_session(email,password,profile) 
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@href="/account/photo/edit"]')))
            
            driver=select_product_topup(email,password,catalog_url,User_ID,amount,driver)  
            driver.execute_script("window.scrollTo(0, 300)")
            
            element=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btnConfirm')))   
            driver.execute_script("arguments[0].click();", element)
            try:
                element=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.status-success")))          
            except:
                
                try:
                    iframe = driver.find_element_by_xpath('//iframe[contains(@id, "razerOTP")]')
                    driver.switch_to_frame(iframe)
                    print('enter OTP Message')
                    k=0
                    while True:
                        time.sleep(1)
                        k=k+1
                        if k >40:
                            break
                        data_file = pd.read_csv("data.csv") 
                        data_cc=data_file[data_file["email"]== email].iloc[-1, :]
                        if int(time.time())-int(data_cc["time"])<60:
                            print(data_cc["OTP"])
                            driver.find_element_by_xpath('//input[contains(@type, "number")]').send_keys(OTP)
                            driver.switch_to.default_content()
        
                            
                            
                except:
                        try:
                            element=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.status-success")))          
                        except:
                            print('Error Message')
        
                            pass
            driver.switch_to.default_content()
                        
            try:
                element=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.status-success"))) 
                status='Successful'         
            except:
                status='Error'         
        
                print('Error Message')
             
                
                
            print("--- %s seconds ---" % (time.time() - start_time))
    except Exception as e:
        status=e
    try:
        driver.quit()
    except:
        pass
    # if os.name!='nt' :                           
    #     display.stop()
    return status
    
app = FastAPI(title='RAZER API')

origins = [
'*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
   


email='bennaoui.ameur@gmail.com'
password='Mohamed@2020'
catalog_url='https://gold.razer.com/gold/catalog/freefire-direct-top-up'
User_ID='2039664991'
amount='100 + 10 Diamonds - USD 1.00'

@app.post("/TOPUP_product/",tags=["TOPUP product"])
async def TOPUP_product_EP(email:str,password:str,catalog_url: str ,User_ID:str,amount: str):
    try:
    
        status=TOPUP_product(email,password,catalog_url,User_ID,amount)  
        print('======================================================')
        
        print(status)
    except Exception as e:
        status=e
    return JSONResponse(content={"status":status })

@app.post("/RELOAD_account/",tags=["RELOAD account"])
async def RELOAD_account_EP(email:str,password:str,pincode: str):
    status=RELOAD_account(email,password,pincode)
    
    return JSONResponse(content={"status":status }) 
  
@app.post("/OTPMessage/",tags=["OTP Message"])
async def OTPMessage_EP(email:str,OTP:str):
    data={
    "time":int(time.time()),
    "email": email,
    "OTP": OTP}
    df = pd.DataFrame()

    df = df.append(data,ignore_index=True)
    df.to_csv('data.csv', mode='a', header=False)

    status='Successful'

    return JSONResponse(content={"status":status }) 

# if __name__ == '__main__':
#     uvicorn.run("main:app", port=8080, host='0.0.0.0', reload=True)

status=TOPUP_product(email,password,catalog_url,User_ID,amount)  
