from django.shortcuts import render
from django.contrib import messages


# Create your views here.
def operation(request):
    import requests, urllib3
    N9kv_vlanDatabase=[]
    linedata = []
    with open("information.txt", "r") as f:
        for line in f:
            linedata = line.split("--")
    IP = linedata[0]
    Username = linedata[1]
    Password = linedata[2]
    #获取n9kv Vlandatabase数
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
    # Define SYS_URL variable
    SYS_URL = "https://"+IP+"/api/mo/sys/bd.json?query-target=subtree"
    # Obtain system information by making session.get call
    # then convert it to JSON format then filter to system attributes
    sys_info = session.get(SYS_URL, verify=False).json()["imdata"]
    # [3]["l2BD"]["attributes"]
    for line in sys_info:
        try:
            if "l2BD" in line:
                N9kv_vlanDatabase.append(line['l2BD']["attributes"]['id'])
        except:
            print("错误")

    if request.method == "POST":
        if "Add" == request.POST.get("Add", None):
            try:
                vlan_number = request.POST.get("vlan_number", None)
                if vlan_number in N9kv_vlanDatabase:
                    messages.success(request, "vlan已存在")
                    return render(request, "operation.html", locals())

                # 创建vlan
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
                # Define SYS_URL variable
                SYS_URL = "https://"+IP+"/api/mo/sys.json"
                # Obtain system information by making session.get call
                # then convert it to JSON format then filter to system attributes
                sys_info = session.get(SYS_URL, verify=False).json()["imdata"][0]["topSystem"]["attributes"]
                # Print hostname, serial nmber, uptime and current state information
                # obtained from the NXOSv9k
                # Define URL and PAYLOAD variables
                URL_2 = "https://"+IP+"/api/mo/sys/bd.json"
                PAYLOAD = {
                    "bdEntity": {
                        "children": [
                            {
                                "l2BD": {
                                    "attributes": {
                                        "fabEncap": "vlan-"+vlan_number,  # vlan的number(此行25位变量)
                                        "pcTag": "1"
                                    }}}]}}
                session.post(URL_2, json=PAYLOAD, verify=False)
                messages.success(request, "操作成功")
                # 再次获取n9kv Vlandatabase数
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
                N9kv_vlanDatabase=[]
                for line in sys_info:
                    try:
                        if "l2BD" in line:
                            N9kv_vlanDatabase.append(line['l2BD']["attributes"]['id'])
                    except:
                        print("错误")

                return render(request, "operation.html", locals())

            except:
                messages.success(request, "操作失败")
                return render(request, "operation.html", locals())
    if request.method == "POST":
        #  删除 vlan
        if  "Remove"==request.POST.get("Remove",None):
            try:
                vlan_number = request.POST.get("vlan_number", None)
                if vlan_number  not in N9kv_vlanDatabase:
                    messages.success(request, "vlan不存在")
                    return render(request, "operation.html", locals())
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
                URL_2 = "https://"+IP+"/api/mo/sys/bd.json"
                PAYLOAD = {
                "bdEntity": {
                    "children": [
                        {
                            "l2BD": {
                                "attributes": {
                                    "fabEncap": "vlan-" + vlan_number,  # vlan的number(此行25位变量)
                                    "status": "deleted"
                                }}}]}}
                session.post(URL_2, json=PAYLOAD, verify=False)

                messages.success(request, "操作成功")
                # 再次获取n9kv Vlandatabase数
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
                N9kv_vlanDatabase = []
                for line in sys_info:
                    try:
                        if "l2BD" in line:
                            N9kv_vlanDatabase.append(line['l2BD']["attributes"]['id'])
                    except:
                        print("错误")
                return render(request, "operation.html", locals())
            except:
                messages.success(request, "操作失败")
    # 处理Interface表单
    if request.method == "POST":
    # 处理Interface表单
       Eth_nubmber = request.POST.get("Eth", None)#获取端口编号值
       Port_Status = request.POST.get("Port_Status", None)#获取端口开关状态
       Switch_Port = request.POST.get("Switch_Port", None)#获取端口Switch_Port开关状态
       Select_SwitchPort_Mode= request.POST.get("Select_SwitchPort_Mode", None)#获取选择的模式
       Select_Vlan = request.POST.get("Select_Vlan", None)#获取选择的Vlan
       Port_IP = request.POST.get("Port_IP", None)#获取输入IP
       Port_Mask = request.POST.get("Port_Mask", None)#获取输入子网掩码
       Switch_Port_1="Layer3"#传输Layer2或Layer3的值
       if "True"==Switch_Port:
            Switch_Port_1="Layer2"
       if"保存"==request.POST.get("Interface_form",None):
        try:
            import requests, urllib3
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
            # 配置端口状态
            session_2 = requests.Session()
            # Define URL and PAYLOAD variables
            URL_2 = "https://"+IP+"//api/mo/sys.json"
            # 配置端口状态
            PAYLOAD = {
                    "topSystem": {
                        "children": [
                            {
                                "interfaceEntity": {
                                    "children": [
                                        {
                                            "l1PhysIf": {
                                                "attributes": {
                                                    "id": "eth1/"+Eth_nubmber,
                                                    "layer": Switch_Port_1,
                                                    "userCfgdFlags": "admin_layer",
                                                    "adminSt": Port_Status

                                                }}}]}}]}
            }
            session.post(URL_2, json=PAYLOAD, verify=False)
            # 配置端口IPv4
            session_2 = requests.Session()
            # Define URL and PAYLOAD variables
            URL_2 = "https://" + IP + "//api/mo/sys.json"
            PAYLOAD = {
                "topSystem": {
                "children": [
                {
                "ipv4Entity": {
                "children": [
                {
                "ipv4Inst": {
                "children": [
                {
                "ipv4Dom": {
                "attributes": {
                "name": "default"
                },
                "children": [
                {
  "            ipv4If": {
                "attributes": {
                "id": "eth1/"+Eth_nubmber
                                 },
                "children": [
                {
                "ipv4Addr": {
                "attributes": {
                "addr": Port_IP+"/"+Port_Mask
}}}]}}]}}]}}]}}]}}

            session.post(URL_2, json=PAYLOAD, verify=False)
            # 配置接口Access模式下的Vlan
            session_2 = requests.Session()
            # Define URL and PAYLOAD variables
            URL_2 = "https://" + IP + "//api/mo/sys.json"
            PAYLOAD = {
  "topSystem": {
    "children": [
      {
        "interfaceEntity": {
          "children": [
            {
              "l1PhysIf": {
                "attributes": {
                  "accessVlan": "vlan-"+Select_Vlan,
                  "id": "eth1/"+Eth_nubmber

}}}]}}]}}

            session.post(URL_2, json=PAYLOAD, verify=False)

            messages.success(request, Eth_nubmber+","+Port_Status+","+Switch_Port+","+Switch_Port_1+","+Select_SwitchPort_Mode+","+Select_Vlan+","+Port_IP+","+Port_Mask)
        except:
            messages.success(request, "操作失败")





    return render(request,"operation.html" , locals())
