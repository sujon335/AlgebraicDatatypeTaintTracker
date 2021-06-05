import sys


ff = open('TopAppsName.txt','r')

Apps = []

for line in ff:
	line = line.strip('\n')
	Apps.append(line)


IMEI="Landroid/telephony/TelephonyManager;.getDeviceId:()Ljava/lang/String;"
AndroidID="Landroid/content/Context;.getContentResolver"
SERIAL="android.os.Build.SERIAL"
IMSI="Landroid/telephony/TelephonyManager;.getSimSerialNumber:()Ljava/lang/String;"
MacAddress="Landroid/net/wifi/WifiInfo;.getMacAddress:()Ljava/lang/String;"
AdvertisingID="Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;"
UUID="Ljava/util/UUID;.randomUUID:()Ljava/util/UUID;"

def find_the_method_slice(alllines,num):
    method_start_line=-1
    methodName=""
    while (num > 0):
        text = alllines[num-1].strip()
        if (text == "</graphml>"):
            method_start_line=num+1
            break
        num=num-1
    if method_start_line>0:
        methodName=alllines[method_start_line-1].strip()
    return methodName,method_start_line



def find_methods(search_text,filename):
    global printed_methods
    id_methods = []
    try:
        with open(filename) as File:
            file_variable = open(filename)
            all_lines = file_variable.readlines()
            id_methods=[]
            for num, line in enumerate(File, 1):
                if search_text in line:
                    print('Found text at line: ', num)
                    methodname,method_start_line=find_the_method_slice(all_lines,num)
                    if methodname not in id_methods and len(methodname)>0:
                        id_methods.append(methodname)
                    if methodname not in printed_methods:
                        printed_methods.append(methodname)
                        print("Method: ", methodname)
    except:
        print("nofile")
    return id_methods

def find_AndroidID_methods(search_text,filename):
    global printed_methods
    id_methods = []
    try:
        with open(filename) as File:
            file_variable = open(filename)
            all_lines = file_variable.readlines()
            id_methods=[]
            for num, line in enumerate(File, 1):
                if search_text in line:
                    print('Found text at line: ', num)
                    text=all_lines[num+1].strip()
                    if "android_id" not in text:
                        continue
                    methodname,method_start_line=find_the_method_slice(all_lines,num)
                    if methodname not in id_methods and len(methodname)>0:
                        id_methods.append(methodname)
                    if methodname not in printed_methods:
                        printed_methods.append(methodname)
                        print("Method: ", methodname)
    except:
        print("nofile")
    return id_methods



printed_methods=[]
Foundlines=[]
methods={}
for file in Apps:
    id_methods=find_AndroidID_methods(AndroidID,"TopFreeApps/"+file)
    for method in id_methods:
        if method in methods:
            val=methods[method]
            methods[method]=val+1
        else:
            methods[method]=1

methods=sorted(methods.items(), key=lambda x: x[1], reverse=True)

c=0
for method in methods:
    print(str(method))
    if (c==15):
        break
    c+=1




