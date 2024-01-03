from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys
import Account as ac
import pandas as pd

options = Options()
options.add_argument("start-maximized")
options.add_argument("--lang=en-US")


class Browser:
    def __init__(self, link):
        self.link = link

        service = Service(chrome_options=options,
                          executable_path=r'PATH OF YOUR BROWSER DRIVER')
        self.browser = webdriver.Chrome(service=service)
        Browser.goInstagram(self)  # To access the instagram
        Browser.quiting(self)
        sys.exit('Program finished.')

    def goInstagram(self):
        self.browser.get(self.link)
        time.sleep(2)
        Browser.login(self)
        time.sleep(2)
        Browser.getFollowers(self)
        time.sleep(2)
        Browser.getFollowing(self)
        time.sleep(2)

    def getFollowers(self):

        followers_btn = self.browser.find_element(By.XPATH, "//a[contains(@href, '/followers')]")
        followers_btn.click()
        time.sleep(2)
        Browser.scrollDown(self)
        followers = self.browser.find_elements(By.CSS_SELECTOR, '._ap3a._aaco._aacw._aacx._aad7._aade')
        followers_names = [name.text for name in followers if name.text != '']
        df_followers_names = pd.DataFrame(followers_names, columns=['followers'])
        df_followers_names.to_csv("followers.csv", header=['followers'], index=False)
        close_btn = self.browser.find_element(By.CSS_SELECTOR, "._ac7b._ac7d")
        close_btn.click()
        self.browser.refresh()  # Need to refresh the page because links are changing after clicking an action.

    def getFollowing(self):

        following_btn = self.browser.find_element(By.XPATH, "//a[contains(@href, '/following')]")
        following_btn.click()
        time.sleep(2)
        Browser.scrollDown(self)
        following = self.browser.find_elements(By.CSS_SELECTOR, '._ap3a._aaco._aacw._aacx._aad7._aade')
        following_names = [name.text for name in following if name.text != '']
        df_following_names = pd.DataFrame(following_names, columns=['following'])
        df_following_names.to_csv("following.csv", header=['following'], index=False)
        close_btn = self.browser.find_element(By.CSS_SELECTOR, "._ac7b._ac7d")
        close_btn.click()
        self.browser.refresh()  # Need to refresh the page because links are changing after clicking an action.

    def scrollDown(self):
        jsCommand = """
                page = document.querySelector("._aano");
                page.scrollTo(0, page.scrollHeight);
                var pageEnd = page.scrollHeight;
                return pageEnd;
                """
        pageEnd = self.browser.execute_script(jsCommand)
        time.sleep(2)
        while True:
            last = pageEnd
            time.sleep(2)
            pageEnd = self.browser.execute_script(jsCommand)
            time.sleep(2)
            if last == pageEnd:
                break

    def login(self):
        username = self.browser.find_element(By.NAME, "username")
        password = self.browser.find_element(By.NAME, "password")

        username.send_keys(ac.username)
        password.send_keys(ac.password)
        time.sleep(2)

        loginBtn = self.browser.find_element(By.CSS_SELECTOR, "#loginForm > div > div:nth-child(3)")
        loginBtn.click()
        time.sleep(4)

        self.browser.get(self.link + "/" + ac.username)  # It is for your profile.
        # self.browser.get(self.link + "/USERNAME") # It is username of the person you want to analyze.
        time.sleep(3)

    def quiting(self):
        self.browser.close()


if __name__ == "__main__":
    Browser("https://www.instagram.com/")
    time.sleep(1000)
