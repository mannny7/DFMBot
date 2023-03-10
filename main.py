import re, os, json, time

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from colorama import just_fix_windows_console
from termcolor import colored

# Fix the terminal colour for windows
just_fix_windows_console()

fileLocation = os.path.dirname(os.path.realpath(__file__))


def log(text, text_color="green"):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(f'{colored(current_time, text_color)} {colored(">>>", text_color)} {colored(text, text_color)}')


def click_element(element_id, logging=False):
    # Will keep trying to click an element by its XPATH
    # If logging is True it will print any thrown exceptions
    while True:
        try:
            driver.find_element(By.XPATH, element_id).click()
            break
        except Exception as e:
            if logging:
                log(e)
            pass


def send_text(element_id, text, logging=False):
    # Send specified text to an element by XPATH
    # if Logging is True it will print any thrown exceptions
    while True:
        try:
            element = driver.find_element(By.XPATH, element_id)
            element.send_keys(text)
            break
        except Exception as e:
            if logging:
                log(e)
            pass


with open(fileLocation + "\\dfm.txt", "r") as file:
    data = json.load(file)
    username = data["username"]
    password = data["password"]

if not(username and password):
    log("Please enter your username and password for DFM in the dfm.txt! It is in the same folder as the Python script", text_color="red")
    exit(code=0)



# Epic ascii art
log("""
$$$$$$$\  $$$$$$$$\ $$\      $$\       $$\   $$\ $$\   $$\ $$\   $$\ $$$$$$$$\ $$$$$$$\  
$$  __$$\ $$  _____|$$$\    $$$ |      $$$\  $$ |$$ |  $$ |$$ | $$  |$$  _____|$$  __$$\ 
$$ |  $$ |$$ |      $$$$\  $$$$ |      $$$$\ $$ |$$ |  $$ |$$ |$$  / $$ |      $$ |  $$ |
$$ |  $$ |$$$$$\    $$\$$\$$ $$ |      $$ $$\$$ |$$ |  $$ |$$$$$  /  $$$$$\    $$$$$$$  |
$$ |  $$ |$$  __|   $$ \$$$  $$ |      $$ \$$$$ |$$ |  $$ |$$  $$<   $$  __|   $$  __$$< 
$$ |  $$ |$$ |      $$ |\$  /$$ |      $$ |\$$$ |$$ |  $$ |$$ |\$$\  $$ |      $$ |  $$ |
$$$$$$$  |$$ |      $$ | \_/ $$ |      $$ | \$$ |\$$$$$$  |$$ | \$$\ $$$$$$$$\ $$ |  $$ |
\_______/ \__|      \__|     \__|      \__|  \__| \______/ \__|  \__|\________|\__|  \__|
""", text_color="red")

dfm_code = int(input(colored("Enter code --> ", "green")))

# Set the browser log through selenium
dc = DesiredCapabilities.CHROME
dc['goog:loggingPrefs'] = { 'browser':'ALL' }

# Install ChromeDriver through code with user needing to (very cool)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get ("https://www.drfrostmaths.com/live-join-new.php")

# Enter game code
send_text('//*[@id="page"]/div[1]/div/form/div/input', dfm_code)
send_text('//*[@id="page"]/div[1]/div/form/div/input', Keys.ENTER)

log("Entered code")

# Use user login
click_element('//*[@id="dfm-button"]')

log("Clicked login")

# login
send_text('//*[@id="dfm-login"]/input[1]', username)
send_text('//*[@id="dfm-login"]/input[2]', password)

log("Sent login info")

# Click "Let's do this thing"
click_element('//*[@id="live-login-button"]')

log("Hit start")

while True:
    for item in driver.get_log('browser'):
        # Each item in the browser log
        try:
            item = str(item)
            # Remove all the random back slashes 
            match = re.findall(r'[^\\]', item)

            clean_string = "".join(match)

            # Since we can't convert the string to a dictionary we have to search for it
            answer = re.search(r'correct[aA]nswer":(?={)', clean_string)
            if answer:
                    # If the string isn't empty then we continue
                    answer_loc = answer.start()
                    small_string = clean_string[answer_loc:answer_loc+300]
                    
                    # Small string starts at the beggining of the answer

                    location = small_string.find("]")
                    
                    # Find the location of the bracket for the end of the answer 

                    final = small_string[0:location]

                    # Final is the complete answer
                    log(f'{final}')
                
            else:
                # Kinda spammy as not every item in the console contains an answer
                log("No answer found in packet...", text_color="yellow")

        except Exception as e:
            # Need to make actual exception handling
            log(e, text_color="red")
            pass

# Add auto answer function
