from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import requests, urllib3
# Create your views here.
def login(request):
    datalist =[]
    if request.method == "POST":
        IP = request.POST.get("IP",None)
        Username = request.POST.get("Username",None)
        Password = request.POST.get("Password",None)
        try:
            # Disable Self-Signed Cert warning for demo
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            # Assign requests.Session instance to session variable
            session = requests.Session()

            # Define URL and PAYLOAD variables
            URL = "https://"+IP+"/api/aaaLogin.json"
            PAYLOAD = {
                "aaaUser": {
                    "attributes": {
                        "name": Username,
                        "pwd": Password
                    }
                }
            }

            # Obtain an authentication cookie
            session.post(URL, json=PAYLOAD, verify=False)
            SYS_URL = "https://"+IP+"/api/mo/sys.json"
            sys_info = session.get(SYS_URL, verify=False).json()["imdata"][0]["topSystem"]["attributes"]
            with open("information.txt", "w+") as f:
                f.write("{}--{}--{}--\n".format(IP, Username, Password))
            messages.success(request, "登录成功")
            return render(request, "Switching.html")

        except:
            messages.success(request, "登录失败")
            return render(request, "login.html")


    if request.method=="GET":
        pass


    return render(request,"login.html")