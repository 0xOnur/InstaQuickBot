from selenium import webdriver
from userinfo import username, password
from selenium.webdriver.common.keys import Keys
from csv import writer, reader
import time
import csv

class Instagram:
    
    driver_path = webdriver.Chrome("C:/webdrivers/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome(chrome_options=self.options)

    def scrollDown(self,max):
        jsKomut = """
        sayfa = document.querySelector(".isgrP");
        sayfa.scrollTo(0,sayfa.scrollHeight);
        """
        self.browser.execute_script(jsKomut)
        while True:
            # son = sayfaSonu
            time.sleep(1)
            followers = len(self.browser.find_elements_by_class_name("wo9IH"))
            self.browser.execute_script(jsKomut)
            if followers > max:
                break
    
    def signIn(self):
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(4)
        username_input = self.browser.find_element_by_name("username")
        password_input = self.browser.find_element_by_name("password")
        username_input.send_keys(username)
        password_input.send_keys(password)
        time.sleep(1)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(6)
        self.browser.get("https://www.instagram.com/")

    def getFollowers(self):
        hesap = input("Takipçisini almak istediğiniz kullanıcı: ")
        max = int(input("Almak istediğiniz kullanıcı sayısı: "))
        self.browser.get(f"https://www.instagram.com/{hesap}")
        time.sleep(3)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        time.sleep(2)
        Instagram.scrollDown(self, max)
        time.sleep(1)
        sayac = 0
        time.sleep(5)
        followers = self.browser.find_element_by_class_name("PZuss").find_elements_by_tag_name("li")
        time.sleep(1)
        for follower in followers:
            if sayac < max:
                    username = follower.find_element_by_tag_name('a').get_attribute("href").replace("https://www.instagram.com/",'').replace("/",'')
                    sayac +=1
                    print(str(sayac) + " --> " + username)
                    with open(f"files/{hesap}-followers.csv","a",encoding="UTF-8",newline='') as file:
                        csv_writer = writer(file)
                        csv_writer.writerow([username])

    def getFollowing(self):
        hesap = input("Takiplerini almak istediğiniz kullanıcı: ")
        max = int(input("Almak istediğiniz kullanıcı sayısı: "))
        self.browser.get(f"https://www.instagram.com/{hesap}")
        time.sleep(3)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
        time.sleep(2)
        Instagram.scrollDown(self,max)
        time.sleep(2)
        sayac = 0
        followers = self.browser.find_element_by_class_name("PZuss").find_elements_by_tag_name("li")
        for follower in followers:
            if sayac < max:
                username = follower.find_element_by_tag_name('a').get_attribute("href").replace("https://www.instagram.com/",'').replace("/",'')
                sayac +=1
                print(str(sayac) + " --> " + username)
                with open(f"files/{hesap}-following.csv","a",encoding="UTF-8",newline='') as file:
                    csv_writer = writer(file)
                    csv_writer.writerow([username])

    def followUser(self,user):
        self.browser.get(f"https://www.instagram.com/{user}/")
        time.sleep(2)
        takip_btn = self.browser.find_element_by_tag_name("button")
        if takip_btn.text == "Follow" or takip_btn.text == "Follow Back":
            takip_btn.click()
            time.sleep(1)
            print(f"{user} --> Takip edildi.")
        else:
            print(f"{user} --> Bu kullanıcıyı zaten takip ediyorsunuz.")

    def followUsers(self):
        user_list = input("Takip etmek istediğiniz kullanıcı listesi(**csv dosyası olmalı!** | Uzantısız yazın!): ")
        with open(f"files/{user_list}.csv","r") as file:
            csv_reader = csv.reader(file)
            for user in csv_reader:
                self.followUser(user[0])

    def unFollowUser(self,user):
        self.browser.get(f"https://www.instagram.com/{user}/")
        time.sleep(2)
        takip_btn = self.browser.find_element_by_tag_name("button")
        if takip_btn.text == 'Message':
            self.browser.find_elements_by_tag_name("button")[1].click()
            time.sleep(2)
            self.browser.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[1]').click()
            time.sleep(2)
            print(f"{user} adlı kullanıcıyı takip etmeyi bıraktınız.")
        else:
            print(f"{user} adlı kullanıcıyı zaten takip etmiyorsunuz.")

    def unFollowUsers(self):
        user_list = input("Takibi bırakmak istediğiniz kullanıcı listesi (**csv dosyası olmalı!** | Uzantısız yazın!): ")
        with open(f"files/{user_list}.csv","r") as file:
            csv_reader = csv.reader(file)
            for user in csv_reader:
                self.unFollowUser(user[0])

    def unFollowFollowing(self):
        sorgu = input("Kendi hesabınızın takip listesini oluşturdunuz mu?  (evet= e/E | hayır= h/H): ")
        if sorgu == 'e' and 'E':
            with open(f"files/{username}-following.csv") as file:
                csv_reader = csv.reader(file)
                for user in csv_reader:
                    self.unFollowUser(user[0])
        else:
            Instagram.getFollowing(self)
            print("Takip listesi oluşturuldu.")

    def comment(self,user):
        self.browser.find_element_by_xpath("//textarea[@placeholder='Add a comment…']").send_keys('@' + user + ' ')
        print(user)
        time.sleep(2)
        time.sleep(5)

    def giftBot(self):
        post_link = input("Çekiliş post linki: ")
        self.browser.get(post_link)
        user_list = input("Etiketleyeceğiniz hesapların listesi (**csv dosyası olmalı!** | Uzantısız yazın!): ")
        sayac = 0
        etiket_adet = int(input("Kaç kişi etiketlemek istiyorsunuz: "))
        time.sleep(3)
        textarea = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[3]/div/form/textarea')
        textarea.click()
        with open(f"files/{user_list}.csv","r") as file:
            csv_reader = csv.reader(file)
            for user in csv_reader:
                sayac +=1
                if sayac < etiket_adet:
                    self.comment(user[0])
                else:
                    sayac = 0
                    time.sleep(3)
                    self.comment(user[0])
                    paylas_buton = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[3]/div/form/button[2]')
                    paylas_buton.click()
                    time.sleep(5)
                    print("etiketlendi.")
                    self.browser.refresh()
                    time.sleep(5)
                    self.browser.refresh()
                    time.sleep(5)
                    textarea = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[3]/div/form/textarea')
                    textarea.click()
                    time.sleep(25)


    def exit(self):
        time.sleep(2)
        self.browser.close()


app = Instagram(username,password)
