import sys

import csv

fw=open('Apps_that_use_Financial_libs.txt','w+')
# fw.write('Appname'+','+'FirstOrderID'+','+'SecondOrderID'+','+'IDs'+','+'ThirdParty'+','+'Own')
# fw.write('\n')


ff = open('TopAppsName.txt','r')
#infile=sys.argv[1]
#ff = open(infile,'r')

Apps = []

for line in ff:
    line = line.strip('\n')
    Apps.append(line)

fff = open('thirdPartyFinancialWords.txt','r')

tpf_words = []

for line in fff:
    line = line.strip('\n')
    tpf_words.append(line)

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
    global methodHash
    id_methods = []
    try:
        with open(filename) as File:
            file_variable = open(filename)
            all_lines = file_variable.readlines()
            id_methods=[]
            for num, line in enumerate(File, 1):
                if search_text in line:
                    #print('Found text at line: ', num)
                    methodname,method_start_line=find_the_method_slice(all_lines,num)
                    if methodname not in id_methods and len(methodname)>0:
                        id_methods.append(methodname)

    except:
        print("nofile",filename)
    return id_methods

def find_AndroidID_methods(search_text,filename):
    id_methods = []
    try:
        with open(filename) as File:
            file_variable = open(filename)
            all_lines = file_variable.readlines()
            id_methods=[]
            for num, line in enumerate(File, 1):
                if search_text in line:
                    #print('Found text at line: ', num)
                    text=all_lines[num+1].strip()
                    if "android_id" not in text:
                        continue
                    methodname,method_start_line=find_the_method_slice(all_lines,num)
                    if methodname not in id_methods and len(methodname)>0:
                        id_methods.append(methodname)

    except:
        print("nofile",filename)
    return id_methods


def search_method(search_text,filename,idNo):
    global IMEI_id_methods, IMSI_id_methods, android_id_methods, ad_id_methods,serial_id_methods,Guid_id_methods,mac_id_methods
    with open(filename) as File:
        file_variable = open(filename)
        all_lines = file_variable.readlines()
        text_calling_methods=[]
        for num, line in enumerate(File, 1):
            if search_text in line:
                #print('Found text at line: ', num)
                #print(all_lines[num - 1])
                if(num in Foundlines):
                    continue
                methodname,method_start_line=find_the_method_slice(all_lines,num)
                if methodname.__contains__(".onClick"):
                    continue
                global printed_methods
                if methodname in printed_methods:
                    continue
                if methodname.strip()==search_text.strip():
                    continue
                if methodname not in text_calling_methods and len(methodname)>0:
                    text_calling_methods.append(methodname)

        if(idNo==1):
            IMEI_id_methods+=text_calling_methods
        elif (idNo==2):
            IMSI_id_methods+=text_calling_methods
        elif (idNo==3):
            android_id_methods+=text_calling_methods
        elif(idNo==5):
            serial_id_methods+=text_calling_methods
        elif(idNo==6):
           ad_id_methods+=text_calling_methods
        elif(idNo==4):
            mac_id_methods+=text_calling_methods
        else:
            Guid_id_methods += text_calling_methods






libraries_apps_count={}
libraries_hash={}
libraries_imei={}
libraries_imsi={}
libraries_aid={}
libraries_serial={}
libraries_mac={}
libraries_adid={}
libraries_guid={}
schemeMethods={}
methodHash={}
Foundlines = []
printed_methods = []
methods = {}
IMEI_id_methods=[]
IMSI_id_methods=[]
mac_id_methods=[]
android_id_methods=[]
serial_id_methods=[]
ad_id_methods=[]
Guid_id_methods=[]
own_package_count=0
for file in Apps:
    IMEI_id_methods=find_methods(IMEI,"TopFreeApps/"+file)
    IMSI_id_methods=find_methods(IMSI,"TopFreeApps/"+file)
    android_id_methods=find_AndroidID_methods(AndroidID,"TopFreeApps/"+file)
    mac_id_methods = find_methods(MacAddress, "TopFreeApps/" + file)
    serial_id_methods = find_methods(SERIAL, "TopFreeApps/" + file)
    ad_id_methods = find_methods(AdvertisingID, "TopFreeApps/" + file)
    Guid_id_methods = find_methods(UUID, "TopFreeApps/" + file)


    all_id_methods=IMEI_id_methods+IMSI_id_methods+android_id_methods+ad_id_methods+serial_id_methods+Guid_id_methods+mac_id_methods

    all_id_methods = list(dict.fromkeys(all_id_methods))
    financial = 0
    for method in all_id_methods:
        print(file,method)
        if method=="":
            continue

        try:
            arr=method.split(';')
            lib_method=arr[0]
        except:
            continue

        for w in tpf_words:
            if w in lib_method:
                financial=1
                break

        if financial==1:
            break


    if financial==1:
        fw.write(str(file))
        fw.write('\n')




