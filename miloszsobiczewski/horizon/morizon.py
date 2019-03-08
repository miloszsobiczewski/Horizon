from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import pdb
from miloszsobiczewski.settings import BASE_DIR
import os
import smtplib
from unidecode import unidecode

class Morizon():
    def __init__(self):
        self.driver = webdriver.Firefox(
            executable_path=os.path.join(BASE_DIR, 'horizon/static/horizon/geckodriver'))
        self.driver.get("https://www.morizon.pl/dzialki/otwocki/wiazowna/")
        self.driver.set_window_size(1600, 850)

    def close(self):
        self.driver.quit()

    def set(self, min_size, max_price):
        self.driver.find_element_by_xpath('//*[@id="ps_living_area"]/div/span').click()
        size = self.driver.find_element_by_xpath('//*[@id="ps_living_area_from"]')
        size.send_keys(min_size)
        self.driver.find_element_by_xpath('//*[@id="ps_price"]/div/span/p').click()
        price = self.driver.find_element_by_xpath('//*[@id="ps_price_to"]')
        price.send_keys(max_price)
        self.driver.find_element_by_xpath('//*[@id="ps"]/section[3]/input').click()
        self.driver.find_element_by_xpath('/ html / body / div[1] / div / div / img').click()

    def search(self):
        df = pd.DataFrame(columns=['#', 'TITLE', 'SUBTITLE', 'DESC', 'PRICE', 'LINK'])
        for j in range(3, 12): #12
            for i in range(1, 36): #36
                try:
                    root = '//*[@id="contentPage"]/div/div/div/div/section/div[' + str(i) + ']/div/div/div/section'
                    title = self.driver.find_element_by_xpath(root + '/header/a/div/div[1]/h2').text
                    subtitle = self.driver.find_element_by_xpath(root + '/header/a/div/div[2]/p[2]').text
                    desc = self.driver.find_element_by_xpath(root + '/div[1]/ul').text
                    price = self.driver.find_element_by_xpath(root + '/header/a/div/div[2]/p[1]').text
                    link = self.driver.find_element_by_xpath('//*[@id="contentPage"]/div/div/div/div/section/div[' +
                                                    str(i) + ']/div/div/div/section/header/a').get_attribute('href')
                    df = df.append(
                        {'TITLE': title, 'SUBTITLE': subtitle, 'DESC': desc, 'PRICE': price, 'LINK': link},
                        ignore_index=True)
                except:
                    print('Koniec strony')
                    break

            # elm = self.driver.find_element_by_xpath('/html/body/div[2]/div[5]/section/div/div[1]/div/div')
            # //*[@id="blog-articles"]
            self.driver.execute_script("window.scroll(0, 15000);")
            # actions = ActionChains(self.driver)
            # pdb.set_trace()
            # actions.move_to_element(elm).perform()
            try:
                self.driver.find_element_by_xpath('//*[@id="contentPage"]/div/div/div/div/footer/div/nav/div/ul/li[' +
                                                  str(j) + ']/a').click()
            except:
                print('Koniec strony')
                break

            # logger('--> Loading next (' + str(j - 1) + ') page...')
        return df

    def clean(self, df, fltr):

        # pdb.set_trace()
        df['Region'], df['Town'], df['Street'] = df['TITLE'].str.split(', ').str
        df = df[~df.Town.isin(fltr)]

        df['total_price'] = 0
        df['total_price'] = df['PRICE'].str.split(' zł', expand=True)

        df['unit_price'] = 0
        df['unit_price'] = df['SUBTITLE'].str.split(' ', expand=True)
        df.loc[:, 'unit_price'] = df['unit_price'].apply(lambda x: float(x.replace(".", "").replace(",", ".")))
        # df = df.sort_values(['unit_price'], ascending=[1])


        df['Size'], df['Type'] = df['DESC'].str.split(' m² ').str
        df.loc[:, 'Size'] = df['Size'].apply(lambda x: int(x.replace(" m²", "")))
        # df.loc[:, 'Size'] = df['Size'].apply(lambda x: int(x))

        df = df[['TITLE', 'SUBTITLE', 'DESC', 'PRICE', 'LINK', 'unit_price', 'total_price', 'Size', 'Type']]
        # pdb.set_trace()
        return df

    def send(self, TO, msg_txt, PW):
        SUBJECT = '[H]orizon - land on sale raport'
        TEXT = 'This message was send from python.'
        # Gmail Sign In
        gmail_sender = 'milosz.x.44@gmail.com'
        gmail_passwd = PW

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_sender, gmail_passwd)

        msg_txt = unidecode(msg_txt)
        BODY = '\r\n'.join(['To: %s' % TO,
                            'From: %s' % gmail_sender,
                            'Subject: %s' % SUBJECT,
                            '', msg_txt + '\n' + TEXT])
        try:
            server.sendmail(gmail_sender, [TO], BODY)
            send_ind = True
        except:
            send_ind = False

        server.quit()
        return send_ind

    def mail_prep(self, df):
        msg = ''
        dim = df.shape[0]
        for i in range(dim):
            msg = msg + f'{df.iloc[i, 1]:30}   {df.iloc[i, 2]:10}   {df.iloc[i, 3]:30}   ' \
                f'{df.iloc[i, 4]:10}   {df.iloc[i, 5]:15}   {df.iloc[i, 7]:100}' + '\n'
            # print(f'{df.iloc[i, 0]:2}  {df.iloc[i, 1]:40}   {df.iloc[i, 2]:20}   {df.iloc[i, 3]:40}   {df.iloc[i, 4]:10}   {df.iloc[i, 5]:100}')
        return msg



