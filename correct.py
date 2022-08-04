import time
import re
import traceback

from typing import List

from selenium import webdriver
from selenium. webdriver. common. keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select



# HERE COME YOUR PERSONAL SETTINGS
USERNAME: str ="ge73vow" # TUM user name
PASSWORD: str = "" # TUM password
PROBLEM: int = 5 # Your problem
SUBPROBLEMS: List[int] = [6, 7] # initial subproblem

class Correction():
    def __init__(self, username: str = USERNAME, 
                        password: str = PASSWORD, 
                        problem: str = PROBLEM, subproblems:
                        List[str] = SUBPROBLEMS):

        self.username = username 
        self.password = password
        self.problem = problem
        self.subproblem = subproblems[0]
        self.subproblem_list = subproblems
        
        self.exercise_position = None
       

        self.url: str = "https://2022ss-in-i2dl.hq.tumexam.de/exam/1/correction/"
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(self.url)
        
    def start(self):
        
        self.login()
        time.sleep(3)
        self.search_problem()
        command = input("Type in 'start' to start your correction when you have selected your exams which you want to correct.")
        if command == "start":
            self.correct()
    def search_problem(self): 
        element = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//input[@name="search-problem"]')))
        element.send_keys(self.problem) 
        element = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, '//input[@name="search-subproblem"]')))
        search_string = "|".join([str(nr) for nr in self.subproblem_list])
        element.send_keys(search_string) 
        time.sleep(0.5)
        element = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, '//select[@name="search-locked"]')))
        
        Select(element).select_by_visible_text("False")
        time.sleep(0.5)
        element = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, '//select[@name="search-corrected"]')))
        Select(element).select_by_visible_text("False")
        

        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="search-erid"]')))
        element.send_keys("E") 
        time.sleep(2)
        self.driver.find_elements(By.XPATH, '//a[@class="js-filtered-link"]')[0].click()
        
        
    def login(self):
        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@id="username"]')))
        element.send_keys(self.username) 

        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@id="password"]')))
        element.send_keys(self.password)

        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[@id="btnLogin"]')))
        element.click()
    


    def set_exercise_position(self):
        self.exercise_position = self.driver.execute_script('return document.getElementsByClassName("main")[0].scrollTop')
        print("Position successfully set")
    def skip(self):
        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@id="skip"]')))
        element.click()
        try:
            for i in range(2):
                alert = Alert(self.driver)
                alert.accept()
        except:
            pass
       
            
    def give_score(self, score):
        try:
            
            element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//div[@id="p{self.problem}.{self.subproblem}.1c{score}"]')))
            element.click()
        except:
            print(traceback.format_exc())
            print("something went wrong, maybe the score is not valid")

    def save_exam(self, reset_subproblem = True):
       
        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//div[@id="save"]')))
        element.click()
        self.set_subproblem(self.subproblem_list[0])
      
        self.scroll_to_exercise() 

    def comment( self, msg): 
        index_subproblem = self.subproblem_list.index(self.subproblem) 
        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//textarea[@id="correction-form-problems-{index_subproblem}-comment"]')))

        element.clear()
        element.send_keys(msg)
        

    def scroll_to_exercise(self):
        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//div[@id="p{self.problem}.{self.subproblem}.1c1"]')))
        time.sleep(0.5)
        offset = self.driver.execute_script(f'return document.getElementById("p{self.problem}.{self.subproblem}.1c1").offsetTop')
        
        self.driver.execute_script(f'document.getElementsByClassName("main")[0].scrollTo(0, {offset})')
    def close(self):
        self.driver.quit()

    def set_subproblem(self, subproblem):
        self.subproblem = subproblem
        print(f"Set subproblem to {subproblem}")

    def next_page(self):
        self.driver.execute_script("document.getElementById('pagination').style.display = 'block';")
        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//div[@id="slideRight"]')))
        element.click()

    def previous_page(self):
        self.driver.execute_script("document.getElementById('pagination').style.display = 'block';")
        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//div[@id="slideLeft"]')))
        element.click()
    

    def correct(self):
        while True:
            self.move_to_subproblem_page()

            self.scroll_to_exercise() 
            self.driver.execute_script("document.getElementById('pagination').style.display = 'none';")
            command =input(':')
            if len(command) == 0:
                print("No valid input")
            
            save_score = re.findall("^[s][0-9]", command) + re.findall("\s[s][0-9]", command)
            change_subproblem = re.findall("^[e][0-9]", command) + re.findall("\s[e][0-9]", command)
            
            next_score = re.findall("^[n][0-9]", command) + re.findall("\s[n][0-9]", command)
            
            
            if "p0" in command:
                self.previous_page()
                command.replace("p0", "")
            elif "p1" in command:
                self.next_page() 
                command.replace("p1", "")

                

            if len(change_subproblem) > 0: 
                self.set_subproblem(int(change_subproblem[0][-1]))
                command = command.replace(change_subproblem[0], "")

          
            if (len(command) > 0):
                if (command[0]!= "m"): 
                    try:
                        message_index = command.index(' m ')
                    except: message_index = False
                else: message_index = None
            else: message_index = None
            
         
             
          

            try: 
                score = int(command)
            except: 
                score = None
                
            if score: 
                self.give_score(score)

            if  (len(command) > 0) & (command == "s"):
                self.save_exam()
            
          
            if (len(command) > 0) & (command == "p"):
                self.set_exercise_position() 
            
            if message_index:  
                self.comment(command[message_index + 3: ])
                self.scroll_to_exercise()

            if command == 'f':
                self.skip()

            if (len(command) > 0) & (command == "c"):
                self.close()
                break
            if (len(command) > 0) & (command == "n"):
                self.check_subproblem_page()

            if len(save_score) > 0 :
                self.give_score(int(save_score[0][-1]))
                self.save_exam()

            
            
            if len(next_score) > 0: 
                self.give_score(int(next_score[0][-1]))
                self.check_subproblem_page()
                

    def check_subproblem_page(self):
        index_subproblem  = self.subproblem_list.index(self.subproblem) 
        
        if self.subproblem_list.index(self.subproblem) == (len(self.subproblem_list) - 1):
            self.save_exam()
        else: 
            
            self.set_subproblem(self.subproblem_list[index_subproblem + 1])           
            self.move_to_subproblem_page()

            self.scroll_to_exercise()

    def move_to_subproblem_page(self):
        while not self.driver.find_elements(By.XPATH, f'//div[@id="p{self.problem}.{self.subproblem}.1c1"]')[0].is_displayed():
            self.next_page()
            time.sleep(0.5)


if __name__ == "__main__":
    try:
        correction = Correction()
        correction.start()
    except:
        print(traceback.format_exc())
        print("Upps something went wront. Please check your settings and try again")
        correction.driver.quit()
    

    
