
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from waiters.waiters import Waiters
import time
import json

class SejmScraper:
    def __init__(self, driver):
        self.driver = driver
        self.waiters = Waiters(self.driver)

    def collect_html_sources(self, url,output_file):
        data_html_pairs = []
        try:
            self.driver.get(url)
            for i in range(1, 16):
                projectXPATH = f'//*[@id="table"]/tbody/tr[{i}]/td[1]/a'
                dateXPATH = f'//*[@id="table"]/tbody/tr[{i}]/td[4]'
                sejmRefXPATH = '//div[@class="row"]//div//div[@class="row"]//a[@target="_blank"][contains(text(),"Dalszy ciąg procesu legislacyjnego powyższego proj")]'
                procXPATH = '//*[@id="view:_id1:_id2:facetMain"]/div/ul'
                procButton = 'proc'

                try:
                    project = self.driver.find_element(By.XPATH, projectXPATH)
                    date = self.driver.find_element(By.XPATH, dateXPATH)
                    date_text = date.text

                    ActionChains(self.driver).key_down(Keys.CONTROL).click(project).key_up(Keys.CONTROL).perform()
                    self.driver.switch_to.window(self.driver.window_handles[-1])

                    self.waiters.wait_until_element_visible((By.XPATH, sejmRefXPATH))
                    self.driver.find_element(By.XPATH, sejmRefXPATH).click()
                    self.driver.switch_to.window(self.driver.window_handles[-1])

                    self.waiters.wait_until_element_visible((By.CLASS_NAME, procButton))
                    self.driver.find_element(By.CLASS_NAME, procButton).click()

                    procElements = self.waiters.wait_until_element_visible((By.XPATH, procXPATH))
                    data_html_pairs.append({"date": date_text, "html": procElements.get_attribute('outerHTML')})

                except Exception as e:
                    print(f"Nie znaleziono procesu{i}, przejście do następnego procesu.")

                finally:
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        time.sleep(10)
        finally:
            self.driver.quit()

        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data_html_pairs, file, ensure_ascii=False, indent=4)

        return data_html_pairs