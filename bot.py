import schedule
import time
from datetime import datetime, timedelta
import json
from decouple import config as getenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#async
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from selenium.webdriver.common.keys import Keys



def make_reserve(driver, titulo_do_card, week_day, user):
    def await_element(search_by: By, value: str, timeout=20):
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((search_by, value)))

   
    driver.get("https://cefer.reservio.com/client/login")
    driver.maximize_window()

    #logar
    await_element(By.XPATH, '//*[@id="frm-loginForm-email"]').send_keys(getenv(f"{user}_EMAIL"))
    await_element(By.XPATH, '//*[@id="frm-loginForm-password"]').send_keys(getenv(f"{user}_PASSWORD"))
    await_element(By.XPATH, '//*[@id="frm-loginForm"]/div[3]/button').click()
    await_element(By.XPATH, '/html/body/div[1]/div/h1/a').click()

    #procurar o horário desejado
    await_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]')
    await_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    await_element(By.XPATH, '//*[@id="calendar"]/div/div/div/div[2]/span/div/div/div[2]/div[2]/div[1]/button')
    cards = driver.find_elements(By.CSS_SELECTOR, '.calendarEvent.calendarEvent-color-blue')
    
    def acha_horario(card, texto):
        if texto in card.text:
            return card
        return None
        
    cards_filtrados = list(filter(None, map(lambda card: acha_horario(card, titulo_do_card), cards)))
    
    # for card in cards_filtrados:
    #     print(card.text)
    
    #print(cards_filtrados)
    cards_filtrados[week_day].find_element(By.TAG_NAME, 'button').click()

    # Clicar em Agendar
    await_element(By.XPATH, '//*[@id="calendar"]/div/div[2]/div/div[1]/div[1]')
    if len(driver.find_elements(By.XPATH, '//*[@id="calendar"]/div/div[2]/div/div[1]/div[1]/p[1]/button')) > 0:
        await_element(By.XPATH, '//*[@id="calendar"]/div/div[2]/div/div[1]/div[1]/p[1]/button').click()
        await_element(By.XPATH, '//*[@id="booking"]/div/div/span/div/div/div/span[2]/div/span[2]/div/span[1]/div/form/div[4]/div/button').click()
        time.sleep(3)
        print('reservei este horário')
    else:
        print('não consegui reservar este horário')

    driver.quit()


def main(horario, user):
    print("open main function")
    # definir o dia da semana
    week_day = datetime.today().weekday()
    if week_day >= 4:
        week_day = 0
    else:
        week_day += 1
    
    chrome_options = Options()
    chrome_options.binary_location = getenv("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-sh-usage")

    
    print(f"agendando para o dia {week_day} da semana")
    driver = webdriver.Chrome(executable_path=getenv("CHROMEDRIVER_PATH"), options=chrome_options) #
    try:
        print(f"criando reserva para {horario}")
        make_reserve(driver, horario, week_day, user)
    except Exception as e:
        print(e.__class__)



print('Hello world!')
with open("schedule.json", "r") as f:
      schedules_dict = json.loads(f.read())

for schedule_dict in schedules_dict:

  hour, minute = schedule_dict["initial_hour"].split(":")
  utc0 = timedelta(hours=float(hour), minutes=float(minute)) + timedelta(hours=3.0)
  utc0 = str(utc0)[:-3]
  print(hour)
  #if hour == "08":
      #utc0 = "03:57"
  print(utc0)

  if "monday" in schedule_dict["dias"]:
      print(schedule_dict)
      schedule.every().sunday.at(utc0).do(main, schedule_dict["card_title"], schedule_dict["user"])
  if "tuesday" in schedule_dict["dias"]:
      print(schedule_dict)
      schedule.every().monday.at(utc0).do(main, schedule_dict["card_title"], schedule_dict["user"])
  if "wednesday" in schedule_dict["dias"]:
      print(schedule_dict)
      schedule.every().tuesday.at(utc0).do(main, schedule_dict["card_title"], schedule_dict["user"])
  if "thursday" in schedule_dict["dias"]:
      print(schedule_dict)
      schedule.every().wednesday.at(utc0).do(main, schedule_dict["card_title"], schedule_dict["user"])
  if "friday" in schedule_dict["dias"]:
      print(schedule_dict)
      schedule.every().thursday.at(utc0).do(main, schedule_dict["card_title"], schedule_dict["user"])
#print(schedule.List)
  #schedule.every().day.at(utc0).do(main, schedule_dict["card_title"], schedule_dict["user"], schedule_dict["dias"])

all_jobs = schedule.get_jobs()
print(all_jobs)
main("SALA DE MUSCULAÇÃO (08H - 09H)", "ANA")
while True:
    schedule.run_pending()
    time.sleep(1)