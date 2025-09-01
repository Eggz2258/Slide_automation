from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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
afll = driver.find_element(By.XPATH, '//*[@id="rowWiseCourseContent_20965"]/td[2]').click()
time.sleep(3)

Table = driver.find_element(By.XPATH, '//*[@id="CourseContentId"]/div/div[1]/table')
time.sleep(1)
nums = Table.find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,'tr')


j =0
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

    time.sleep(1)
    btns = driver.find_elements(By.CLASS_NAME,"link-preview")

    for btn in btns:
        print(len(btn.find_elements(By.TAG_NAME,"iframe")))
        if len(btn.find_elements(By.TAG_NAME,"iframe")) >0:
            print("in")
            time.sleep(1)
            btn = btn.find_element(By.TAG_NAME,"a")
            clic(btn)
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
        else:
                clic(btn)

    time.sleep(1)
# driver.find_element(By.CLASS_NAME,"pull-left").click()
    
    main =  driver.find_element(By.PARTIAL_LINK_TEXT,"UE24")
    clic(main)
    #actions.scroll_to_element(main)
    time.sleep(2)

input()
driver.quit()
