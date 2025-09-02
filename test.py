from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import requests


options = Options()
# Try normal first, then headless if it still crashes
#options.add_argument("--headless=new")
options.debugger_address = "127.0.0.1:9222"

prefs = {
    "download.default_directory": r"C:\Downloads",   # your folder
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True       # don't open in browser, download instead
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Edge(options=options)
wait = WebDriverWait(driver, 10)
driver.get("https://www.pesuacademy.com/Academy/s/studentProfilePESU")
#handles = driver.window_handles
#driver.switch_to.window(handles[-1])  



# login_name = driver.find_element(By.XPATH,'//*[@id="j_scriptusername"]')
# login_name.send_keys()
print(driver.title)

actions = ActionChains(driver)


def click2(by, ele,parent = None):
    if parent:
        ele = wait.until(lambda d: EC.element_to_be_clickable(parent.find_element(by, ele))(d))
    else:
        ele = wait.until(EC.element_to_be_clickable((by, ele)))
    clic(ele)

def clic(ele):
    time.sleep(0.5)
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", ele)
    time.sleep(1)
    ele.click()

def wait_find(by, ele):
    
    Table =wait.until(EC.element_to_be_clickable((by, ele))) 
    return Table
def rec(i):
    try:
        click2(By.ID, 'contentType_2')
    except Exception as e:
        print("trying again")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", driver.find_element(By.ID, 'contentType_2'))
        rec(i)
def click_tr(i):
    a = wait_find(By.XPATH, '//*[@id="CourseContentId"]/div/div[1]/table')
    b = a.find_element(By.TAG_NAME,"tbody")
    e = b.find_elements(By.TAG_NAME,'tr')
    #e = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="CourseContentId"]/div/div[1]/table')))   .(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,'tr')
    print(i)
    #print(e[i])
    time.sleep(1)
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", e[i])
    time.sleep(1)
    e[i].click()

    #slides_btn =driver.find_element(By.ID, "contentType_2")
    # element = wait.until(EC.element_to_be_clickable((By.ID, 'contentType_2')))
    # clic(element)
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

    with open(f"./Outputs/output{j}.pdf", "wb") as f:
        f.write(resp.content)

    time.sleep(1)
    print("File saved as output.pdf")
    j+=1



#actions.scroll_to_element(el)

time.sleep(2)

# course = driver.find_element(By.XPATH,'//*[@id="menuTab_653"]/a/span[2]').click()
# element = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTab_653"]/a/span[2]'))).click()


click2(By.XPATH, '//*[@id="menuTab_653"]/a/span[2]')

#afll = driver.find_element(By.XPATH, '//*[@id="rowWiseCourseContent_20965"]/td[2]').click()

click2(By.XPATH, '//*[@id="rowWiseCourseContent_20965"]/td[2]')


Table = wait_find(By.XPATH, '//*[@id="CourseContentId"]/div/div[1]/table')
#click2(By.XPATH, '//*[@id="CourseContentId"]/div/div[1]/table')

nums = Table.find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,'tr')



j =0
for i in range(10,len(nums)):
    try:
        print("first")
        click_tr(i)
        time.sleep(1)
        btns = driver.find_elements(By.CLASS_NAME,"link-preview")

        for btn in btns:

            print(len(btn.find_elements(By.TAG_NAME,"iframe")))

            if len(btn.find_elements(By.TAG_NAME,"iframe")) >0:
                pdf_down(btn)
                
            else:
                clic(btn)

        time.sleep(1)
    # driver.find_element(By.CLASS_NAME,"pull-left").click()
        
        # main =  driver.find_element(By.PARTIAL_LINK_TEXT,"UE24")
        # clic(main)
        click2(By.PARTIAL_LINK_TEXT,"UE24")
        #actions.scroll_to_element(main)
        time.sleep(2)

    except Exception as e:
        print(f"could not do {i} ;{e}")
        click2(By.PARTIAL_LINK_TEXT,"UE24")
        pass

input()
driver.quit()
