# we want to create an instagram bot to simulate the like action for a desired account.
# for this process we are gonna use selenium library to automate the use of web browser
# we'll use the time library to give some sleep time to wait for webpage elements to load



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class InstaBot:
    def __init__(self,username,password):    # Our bot class has a username, password and a driver for web
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()


    def CloseBrowser(self):
        self.driver.close()


    def Login(self):
        driver = self.driver
        driver.get('https://www.instagram.com/') # open the web browser defined above and go to instagram.com
        time.sleep(3) # wait for 3 seconds to load all elements of webpage

        # so far the instagram page should be loaded in the webpage but, it's the signup page not the login page!
        # we should tell the bot to click the login button on the page by using XPATH ! https://www.guru99.com/xpath-selenium.html
        # The html tag for login button ==>  <a href="/accounts/login/?source=auth_switcher">Log in</a>
        # The XPATH equivalent of the tag is ==> "//a[@href='/accounts/login/?source=auth_switcher']"] 
        # xpath = //tagname[@attribute='value']

        login_btn = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_btn.click()                        
        time.sleep(3)
        # now we are in the login page and we have to fill the username and password
        username_element = driver.find_element_by_xpath("//input[@name='username']")
        username_element.clear() # clear the field
        username_element.send_keys(self.username) # put the defined username in this field
        password_element = driver.find_element_by_xpath("//input[@name='password']")
        password_element.clear()
        password_element.send_keys(self.password)
        # after filling the username and poassword we can either click login or press enter on keyboard
        password_element.send_keys(Keys.RETURN) # pressing enter
        # because i've activated 2 step verification, after pressing enter i have to enter a security code 
        # manually so i'll make the bot wait for 7 seconds ( so i can enter the security code ) and press enter after.
        time.sleep(7)
        verification_element = driver.find_element_by_xpath("//input[@name='verificationCode']")
        verification_element.send_keys(Keys.RETURN)
        time.sleep(3)

    def Like_photos(self,hashtag):
        driver = self.driver
        driver.get('https://www.instagram.com/explore/tags/'+hashtag+'/') # open the page of desired hashtag
        time.sleep(3)
        # in the hashtag page, instagram will not load more pictures until you scroll the page down
        # so we have to simulate the scroll action with the bot
        for i in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        hrefs = driver.find_elements_by_tag_name('a') # in this line we are finding elementS insted of element ! so we have a list
        pic_hrefs = [item.get_attribute('href') for item in hrefs]
        pic_hrefs = pic_hrefs[0:len(pic_hrefs)-14] # getting rid of useless hrefs (SEE SOLVED PROBLEMS BELOW)
        # pic_hrefs = [href for href in pic_hrefs if hashtag in href] #### this is not working anymore because hashtag is not in the href anymore.
        print(hashtag + ' photos : ' + str(len(pic_hrefs)))

        for pic_href in pic_hrefs:
            driver.get(pic_href)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.find_element_by_xpath("//span[@aria-label='Like']").click()
            time.sleep(5)


      
      
shahinBot = InstaBot('username','password')
shahinBot.Login()
shahinBot.Like_photos('coding')









# SOLVED PROBLEMS
  # the href is not including the hashtag name in it !
  # when we scroll for 5 page in line 59, we have 65 hrefs which 14 of them is not useful ! it doesn't matter which hashtag we are searching for!
  # I think we have those 14 hrefs all the time even when we have only one pic in the page! YES I AM RIGHT
  # And they are always last 14 hrefs ! I should get rid of them 