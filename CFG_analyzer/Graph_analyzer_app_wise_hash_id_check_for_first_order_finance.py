import sys

import csv

fw=open('first_order_app_wise_hash_stats_finance.csv','w+')
# fw.write('Appname'+','+'FirstOrderID'+','+'SecondOrderID'+','+'IDs'+','+'ThirdParty'+','+'Own')
# fw.write('\n')

fw.write('App'+','+'IMEIHashed'+','+'IMEIRaw'+','+'IMSIHashed'+','+'IMSIRaw'+','+'AndroidIDHashed'+','+'AndroidIDRaw'+','+'SerialNoHashed'+','+'SerialNoRaw'+','+'MacAddressHashed'+','+'MacAddressRaw'+','+'ADvID'+','+'GUID')
fw.write('\n')

ff = open('finance_AppsName.txt','r')
#infile=sys.argv[1]
#ff = open(infile,'r')

Apps = []

for line in ff:
	line = line.strip('\n')
	Apps.append(line)

# fff = open('thirdPartyWords.txt','r')

tp_words = []

# for line in fff:
# 	line = line.strip('\n')
# 	tp_words.append(line)

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


def find_sub_method_slice_hash(alllines,method):
    print(method)
    arr=method.split('/')
    if arr[0]=="`Ljava" or arr[0]=="`Landroid":
        return 0
    index=0
    while(index<len(alllines)):
        line=alllines[index].strip()
        if method in line:
            next_line=alllines[index+1].strip()
            if next_line=="{":
                method_hash=sub_method_slice_hash(alllines,index+1)
                print("method Hash: ",method_hash)
                return method_hash
        index+=1

    return 0

def sub_method_slice_hash(alllines,num):
    lines=""

    while(num<len(alllines)):
        line=alllines[num-1].strip()
        lines+=line+" "
        if line=="})" or line=="}})" or line=="}}})":
            break
        num=num+1
    if "hashCode" in lines:
        return 1
    if "MessageDigest" in lines:
        return 1
    if "nameUUIDFromBytes" in lines:
        return 1
    if "md5" in lines:
        return 1
    return 0

def method_slice_hash(alllines,num):
    global outfile
    lines=""
    sub_method_hashed=0
    while(num<len(alllines)):
        line=alllines[num-1].strip()
        lines+=line+" "
        # outfile.write(line)
        # outfile.write('\n')
        if line=="})" or line=="}})" or line=="}}})":
            break
        num=num+1
        if "@signature" in line:
            arr=line.split('@signature')
            arr2=arr[1].split('@')
            sub_method=arr2[0].strip()
            flag=find_sub_method_slice_hash(alllines,sub_method)
            if flag==1:
                sub_method_hashed=1
    if "hashCode" in lines:
        return 1
    if "MessageDigest" in lines:
        return 1
    if "nameUUIDFromBytes" in lines:
        return 1
    if "md5" in lines:
        return 1
    if sub_method_hashed==1:
        return 1
    else:
        return 0

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
                        hash=method_slice_hash(all_lines, method_start_line)
                        print("hash: ", hash)
                        methodHash[methodname]=hash
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
                        hash=method_slice_hash(all_lines, method_start_line)
                        print("hash: ", hash)
                        methodHash[methodname]=hash
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
                    hash = method_slice_hash(all_lines, method_start_line)
                    print("hash: ", hash)
                    methodHash[methodname] = hash
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



def process_id_methods(idmethods,file,idNo):
    tp=0
    ims=idmethods.copy()
    global tp_words
    for idmetho in ims:
        for w in tp_words:
            if w in idmetho:
                #print("found third party:  ",w)
                tp+=1
                break
        if idmetho[-1] == 'V' or idmetho[-1] == 'Z' or idmetho[-1] == 'I':
            continue
        search_method(idmetho, "TopFreeApps/" + file,idNo)
    return tp



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
    im_raw= 0
    im_hash=0
    ims_raw= 0
    ims_hash=0
    aid_raw= 0
    aid_hash=0
    sid_raw= 0
    sid_hash=0
    mac_raw=0
    mac_hash=0
    adid = 0
    guid = 0

    IMEI_id_methods=find_methods(IMEI,"FinanceApps/"+file)
    IMSI_id_methods=find_methods(IMSI,"FinanceApps/"+file)
    android_id_methods=find_AndroidID_methods(AndroidID,"FinanceApps/"+file)
    mac_id_methods = find_methods(MacAddress, "FinanceApps/" + file)
    serial_id_methods = find_methods(SERIAL, "FinanceApps/" + file)
    ad_id_methods = find_methods(AdvertisingID, "FinanceApps/" + file)
    Guid_id_methods = find_methods(UUID, "FinanceApps/" + file)


    all_id_methods=IMEI_id_methods+IMSI_id_methods+android_id_methods+ad_id_methods+serial_id_methods+Guid_id_methods+mac_id_methods

    all_id_methods = list(dict.fromkeys(all_id_methods))
    for method in all_id_methods:
        id_count=0
        hashed=0
        print(file,method)
        if method=="":
            continue
        if methodHash[method]==1:
            hashed=1

        if method in IMEI_id_methods:
            id_count+=1
        if method in IMSI_id_methods:
            id_count+=1
        if method in android_id_methods:
            id_count += 1
        if method in mac_id_methods:
            id_count += 1
        if method in serial_id_methods:
            id_count += 1
        if method in ad_id_methods:
            id_count += 1
        if method in Guid_id_methods:
            id_count += 1

        if id_count >1 :
            continue


        if method in IMEI_id_methods:
            if hashed==1:
                im_hash+=1
            else:
                im_raw+=1

        if method in IMSI_id_methods:
            if hashed==1:
                ims_hash+=1
            else:
                ims_raw+=1
        if method in android_id_methods:
            if hashed==1:
                aid_hash+=1
            else:
                aid_raw+=1

        if method in mac_id_methods:
            if hashed==1:
                mac_hash+=1
            else:
                mac_raw+=1

        if method in serial_id_methods:
            if hashed==1:
                sid_hash+=1
            else:
                sid_raw+=1
        if method in ad_id_methods:
            adid+=1

        if method in Guid_id_methods:
            guid+=1




    fw.write(str(file)  + ',' +str(im_hash)+','+ str(im_raw) + ',' + str(
        ims_hash) + ','+str(ims_raw)+','+  str(aid_hash) + ','+str(aid_raw)+','+  str(sid_hash) + ','+str(sid_raw)+ ','+ str(mac_hash)+ ','+str(mac_raw)+ ',' + str(adid) + ',' + str(guid))
    fw.write('\n')

