from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import os
import shutil
import time as t
import subprocess as s

user = ""
password = ""
folder_name = ""
folder_aux = ""
phpsessid = ""

list_not_downloaded = []


def leer_credenciales(archivo='datos.txt'):
    """
    Lee las credenciales e información necesaria desde un archivo de texto.

    :param archivo: Nombre del archivo de texto con las credenciales.
    :return: Un diccionario con los datos de usuario, contraseña y rutas de carpetas.
    """
    datos = {}

    try:
        with open(archivo, 'r') as file:
            for line in file:
                clave, valor = line.strip().split(': ', 1)
                datos[clave] = valor
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{archivo}'.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

    return datos

def login(driver, user, password):
    #open the page
    driver.get("https://jutge.org/")
    driver.find_element("name", "email").send_keys(user)
    driver.find_element("name", "password").send_keys(password)
    #find button and click
    driver.find_element("name", "submit").click()
    #check if info is correct
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@title="Dashboard"]')))
        return True
    except:
        return False


def download_code(driver, link, problem_id):
    path_submisions = link + '/submissions'
    driver.get(path_submisions)
    tr_elements = driver.find_elements(By.TAG_NAME, "tr")
    for tr in tr_elements:
        lista = tr.find_elements(By.CLASS_NAME, "col-sm-1")
        if (len(lista) >= 3):
            img_element = lista[0].find_element(By.TAG_NAME, "img")
            value = img_element.get_attribute("src")
            if value[22:27] != "green":
                continue
            link_submission = lista[2].find_element(By.TAG_NAME, "a").get_attribute("href")
            return download(link_submission, driver, "code", problem_id)
    return False

def download(link, driver, tipo, problem_id):
    if tipo == "code":
        driver.get(link + '/download')
        try:
            WebDriverWait(driver, 0.5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@class='alert alert-danger ']")))
            return False
        except:
            return True
        
    elif tipo == "pdf":
        session = requests.Session()
        session.cookies.set('PHPSESSID', phpsessid)
        response = session.get(link + '/pdf')

        if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
            with open(os.path.join(folder_aux, "problem.pdf"), 'wb') as f:
                f.write(response.content)
            print("PDF descargado correctamente.")
            return True
        else:
            print("No se ha podido descargar el PDF. Respuesta HTTP:", response.status_code)
            return False
        
def move(problem_id):
    for file in os.listdir(folder_aux):
        if "program.cc" in file or "program.tar" in file:
            shutil.move(os.path.join(folder_aux, file), os.path.join(folder_name, problem_id))
        if "problem.pdf" in file:
            shutil.move(os.path.join(folder_aux, file), os.path.join(folder_name, problem_id))
    if len(os.listdir(folder_aux)) != 0:
        return False
    
    return True

    
def cada_problem(driver, link):
    problem_id = link[27:33]

    folder_path = os.path.join(folder_name, problem_id)
    if os.path.exists(folder_path):
        print(f"El problema {problem_id} ya existe en la carpeta")

        return True
    
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(link)
    if not download(link, driver, "pdf", problem_id):
        print(f"ERROR 100 Hubo un problema descargando {problem_id}")
        list_not_downloaded.append(problem_id)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return
    
    if not download_code(driver, link, None):
        print(f"ERROR 101 Hubo un problema descargando {problem_id}")
        list_not_downloaded.append(problem_id)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return
    
    print(f"Pdf y codigo de {problem_id} descargado")

    os.makedirs(folder_path)
    if move(problem_id):
        print(f"El problema {problem_id} se ha movido")
    else:
        print(f"Hubo un problema moviento los archivos de {problem_id}")
        list_not_downloaded.append(problem_id)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def eliminar_directorios_con_condiciones(directorio):
    for root, dirs, files in os.walk(directorio, topdown=False):
        condicion_tar = any(file.endswith('.tar') for file in files)
        condicion_un_fichero = len(files) == 1
        condicion_peso = any(os.path.getsize(os.path.join(root, file)) == 0 for file in files)
        problem_id = root[-6:]

        if condicion_tar:
            try:
                shutil.rmtree(root)
            except:
                print(f"Error al eliminar {root}")
        elif condicion_un_fichero:
            try:
                print(f"La carpeta del problema {problem_id} solamente tenia un fichero")
                list_not_downloaded.append(problem_id)
                shutil.rmtree(root)
            except:
                print(f"Error al eliminar {root}")
        elif condicion_peso:
            try:
                print(f"La carpeta del problema {problem_id} tenia un fichero de 0 bytes")
                list_not_downloaded.append(problem_id)
                shutil.rmtree(root)
            except:
                print(f"Error al eliminar {root}")


def main():
    time_start = t.time()    

    global user, password, folder_name, folder_aux, phpsessid
    datos = leer_credenciales() #lee datos.txt
    user = datos['user']
    password = datos['password']
    folder_name = datos['folder_name']
    phpsessid = datos['PHPSESSID']
    username = s.run("whoami", stdout=s.PIPE, text= True).stdout.strip()
    folder_aux = f"/home/{username}/aux"

    #estas configuraciones son para que no salga la ventana de chrome y para que la descarga
    #se redirija a la carpeta que queremos
    chrome_options = Options()

    prefs = {
        "download.default_directory": folder_aux,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
        }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)

    if not login(driver, user, password):
        print("Credentials are not correct")
        exit()

    if os.path.exists(folder_aux):
        shutil.rmtree(folder_aux)
    os.makedirs(folder_aux)    
    
    driver.get("https://jutge.org/problems/accepted")

    #localiza la tabla de problemas
    tabla = driver.find_elements(By.CLASS_NAME, "table")
    filas = tabla[0].find_elements(By.TAG_NAME, "a")

    for problema in filas:
        link = problema.get_attribute("href")
        if link[-3:] != "pdf":
            cada_problem(driver, link)

    eliminar_directorios_con_condiciones(folder_name)

    #elimina las problemas que eran un .tar o si la carpeta tenia solo 1 archivo o un archivo con 0 bytes
    if (len(list_not_downloaded) > 0):
        print("\n Ha habido problemas con los siguientes problemas:")
        print(list_not_downloaded)
        print("A veces los problemas que pertenecen a examenes están más protegidos que el resto y los archivos no se descargan correctamente")
        print("El resto de errores son desconocidos y se está trabajando en ello")

    if os.path.exists(folder_aux):
        shutil.rmtree(folder_aux)
    
    driver.close()
    time_end = t.time()
    time = time_end - time_start
    minutes = int(time/60)
    seconds = int(time%60)
    print(f"Tiempo de ejecución: {minutes} minutos y {seconds} segundos")
    
if __name__ == '__main__':
    main()