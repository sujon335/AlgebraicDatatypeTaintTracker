import sys

import csv

fw=open('Updated_finance_app_wise_thirdparty_stats.csv','w+')
# fw.write('Appname'+','+'FirstOrderID'+','+'SecondOrderID'+','+'IDs'+','+'ThirdParty'+','+'Own')
# fw.write('\n')

fw.write('App'+','+'IMEIHashed(TP)'+','+'IMEIRaw(TP)'+','+'IMEIHashed(O)'+','+'IMEIRaw(O)'+','+'IMSIHashed(TP)'+','+'IMSIRaw(TP)'+','+'IMSIHashed(O)'+','+'IMSIRaw(O)'+','+'AndroidIDHashed(TP)'+','+'AndroidIDRaw(TP)'+','+'AndroidIDHashed(O)'+','+'AndroidIDRaw(O)'+','+'SerialNoHashed(TP)'+','+'SerialNoRaw(TP)'','+'SerialNoHashed(o)'+','+'SerialNoRaw(o)'+','+'MacAddressHashed(TP)'+','+'MacAddressRaw(TP)'+','+'MacAddressHashed(O)'+','+'MacAddressRaw(O)'+','+'ADvID(TP)'+','+'ADvID(O)'+','+'GUID(TP)'+','+'GUID(O)')
fw.write('\n')

ff = open('updated_finance_AppsName.txt','r')
#infile=sys.argv[1]
#ff = open(infile,'r')

Apps = []

for line in ff:
	line = line.strip('\n')
	Apps.append(line)

fff = open('thirdPartyWords.txt','r')

tp_words = []

for line in fff:
	line = line.strip('\n')
	tp_words.append(line)

#print(tp_words)
# fff = open('thirdPartyWords.txt','r')


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
    #print(method)
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
                #print("method Hash: ",method_hash)
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
                        #print("hash: ", hash)
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
                        #print("hash: ", hash)
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
                    #print("hash: ", hash)
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
count=0
for file in Apps:
    im_raw_tp= 0
    im_hash_tp=0
    im_raw_o= 0
    im_hash_o=0
    ims_raw_tp= 0
    ims_hash_tp=0
    ims_raw_o= 0
    ims_hash_o=0
    aid_raw_tp= 0
    aid_hash_tp=0
    aid_raw_o= 0
    aid_hash_o=0
    sid_raw_tp= 0
    sid_hash_tp=0
    sid_raw_o= 0
    sid_hash_o=0
    mac_raw_tp=0
    mac_hash_tp=0
    mac_raw_o=0
    mac_hash_o=0
    adid_tp = 0
    guid_tp = 0
    adid_o = 0
    guid_o = 0

    IMEI_id_methods=find_methods(IMEI,"FinanceAppsOutputUpdated/"+file)
    IMSI_id_methods=find_methods(IMSI,"FinanceAppsOutputUpdated/"+file)
    android_id_methods=find_AndroidID_methods(AndroidID,"FinanceAppsOutputUpdated/"+file)
    mac_id_methods = find_methods(MacAddress, "FinanceAppsOutputUpdated/" + file)
    serial_id_methods = find_methods(SERIAL, "FinanceAppsOutputUpdated/" + file)
    ad_id_methods = find_methods(AdvertisingID, "FinanceAppsOutputUpdated/" + file)
    Guid_id_methods = find_methods(UUID, "FinanceAppsOutputUpdated/" + file)


    all_id_methods=IMEI_id_methods+IMSI_id_methods+android_id_methods+ad_id_methods+serial_id_methods+Guid_id_methods+mac_id_methods

    all_id_methods = list(dict.fromkeys(all_id_methods))
    for method in all_id_methods:
        hashed=0
        third_party=0
        print(file,method)
        if method=="":
            continue
        if methodHash[method]==1:
            hashed=1
        try:
            arr=method.split(';')
            lib_method=arr[0]
        except:
            continue
        for w in tp_words:
            if w in lib_method:
                third_party=1
                break

        #print("method: ", method)
        if third_party==1:
            #print("third Party found")

            if method in IMEI_id_methods:
                if hashed==1:
                    im_hash_tp+=1
                else:
                    im_raw_tp+=1

            if method in IMSI_id_methods:
                if hashed==1:
                    ims_hash_tp+=1
                else:
                    ims_raw_tp+=1
            if method in android_id_methods:
                if hashed==1:
                    aid_hash_tp+=1
                else:
                    aid_raw_tp+=1

            if method in mac_id_methods:
                if hashed==1:
                    mac_hash_tp+=1
                else:
                    mac_raw_tp+=1

            if method in serial_id_methods:

                if hashed==1:
                    sid_hash_tp+=1
                else:
                    sid_raw_tp+=1
            if method in ad_id_methods:
                adid_tp+=1

            if method in Guid_id_methods:
                guid_tp+=1

        else:
            if method in IMEI_id_methods:
                if hashed == 1:
                    im_hash_o += 1
                else:
                    im_raw_o += 1

            if method in IMSI_id_methods:
                if hashed == 1:
                    ims_hash_o += 1
                else:
                    ims_raw_o += 1
            if method in android_id_methods:
                if hashed == 1:
                    aid_hash_o += 1
                else:
                    aid_raw_o += 1

            if method in mac_id_methods:
                if hashed == 1:
                    mac_hash_o += 1
                else:
                    mac_raw_o += 1

            if method in serial_id_methods:

                if hashed == 1:
                    sid_hash_o += 1
                else:
                    sid_raw_o += 1
            if method in ad_id_methods:
                adid_o += 1

            if method in Guid_id_methods:
                guid_o += 1


    fw.write(str(file)  + ',' +str(im_hash_tp)+','+ str(im_raw_tp) + ',' +str(im_hash_o)+','+ str(im_raw_o) + ',' + str(
        ims_hash_tp) + ','+str(ims_raw_tp)+ ',' + str(
        ims_hash_o) + ','+str(ims_raw_o)+','+  str(aid_hash_tp) + ','+str(aid_raw_tp)+','+  str(aid_hash_o) + ','+str(aid_raw_o)+','+  str(sid_hash_tp) + ','+str(sid_raw_tp)+','+  str(sid_hash_o) + ','+str(sid_raw_o)+ ','+ str(mac_hash_tp)+ ','+str(mac_raw_tp)+ ','+ str(mac_hash_o)+ ','+str(mac_raw_o)+ ',' + str(adid_tp)+ ',' + str(adid_o)  + ',' + str(guid_tp)+ ',' + str(guid_o))
    fw.write('\n')
    count+=1
    print("written file: ",file,count)
