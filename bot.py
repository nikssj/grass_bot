from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
from selenium.common.exceptions import WebDriverException

csv_file = "pags.csv"

# Ruta al controlador del navegador (ChromeDriver en este caso)


# Inicializar el navegador
driver = webdriver.Chrome()
 
try:
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row['url']
            try:
                # Visitar la URL
                driver.get(url)
                print("Visitando:", url)
                # Esperar unos segundos antes de pasar a la siguiente URL
                time.sleep(2)  # Cambia este valor según lo que necesites
            except WebDriverException as e:
                print(f"No se pudo cargar la URL {url}: {str(e)}")
                continue  # Pasar a la siguiente URL
finally:
    # Cerrar el navegador al finalizar
    driver.quit()
    