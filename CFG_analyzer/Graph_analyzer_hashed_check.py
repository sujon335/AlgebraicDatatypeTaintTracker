import sys

import csv

fw=open('App_ID_stats4.csv','w+')
# fw.write('Appname'+','+'FirstOrderID'+','+'SecondOrderID'+','+'IDs'+','+'ThirdParty'+','+'Own')
# fw.write('\n')

fw.write('Appname'+','+'FirstOrderID'+','+'SecondOrderID'+','+'IMEI'+','+'IMSI'+','+'AndroidID'+','+'SerialNo'+','+'MacAddress'+','+'ADvID'+','+'GUID'+','+'ThirdParty'+','+'Own')
fw.write('\n')

ff = open('TopAppsName.txt','r')

Apps = []

for line in ff:
	line = line.strip('\n')
	Apps.append(line)

fff = open('thirdPartyWords.txt','r')

tp_words = []

for line in fff:
	line = line.strip('\n')
	tp_words.append(line)

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
            #print(arr)
            if(len(arr)>1):
                arr2=arr[1].split('@')
                sub_method=arr2[0].strip()
                #print(sub_method)
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

# def method_slice_hash(alllines,num):
#     global outfile
#     lines=""
#     while(num<len(alllines)):
#         line=alllines[num-1].strip()
#         lines+=line+" "
#         # outfile.write(line)
#         # outfile.write('\n')
#         if line=="})" or line=="}})" or line=="}}})":
#             break
#         num=num+1
#     if "hashCode" in lines:
#         return 1
#     if "MessageDigest" in lines:
#         return 1
#     if "nameUUIDFromBytes" in lines:
#         return 1
#     if "md5" in lines:
#         return 1
#     return 0


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
                        methodHash[methodname]=hash
    except:
        print("nofile")
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
                        methodHash[methodname]=hash
    except:
        print("nofile")
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



schemes={}
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
    im = len(IMEI_id_methods)
    ims = len(IMSI_id_methods)
    aid = len(android_id_methods)
    mid = len(mac_id_methods)
    sid = len(serial_id_methods)
    adid = len(ad_id_methods)
    guid = len(Guid_id_methods)
    first_order_id_count=len(IMEI_id_methods)+len(IMSI_id_methods)+len(android_id_methods)+len(mac_id_methods)+len(serial_id_methods)+len(ad_id_methods)+len(Guid_id_methods)
    own_package_count=0
    third_party_count=0
    second_order_id_count=0
    third_party_count+=process_id_methods(IMEI_id_methods,file,1)
    third_party_count+=process_id_methods(IMSI_id_methods, file, 2)
    third_party_count+=process_id_methods(android_id_methods, file, 3)
    third_party_count+=process_id_methods(mac_id_methods, file, 4)
    third_party_count+=process_id_methods(serial_id_methods, file, 5)
    third_party_count+=process_id_methods(ad_id_methods, file, 6)
    third_party_count+=process_id_methods(Guid_id_methods, file, 7)
    own_package_count=first_order_id_count-third_party_count

    all_id_methods=IMEI_id_methods+IMSI_id_methods+android_id_methods+ad_id_methods+serial_id_methods+Guid_id_methods+mac_id_methods
    Ids=""
    combinedIDs=[]
    for method in all_id_methods:
        if method=="":
            continue
        c=0
        if method in IMEI_id_methods:
            Ids+="IMEI + "
            c+=1
        if method in IMSI_id_methods:
            Ids+="IMSI + "
            c+=1
        if method in android_id_methods:
            Ids+="AndroidID + "
            c+=1
        if method in mac_id_methods:
            Ids+="Mac + "
            c+=1
        if method in serial_id_methods:
            Ids+="SERIAL + "
            c+=1
        if method in ad_id_methods:
            Ids+="AdvertisingID + "
            c+=1
        if method in Guid_id_methods:
            Ids+="GUID + "
            c+=1

        if (c>1):
            combinedIDs.append(Ids)
            if (methodHash[method] == 0):
                if Ids not in schemes:
                    schemes[Ids] = 0
            else:
                if Ids in schemes:
                    val = schemes[Ids]
                    schemes[Ids] = val + 1
                    print(Ids + "has # " + str(val+1) + " hashes now")
                else:
                    schemes[Ids] = 1
                print(" File : "+ file + " method: "+ method+" is hashed ")

        Ids=""

    combinedIDs = list( dict.fromkeys(combinedIDs) )
    second_order_id_count = len(combinedIDs)
    for sch in combinedIDs:
        im = 0
        ims = 0
        aid = 0
        sid = 0
        mid = 0
        adid = 0
        guid = 0
        if "IMEI" in sch:
            im=1
            first_order_id_count-=1
        if "IMSI" in sch:
            ims=1
            first_order_id_count -= 1
        if "AndroidID" in sch:
            aid=1
            first_order_id_count -= 1
        if "Mac" in sch:
            mid=1
            first_order_id_count -= 1
        if "SERIAL" in sch:
            sid=1
            first_order_id_count -= 1
        if "AdvertisingID" in sch:
            adid=1
            first_order_id_count -= 1
        if "GUID" in sch:
            guid=1
            first_order_id_count -= 1

        fw.write(str(file) + ',' + str(first_order_id_count) + ',' + str(second_order_id_count) + ',' +str(im)+','+str(ims)+','+str(aid)+','+str(sid)+','+str(mid)+','+str(adid)+','+str(guid)+',' + str(third_party_count) + ',' + str(own_package_count))
        fw.write('\n')
    if(second_order_id_count==0):
        fw.write(str(file) + ',' + str(first_order_id_count) + ',' + str(second_order_id_count) + ',' +str(im)+','+str(ims)+','+str(aid)+','+str(sid)+','+str(mid)+','+str(adid)+','+str(guid)+',' + str(third_party_count) + ',' + str(own_package_count))
        fw.write('\n')
    #print(str(file) + ',' + str(first_order_id_count) + ',' + str(second_order_id_count)+','+ str(combinedIDs)+',' +str(third_party_count)+','+ str(own_package_count))
    # fw.write(str(file) + ',' + str(first_order_id_count) + ',' + str(second_order_id_count)+','+ str(combinedIDs).replace(',','#')+',' +str(third_party_count)+','+ str(own_package_count))
    # fw.write('\n')

for key in schemes:
    arr=str(key).split('+')
    schemes[key]=schemes[key]/ (len(arr)-1)

schemes=sorted(schemes.items(), key=lambda x: x[1], reverse=True)


for scheme in schemes:
    print(str(scheme))

