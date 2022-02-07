import schedule
import time
from datetime import datetime
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#async
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_argument("--headless")

def make_reserve(driver, titulo_do_card, week_day):
    def await_element(search_by: By, value: str, timeout=20):
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((search_by, value)))

   
    driver.get("https://cefer.reservio.com/client/login")
    driver.maximize_window()

    #logar
    await_element(By.XPATH, '//*[@id="frm-loginForm-email"]').send_keys(os.environ.get("EMAIL"))
    await_element(By.XPATH, '//*[@id="frm-loginForm-password"]').send_keys(os.environ.get("PASSWORD"))
    await_element(By.XPATH, '//*[@id="frm-loginForm"]/div[3]/button').click()
    await_element(By.XPATH, '/html/body/div[1]/div/h1/a').click()

    #procurar o horário desejado
    await_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]')
    await_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    await_element(By.XPATH, '//*[@id="calendar"]/div/div/div/div[2]/span/div/div/div[2]/div[2]/div[1]/button')
    #//*[@id="calendar"]/div/div/div/div[2]/span/div/div/div[2]/div[2]/div[1]
    #.calendarEvent.calendarEvent-color-blue
    #.calendarEvent.calendarEvent-color-blue.calendarEvent-inactive
    cards = driver.find_elements(By.CSS_SELECTOR, '.calendarEvent.calendarEvent-color-blue')
    
    def acha_horario(card, texto):
        if texto in card.text:
            return card
        return None
        
    cards_filtrados = list(filter(None, map(lambda card: acha_horario(card, titulo_do_card), cards)))
    
    for card in cards_filtrados:
        print(card.text)
    
    #print(cards_filtrados)
    cards_filtrados[week_day].find_element(By.TAG_NAME, 'button').click()
    #time.sleep(3)

    # Clicar em Agendar
    await_element(By.XPATH, '//*[@id="calendar"]/div/div[2]/div/div[1]/div[1]')
    if len(driver.find_elements(By.XPATH, '//*[@id="calendar"]/div/div[2]/div/div[1]/div[1]/p[1]/button')) > 0:
        await_element(By.XPATH, '//*[@id="calendar"]/div/div[2]/div/div[1]/div[1]/p[1]/button').click()
        await_element(By.XPATH, '//*[@id="booking"]/div/div/span/div/div/div/span[2]/div/span[2]/div/span[1]/div/form/div[4]/div/button').click()
        time.sleep(3)
        print('reservei este horário')
    else:
        print('não consegui reservar este horário')
    #pyautogui.click(x=675, y=282)

    # Janela de reserva, agendar
    #pyautogui.click(x=1000, y=749)

def main():
    # definir o dia da semana
    week_day = datetime.today().weekday()
    if week_day >= 4:
        week_day = 0
    else:
        week_day += 1
    print(week_day)

    #definir o horário a ser reservado
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    start_time = current_time[0:2]
    print(start_time)
    finish_time = int(start_time) + 1
    print(finish_time)
    
    if finish_time <= 9:
        horario = f"SALA DE MUSCULAÇÃO ({start_time}H - 0{finish_time}H)"
    else:
        horario = f"SALA DE MUSCULAÇÃO ({start_time}H - {finish_time}H)"
    print(horario)
    

    driver = webdriver.Chrome("./chromedriver.exe", chrome_options=chrome_options) #
    make_reserve(driver, horario, week_day)

#//*[@id="calendar"]/div/div[2]/div/div[1]/div[1]/p[1]/button/span
#//*[@id="calendar"]/div/div[2]/div/div[1]/div[1]/p[1]/button
#//*[@id="booking"]/div/div/span/div/div/div/span[2]/div/span[2]/div/span[1]/div/form/div[4]/div/button

#schedule.every().monday.at("06:00").do(main)
#schedule.every().monday.at("07:00").do(main)
#schedule.every().monday.at("08:00").do(main)
#schedule.every().monday.at("09:00").do(main)
#schedule.every().monday.at("10:00").do(main)
schedule.every().monday.at("16:00").do(main)
schedule.every().monday.at("17:00").do(main)
schedule.every().monday.at("18:00").do(main)
schedule.every().monday.at("19:00").do(main)


while True:
    schedule.run_pending()
    time.sleep(1)
