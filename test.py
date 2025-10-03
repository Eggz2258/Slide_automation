from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import requests
from os import path
from PyPDF2 import PdfWriter



#msedge --remote-debugging-port=9222 --user-data-dir="C:/Users/jishn/EdgeProfile"

options = Options()
options.debugger_address = "127.0.0.1:9222"
dPath = path.abspath(r"./Outputs/notes")
prefs = {
    "download.default_directory": dPath,   # your folder
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True       # don't open in browser, download instead
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Edge(options=options)
actions = ActionChains(driver)
wait = WebDriverWait(driver, 10)


driver.get("https://www.pesuacademy.com/Academy/s/studentProfilePESU")
print(driver.title)

Flag = 0

ask =  input("Slides or Note: ")

if "slides" in ask:
    Flag = 0
elif "note" in ask:
    Flag = 1


def click2(by, ele,parent = None):
    if parent:
        ele = wait.until(lambda d: EC.element_to_be_clickable(parent.find_element(by, ele))(d))
    else:
        ele = wait.until(EC.element_to_be_clickable((by, ele)))

    print("Clicking",ele.text+"...")
    clic(ele)

def clic(ele):
    time.sleep(0.5)
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", ele)
    time.sleep(1)
    ele.click()

def wait_find(by, ele):
    
    Table =wait.until(EC.element_to_be_clickable((by, ele))) 
    return Table


def noterec(i):
    try:
        click2(By.ID, 'contentType_3')
    except Exception as e:
        print("trying again")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", driver.find_element(By.ID, 'contentType_2'))
        noterec(i)

def rec(i):
    try:
        click2(By.ID, 'contentType_2')
    except Exception as e:
        print("trying again")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", driver.find_element(By.ID, 'contentType_2'))
        rec(i)

def click_tr(i):
    global Flag
    global chapter_name
    a = wait_find(By.XPATH, '//*[@id="CourseContentId"]/div/div[1]/table')
    b = a.find_element(By.TAG_NAME,"tbody") #full chapter table
    e = b.find_elements(By.TAG_NAME,'tr') #list of chapters
    name_raw = e[i].text
    name = ""
    for ws in name_raw:
            name += ws
    name = name.split()
    name = name[0]
    
    chapter_name.append(name)
    time.sleep(0.5)
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", e[i])
    time.sleep(1)
    e[i].click()

    #slides_btn
    if(Flag):
        noterec(i)
    else:
        rec(i)

def pdf_down(btn):
    global j
    print("in")
    
    # btn = btn.find_element(By.TAG_NAME,"a")
    click2(By.TAG_NAME,"a", parent=btn)
    time.sleep(1)
    link = driver.find_element(By.TAG_NAME,"iframe").get_attribute("src")
    # driver.get(link)
    # driver.print_page()
    cookies = {c['name']: c['value'] for c in driver.get_cookies()}
    resp = requests.get(link, cookies=cookies)

    with open(f"./Outputs/notes/output{j}.pdf", "wb") as f:
        f.write(resp.content)

    time.sleep(1)
    print("File saved in Outputs")
    j+=1

def course_selector(name):
    for course in (driver.find_elements(By.TAG_NAME,"tr")):
        print(course.text.lower())
        if(name.lower() in course.text.lower()):
            click2(By.ID, course.get_dom_attribute("id"))


def unit_selector(unit_no):
        Unit = wait_find(By.ID, "courselistunit").find_elements(By.TAG_NAME,"li")
        Unit[unit_no - 1].click()
time.sleep(2)

#course.click

click2(By.XPATH, '//*[@id="menuTab_653"]/a/span[2]')


#course selecotr
name = input("Enter name: ").lower()
course_selector(name)

unit_no = int(input("Enter Unit: "))
unit_selector(unit_no)

time.sleep(0.5)
Table = wait_find(By.XPATH, '//*[@id="CourseContentId"]/div/div[1]/table')


nums = Table.find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,'tr')

j =0
chapter_name = []
for i in range(len(nums)):
    try:
        time.sleep(1)
        click_tr(i)     #click the section
        print(chapter_name)
        time.sleep(1)
        btns = driver.find_elements(By.CLASS_NAME,"link-preview")

        for btn in btns:  #inside the section
            print(len(btn.find_elements(By.TAG_NAME,"iframe")))
            if len(btn.find_elements(By.TAG_NAME,"iframe")) >0:
                pdf_down(btn)
                
            else:
                clic(btn)

        time.sleep(1)
    
        click2(By.PARTIAL_LINK_TEXT,"UE24") #go back to main units
        time.sleep(2)

        unit_selector(unit_no)#sleect unit
        time.sleep(1)
    except Exception as e:
        print(f"could not do {i} ;{e}")
        click2(By.PARTIAL_LINK_TEXT,"UE24")

        unit_selector(unit_no)
        pass



input()
driver.quit()
