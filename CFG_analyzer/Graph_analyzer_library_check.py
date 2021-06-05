import sys

import csv

fw=open('library_stats_4.csv','w+')
# fw.write('Appname'+','+'FirstOrderID'+','+'SecondOrderID'+','+'IDs'+','+'ThirdParty'+','+'Own')
# fw.write('\n')

fw.write('Library'+','+'LibraryMethods'+','+'IMEIHashed'+','+'IMEIRaw'+','+'IMSIHashed'+','+'IMSIRaw'+','+'AndroidIDHashed'+','+'AndroidIDRaw'+','+'SerialNoHashed'+','+'SerialNoRaw'+','+'MacAddressHashed'+','+'MacAddressRaw'+','+'ADvID'+','+'GUID')
fw.write('\n')

ff = open('TopAppsName.txt','r')
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
    IMEI_id_methods=find_methods(IMEI,"TopFreeApps/"+file)
    IMSI_id_methods=find_methods(IMSI,"TopFreeApps/"+file)
    android_id_methods=find_AndroidID_methods(AndroidID,"TopFreeApps/"+file)
    mac_id_methods = find_methods(MacAddress, "TopFreeApps/" + file)
    serial_id_methods = find_methods(SERIAL, "TopFreeApps/" + file)
    ad_id_methods = find_methods(AdvertisingID, "TopFreeApps/" + file)
    Guid_id_methods = find_methods(UUID, "TopFreeApps/" + file)


    all_id_methods=IMEI_id_methods+IMSI_id_methods+android_id_methods+ad_id_methods+serial_id_methods+Guid_id_methods+mac_id_methods

    all_id_methods = list(dict.fromkeys(all_id_methods))
    for method in all_id_methods:
        print(file,method)
        if method=="":
            continue
        if method in libraries_apps_count:
            libraries_apps_count[method] = libraries_apps_count[method] +1
        else:
            libraries_apps_count[method]=1

        if method not in libraries_hash:
            if (methodHash[method] == 0):
                libraries_hash[method] = 0
            else:
                libraries_hash[method] = 1

        if method in IMEI_id_methods:
            if method in libraries_imei:
                libraries_imei[method] = libraries_imei[method] + 1
            else:
                libraries_imei[method] = 1
        else:
            libraries_imei[method]=0
        if method in IMSI_id_methods:
            if method in libraries_imsi:
                libraries_imsi[method] = libraries_imsi[method] + 1
            else:
                libraries_imsi[method] = 1
        else:
            libraries_imsi[method]=0
        if method in android_id_methods:
            if method in libraries_aid:
                libraries_aid[method] = libraries_aid[method] + 1
            else:
                libraries_aid[method] = 1
        else:
            libraries_aid[method]=0
        if method in mac_id_methods:
            if method in libraries_mac:
                libraries_mac[method] = libraries_mac[method] + 1
            else:
                libraries_mac[method] = 1
        else:
            libraries_mac[method]=0
        if method in serial_id_methods:
            if method in libraries_serial:
                libraries_serial[method] = libraries_serial[method] + 1
            else:
                libraries_serial[method] = 1
        else:
            libraries_serial[method]=0
        if method in ad_id_methods:
            if method in libraries_adid:
                libraries_adid[method] = libraries_adid[method] + 1
            else:
                libraries_adid[method] = 1
        else:
            libraries_adid[method]=0
        if method in Guid_id_methods:
            if method in libraries_guid:
                libraries_guid[method] = libraries_guid[method] + 1
            else:
                libraries_guid[method] = 1
        else:
            libraries_guid[method]=0


