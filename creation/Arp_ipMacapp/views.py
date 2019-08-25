from django.shortcuts import render
from datetime import datetime
from django import template
import json


# Create your views here.
def index7(request):
    import requests, urllib3
    arp_ifID = []
    arp_ip = []
    arp_mac = []
    linedata = []

    with open("information.txt", "r") as f:
        for line in f:
            linedata = line.split("--")
    IP = linedata[0]
    Username = linedata[1]
    Password = linedata[2]

    # 获取arp_mac_ip 表
    # Disable Self-Signed Cert warning for demo
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # Assign requests.Session instance to session variable
    session = requests.Session()
    # Define URL and PAYLOAD variables
    URL = "https://" + IP + "/api/aaaLogin.json"
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
    # Define SYS_URL variable
    SYS_URL = "https://" + IP + "/api/mo/sys/arp/inst.json?rsp-subtree=full&rsp-foreign-subtree=ephemeral&batch-id=1&batch-size=20000"
    # Obtain system information by making session.get call
    # then convert it to JSON format then filter to system attributes
    sys_info = session.get(SYS_URL, verify=False).json()["imdata"][0]["arpInst"]["children"]
    # [3]["l2BD"]["attributes"]
    if request.method == "GET":
        if "保存" == request.GET.get("保存", None):
            time = datetime.now()
            time1 = str(time.strftime("%Y_%m_%d %H_%M_%S")) + ".txt"
            f = open(time1, "w")
            f.write('')
            f.close()
            for line1 in sys_info:
                try:
                    if "arpDom" in line1:
                        for line in line1["arpDom"]["children"][0]["arpDb"]["children"]:
                            if "arpAdjEp" in line:
                                f = open(time1, "a+")
                                f.write(line['arpAdjEp']["attributes"]["ip"] + "," + line['arpAdjEp']["attributes"][
                                    "mac"] + ',' + line['arpAdjEp']["attributes"]["ifId"] + "\n")
                                f.close()
                                # arp_ifID.append(line['arpAdjEp']["attributes"]["ip"] + "," + line['arpAdjEp']["attributes"]["mac"] + ',' + line['arpAdjEp']["attributes"]["ifId"])
                                # arp_ip.append(line['arpAdjEp']["attributes"]['ip'])
                                # arp_mac.append(line['arpAdjEp']["attributes"]['mac'])



                except:
                    print("错误")

    arp_len = map(int, range(len(arp_ip)))
    return render(request, "Arp_ipMac.html", locals(), sys_info)


def zzz(List, i):
    return List[int(i)]
