# ScrapperJutge
ESPAÑOL:

Descripción
Este proyecto consiste en un script de Python diseñado para realizar webscraping en la página web de Jutge.org, una plataforma utilizada por estudiantes de la Universidad Politécnica de Cataluña (UPC) de la Facultad de Informática de Barcelona (FIB) para aprender a programar. El script permite a los usuarios descargar automáticamente todos los programas que han enviado a Jutge.org, junto con sus respectivos enunciados.
Instalación
Para utilizar este script, primero asegúrate de tener Python instalado en tu sistema. Luego, clona este repositorio en tu máquina local utilizando:

git clone https://github.com/miguelxsm/ScrapperJutge

El script requiere las siguientes bibliotecas de Python, que puedes instalar usando `pip3`:

pip3 install -r requirements.txt

El archivo `requirements.txt` se incluye en el repositorio.

IMPORTANTE (pasos previos)
Es necesario que antes de ejecutar el script hagas unos pequeños cambios en el arhivo datos.txt:
1. Poner tus creedenciales del Jutge
2. Especificar el PATH ABSOLUTO de la carpeta donde quieres que se descarguen los problemas.
3. Especificar el PHPSESSID:
   3.1. Entrar a un problema cualquiera de Jutge, como por ejemplo https://jutge.org/problems/P99182_es
   3.2. Pulsar F12 y situarse en la pestaña de 'Network'
   3.3. Pulsar F5 o refrescar la página (así es visible una request)
   3.4 Se desplegará una lista, pinchar en la que tiene el ID del problema, en el caso anterior P99182_es
   3.5. Buscar la linea donde pone Cookie y copiar el valor de PHPSESSID, en mi caso aparece así: PHPSESSID=t9hi61slc6rtf1cgfqspedm8bi;
   3.6 Poner el valor de PHPSESSID en el fichero datos.txt

Uso
Para ejecutar el script, navega al directorio donde se encuentra el archivo `scrapper_jutge.py` y ejecútalo con:

python3 scrapper_jutge.py

Tendrás que esperar a que termine el Script sin usar el ordenador para tenerlo todo listo ya que la librería Selenium funciona a tiempo real.

ENGLISH:

Description
This project consists of a Python script designed to perform web scraping on the Jutge.org website, a platform used by students of the Polytechnic University of Catalonia (UPC) at the Faculty of Informatics of Barcelona (FIB) to learn programming. The script allows users to automatically download all the programs they have submitted to Jutge.org, along with their respective statements.
Installation
To use this script, first make sure you have Python installed on your system. Then, clone this repository to your local machine using:

git clone https://github.com/miguelxsm/ScrapperJutge

The script requires the following Python libraries, which you can install using pip3:

pip3 install -r requirements.txt

The `requirements.txt` file is included in the repository.
IMPORTANT (Preliminary Steps)
It is necessary that before executing the script you make some small changes in the `datos.txt` file:

- Enter your Jutge credentials.
- Specify the ABSOLUTE PATH of the folder where you want the problems to be downloaded.
- Specify the ABSOLUTE PATH of an auxiliary folder for the program to function correctly (this folder is deleted and created each time the program is executed).
Usage
To execute the script, navigate to the directory where the `scrapper_jutge.py` file is located and run it with:

python3 scrapper_jutge.py

You will have to wait for the script to finish without using the computer to have everything ready, since the Selenium library works in real time.
