import browser

browser.app.signIn()
while True:
    print("""
            1--> İstediğiniz hesabın takipçilerini getir.
            2--> İstediğiniz hesabın takip ettiklerini getir.
            3--> Kullanıcı listesini takip et.
            4--> Kullanıcı listesini takipten çık.
            5--> Takip ettiklerinizi takipten çıkın.
            6--> Çekiliş etiketleme botu.
            7--> Çıkış

    """)
    soru = int(input("Yapmak istediğiniz işlemi seçiniz: "))
    if soru == 1:
        browser.app.getFollowers()
    elif soru == 2:
        browser.app.getFollowing()
    elif soru == 3:
        browser.app.followUsers()
    elif soru == 4:
        browser.app.unFollowUsers()
    elif soru == 5:
        browser.app.unFollowFollowing()
    elif soru == 6:
        browser.app.giftBot()
    elif soru == 7:
        browser.app.exit()
        break
