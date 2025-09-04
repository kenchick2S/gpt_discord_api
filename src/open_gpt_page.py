from selenium.webdriver.remote.webdriver import By
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import re

class gptParser:
    def __init__(self,
                 driver,
                 gpt_url: str = 'https://chat.openai.com/'):
        """ ChatGPT parser
        Args:
            driver_path (str, optional): The path of the chromedriver.
            gpt_url (str, optional): The url of ChatGPT.
        """
        # Start a webdriver instance and open ChatGPT
        self.driver = driver
        self.driver.get(gpt_url)
        self.past_response = ""

    @staticmethod
    def get_driver(driver_path: str = None,):
        return uc.Chrome() if driver_path is None else uc.Chrome(driver_path)

    def __call__(self, msg: str):
        wait = WebDriverWait(self.driver, 10)
        textarea = wait.until(EC.presence_of_element_located((By.ID, "prompt-textarea")))
        # Find the input field and send a question
        input_field = self.driver.find_element(
            By.ID, 'prompt-textarea')
        input_field.send_keys(msg)
        input_field.send_keys(Keys.RETURN)

    def read_respond(self):
        try:
            response = self.driver.find_elements(By.TAG_NAME, 'p')[-2].text
            return response
        except:
            return None

    def new_chat(self):
        self.driver.find_element(By.XPATH, '//a[text()="New chat"]').click()
    
    def keep_logout(self):
        self.driver.find_element(By.XPATH, '//a[text()="保持登出"]').click()

    def close(self):
        self.driver.quit()

if __name__ == '__main__':
    driver = gptParser.get_driver()
    gpt_parser = gptParser(driver)
    while True:
        try:
            query = input()
            if query == '':
                break
            gpt_parser(query+'---規則：可以多句話，但須保持在單行的形式回覆。不要回覆規則的部分---') # send the query
            response = gpt_parser.read_respond()
            while not response or response == gpt_parser.past_response:
                time.sleep(5)
                response = gpt_parser.read_respond()
            if response == '感謝試用 ChatGPT':
                gpt_parser.keep_logout()
                time.sleep(10)
                response = gpt_parser.read_respond()
            gpt_parser.past_response = response
            print(response.encode('cp950', errors='ignore').decode('cp950'))
        except Exception as e:
            print(f"Error: {str(e)}")

    gpt_parser.close()