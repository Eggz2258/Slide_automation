from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


options = Options()
# Try normal first, then headless if it still crashes
#options.add_argument("--headless=new")
options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Edge(options=options)
driver.get("https://www.pesuacademy.com/Academy/s/studentProfilePESU")
#handles = driver.window_handles
#driver.switch_to.window(handles[-1])  



# login_name = driver.find_element(By.XPATH,'//*[@id="j_scriptusername"]')
# login_name.send_keys()
print(driver.title)

actions = ActionChains(driver)

def clic(ele):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ele)
    time.sleep(1)
    ele.click()
#actions.scroll_to_element(el)
input()
time.sleep(2)
course = driver.find_element(By.XPATH,'//*[@id="menuTab_653"]/a/span[2]').click()
time.sleep(3)
afll = driver.find_element(By.XPATH, '//*[@id="rowWiseCourseContent_20968"]/td[2]').click()
time.sleep(3)

Table = driver.find_element(By.XPATH, '//*[@id="CourseContentId"]/div/div[1]/table')
time.sleep(1)
nums = Table.find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,'tr')



for i in range(len(nums)):
    time.sleep(2)
    e = driver.find_element(By.XPATH, '//*[@id="CourseContentId"]/div/div[1]/table').find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,'tr')
#    print(e[i])
    time.sleep(1)
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", e[i])
    time.sleep(1)
    e[i].click()
    time.sleep(2)    
    slides_btn =driver.find_element(By.ID, "contentType_2")
    clic(slides_btn)
    try:
        time.sleep(1)
        btn = driver.find_element(By.CLASS_NAME,"link-preview")
        clic(btn)
    except:
        pass
    time.sleep(1)
# driver.find_element(By.CLASS_NAME,"pull-left").click()
    
    main =  driver.find_element(By.PARTIAL_LINK_TEXT,"UE24")
    clic(main)
    #actions.scroll_to_element(main)
    time.sleep(2)

input()
driver.quit()
