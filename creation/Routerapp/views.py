from django.shortcuts import render
import urllib3, requests
from django.contrib import messages


# Create your views here.
def index2(request):
    linedata = []
    with open("information.txt", "r") as f:
        for line in f:
            linedata = line.split("--")
    IP = linedata[0]
    Username = linedata[1]
    Password = linedata[2]
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
    SYS_URL = "https://" + IP + "/api/mo/sys/bd.json?query-target=subtree"
    # Obtain system information by making session.get call
    # then convert it to JSON format then filter to system attributes
    sys_info = session.get(SYS_URL, verify=False).json()["imdata"]
    # [3]["l2BD"]["attributes"]

    if request.method == "POST":
        # 添加静态路由
        if "Add_StaticRouter" == request.POST.get("Add_StaticRouter", None):
            try:

                Static_netIP = request.POST.get("Static_netIP", None)
                Static_SubnetMark = request.POST.get("Static_SubnetMark", None)
                Static_Nexthop = request.POST.get("Static_Nexthop", None)
                print(Static_netIP,Static_SubnetMark,Static_Nexthop)
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
                SYS_URL = "https://" + IP + "/api/mo/sys.json"
                # Obtain system information by making session.get call
                # then convert it to JSON format then filter to system attributes
                sys_info = session.get(SYS_URL, verify=False).json()["imdata"][0]["topSystem"]["attributes"]
                # Print hostname, serial nmber, uptime and current state information
                # obtained from the NXOSv9k
                # Define URL and PAYLOAD variables
                URL_2 = "https://" + IP + "/api/mo/sys/ipv4/inst.json"
                PAYLOAD = {
                    "ipv4Inst": {
                        "children": [
                            {
                                "ipv4Dom": {
                                    "attributes": {
                                        "name": "default"
                                    },
                                    "children": [
                                        {
                                            "ipv4Route": {
                                                "attributes": {
                                                    "prefix": Static_netIP+"/"+Static_SubnetMark
                                                },
                                                "children": [
                                                    {
                                                        "ipv4Nexthop": {
                                                            "attributes": {
                                                                "nhAddr": Static_Nexthop+"/32",
                                                                "nhIf": "unspecified",
                                                                "nhVrf": "default"
                                                            }}}]}}]}}]}}
                session.post(URL_2, json=PAYLOAD, verify=False)
                messages.success(request, "操作成功")
                return render(request, "Router.html")

            except:
                messages.success(request, "操作失败")

    return render(request, "Router.html",locals())
