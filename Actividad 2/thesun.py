import random
import string
import time

import pyautogui
from selenium import webdriver


# Recordar que la variable en este caso se llamará "driver",
# con la que deberán trabajar los códigos.
# Existen ocasiones en las cuales la página necesita tiempo para cargar y
# si se realizan acciones demasiado rápido, se descoordina el programa y termina.
# Es recomendable en este caso usar #time.sleep(1) o los segundos que usted desee que espere.
def spawn_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.todocodigos.cl/")
    driver.set_window_position(1, 1)
    driver.set_window_size(1300, 700)
    return driver


spawn_browser()


def signIn(nombre, apellido, password, email):
    email, terminacion = email.split("@")
    pyautogui.moveTo(1080, 180, 1)  # iniciarSesion  moveTo(x,y,tiempo)
    pyautogui.click()
    time.sleep(5)
    pyautogui.moveTo(730, 295, 1)
    pyautogui.click()
    pyautogui.click()
    pyautogui.moveTo(568, 535, 1)
    pyautogui.click()
    pyautogui.write(email)
    pyautogui.hotkey("altright", "q")
    pyautogui.write(terminacion)
    pyautogui.press("tab")
    pyautogui.write(password)
    pyautogui.press("tab")
    pyautogui.write(nombre)
    pyautogui.press("tab")
    pyautogui.write(apellido)
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("enter")
    pyautogui.press("tab")
    pyautogui.press("enter")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("enter")


# signIn("Benjamin","Aguirre","fork123","3pur1o@gmail.com","962299018","11298581-6")
def logIn(password, email):
    email, terminacion = email.split("@")
    pyautogui.moveTo(1080, 180, 1)  # iniciarSesion  moveTo(x,y,tiempo)
    pyautogui.click()
    time.sleep(10)
    pyautogui.moveTo(523, 432)
    pyautogui.click()
    pyautogui.click()
    pyautogui.write(email)
    pyautogui.hotkey("altright", "q")
    pyautogui.write(terminacion)
    pyautogui.press("tab")
    pyautogui.write(password)
    pyautogui.press("enter")


def passchange(password, email, nuevaPass, logIn):
    logIn(password, email)
    time.sleep(10)
    pyautogui.moveTo(1080, 180, 1)  # iniciarSesion  moveTo(x,y,tiempo)
    pyautogui.click()
    time.sleep(5)
    pyautogui.moveTo(1241, 151, 1)
    pyautogui.click()
    time.sleep(5)
    pyautogui.moveTo(1183, 233, 1)
    pyautogui.click()
    pyautogui.click()
    time.sleep(10)
    pyautogui.write(password)
    pyautogui.press("tab")
    pyautogui.write(nuevaPass)
    pyautogui.press("tab")
    pyautogui.write(nuevaPass)
    pyautogui.press("enter")


def reestablecer(email):
    email, terminacion = email.split("@")
    pyautogui.moveTo(1080, 180, 1)
    pyautogui.click()
    time.sleep(10)
    pyautogui.moveTo(546, 563, 1)
    pyautogui.click()
    time.sleep(4)
    pyautogui.write(email)
    pyautogui.hotkey("altright", "q")
    pyautogui.write(terminacion)
    pyautogui.press("enter")


# signIn("Benjamin","Aguirre","Thesun1234","3pur1o@gmail.com")
# logIn("Thesun1234","3pur1o@gmail.com")
# passchange("Thesun1234","3pur1o@gmail.com","Thesun12345",logIn)
# reestablecer("3pur1o@gmail.com")
def generador():
    letras = string.ascii_lowercase
    resultado = "".join(random.choice(letras) for i in range(6))
    return resultado


def fuerza(mail):

    password = generador()
    logIn(password, "3pur1o@gmail.com")
    for j in range(1, 150):
        print("intento " + str(j) + " con la pass " + password)
        time.sleep(5)
        pyautogui.moveTo(540, 559)
        pyautogui.click()
        pyautogui.click()
        pyautogui.hotkey("delete")
        password = generador()
        pyautogui.write(password)
        pyautogui.press("enter")


fuerza("3pur1o@gmail.com")