library_common_methods={}
libraries_common_imei_raw={}
libraries_common_imei_hashed={}
libraries_common_imsi_raw={}
libraries_common_imsi_hashed={}
libraries_common_androidid_raw={}
libraries_common_androidid_hashed={}
libraries_common_serial_raw={}
libraries_common_serial_hashed={}
libraries_common_mac_raw={}
libraries_common_mac_hashed={}
libraries_common_adid={}
libraries_common_guid={}
for method in libraries_apps_count:
    apps_count = libraries_apps_count[method]
    hash=libraries_hash[method]
    im = libraries_imei[method]
    ims = libraries_imsi[method]
    aid = libraries_aid[method]
    sid = libraries_serial[method]
    mid =libraries_mac[method]
    adid = libraries_adid[method]
    guid = libraries_guid[method]
    try:

        #arr1=str(method).split(';')
        arr=str(method).split('/')
        method_common_name =arr[0]+'/'+arr[1]
    except:
        continue
    if method_common_name in library_common_methods:
        if hash==0:
            libraries_common_imei_raw[method_common_name]=libraries_common_imei_raw[method_common_name]+im
            libraries_common_imsi_raw[method_common_name]=libraries_common_imsi_raw[method_common_name]+ims
            libraries_common_androidid_raw[method_common_name] = libraries_common_androidid_raw[method_common_name] + aid
            libraries_common_serial_raw[method_common_name] = libraries_common_serial_raw[method_common_name] + sid
            libraries_common_mac_raw[method_common_name] = libraries_common_mac_raw[method_common_name] + mid
        else:
            libraries_common_imei_hashed[method_common_name]=libraries_common_imei_hashed[method_common_name]+im
            libraries_common_imsi_hashed[method_common_name]=libraries_common_imsi_hashed[method_common_name]+ims
            libraries_common_androidid_hashed[method_common_name] = libraries_common_androidid_hashed[method_common_name] + aid
            libraries_common_serial_hashed[method_common_name] = libraries_common_serial_hashed[method_common_name] + sid
            libraries_common_mac_hashed[method_common_name] = libraries_common_mac_hashed[method_common_name] + mid

        library_common_methods[method_common_name] = library_common_methods[method_common_name]+1
        libraries_common_adid[method_common_name] = libraries_common_adid[method_common_name] + adid
        libraries_common_guid[method_common_name] = libraries_common_guid[method_common_name] + guid


    else:
        if hash==0:
            libraries_common_imei_raw[method_common_name]=im
            libraries_common_imsi_raw[method_common_name]=ims
            libraries_common_androidid_raw[method_common_name] = aid
            libraries_common_serial_raw[method_common_name] =  sid
            libraries_common_mac_raw[method_common_name] =  mid

            libraries_common_imei_hashed[method_common_name]=0
            libraries_common_imsi_hashed[method_common_name]=0
            libraries_common_androidid_hashed[method_common_name] = 0
            libraries_common_serial_hashed[method_common_name] = 0
            libraries_common_mac_hashed[method_common_name] =  0

        else:
            libraries_common_imei_hashed[method_common_name]=im
            libraries_common_imsi_hashed[method_common_name]=ims
            libraries_common_androidid_hashed[method_common_name] = aid
            libraries_common_serial_hashed[method_common_name] = sid
            libraries_common_mac_hashed[method_common_name] =  mid

            libraries_common_imei_raw[method_common_name]=0
            libraries_common_imsi_raw[method_common_name]=0
            libraries_common_androidid_raw[method_common_name] = 0
            libraries_common_serial_raw[method_common_name] =  0
            libraries_common_mac_raw[method_common_name] =  0


        library_common_methods[method_common_name] = 1
        libraries_common_adid[method_common_name] = adid
        libraries_common_guid[method_common_name] = guid




for method in library_common_methods:
    method_count = library_common_methods[method]
    im_raw= libraries_common_imei_raw[method]
    im_hash=libraries_common_imei_hashed[method]
    ims_raw= libraries_common_imsi_raw[method]
    ims_hash=libraries_common_imsi_hashed[method]
    aid_raw= libraries_common_androidid_raw[method]
    aid_hash=libraries_common_androidid_hashed[method]
    sid_raw= libraries_common_serial_raw[method]
    sid_hash=libraries_common_serial_hashed[method]
    mac_raw= libraries_common_mac_raw[method]
    mac_hash=libraries_common_mac_hashed[method]


    adid = libraries_common_adid[method]
    guid = libraries_common_guid[method]

    fw.write(str(method) + ',' + str(method_count) + ',' +str(im_hash)+','+ str(im_raw) + ',' + str(
        ims_hash) + ','+str(ims_raw)+','+  str(aid_hash) + ','+str(aid_raw)+','+  str(sid_hash) + ','+str(sid_raw)+ ','+ str(mac_hash)+ ','+str(mac_raw)+ ',' + str(adid) + ',' + str(guid))
    fw.write('\n')


# for method in libraries_apps_count:
#     apps_count = libraries_apps_count[method]
#     hash=libraries_hash[method]
#     im = libraries_imei[method]
#     ims = libraries_imsi[method]
#     aid = libraries_aid[method]
#     sid = libraries_serial[method]
#     mid =libraries_mac[method]
#     adid = libraries_adid[method]
#     guid = libraries_guid[method]
#
#     fw.write(str(method) + ',' + str(apps_count) + ',' +str(hash)+','+ str(im) + ',' + str(
#         ims) + ',' + str(aid) + ',' + str(sid) + ',' + str(mid) + ',' + str(adid) + ',' + str(guid))
#     fw.write('\n')

