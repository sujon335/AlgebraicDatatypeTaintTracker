import sys
from sys import argv
import os
import csv

# fw=open('app_wise_thirdparty_stats.csv','w+')
# # fw.write('Appname'+','+'FirstOrderID'+','+'SecondOrderID'+','+'IDs'+','+'ThirdParty'+','+'Own')
# # fw.write('\n')
#
# fw.write('App'+','+'IMEIHashed(TP)'+','+'IMEIRaw(TP)'+','+'IMEIHashed(O)'+','+'IMEIRaw(O)'+','+'IMSIHashed(TP)'+','+'IMSIRaw(TP)'+','+'IMSIHashed(O)'+','+'IMSIRaw(O)'+','+'AndroidIDHashed(TP)'+','+'AndroidIDRaw(TP)'+','+'AndroidIDHashed(O)'+','+'AndroidIDRaw(O)'+','+'SerialNoHashed(TP)'+','+'SerialNoRaw(TP)'+','+'MacAddressHashed(O)'+','+'MacAddressRaw(O)'+','+'ADvID(TP)'+','+'ADvID(O)'+','+'GUID(TP)'+','+'GUID(O)')
# fw.write('\n')

# ff = open('TopAppsName.txt','r')
#infile=sys.argv[1]
#ff = open(infile,'r')
try:
 path=argv[1]
except:
 print("please provide the generated CFG file name with extension")

isFile = os.path.isfile(path)

Apps = []

# for line in ff:
# 	line = line.strip('\n')
# 	Apps.append(line)

if(isFile):
 Apps.append(path)
else:
 print("CFG text file needed")

#Apps.append("com.dunkinbrands.otgo.txt")


fff = open('thirdPartyWords.txt','r')

tp_words = []

for line in fff:
	line = line.strip('\n')
	tp_words.append(line)

fff.close()
#print(tp_words)
ffff = open('sources.txt','r')

sources ={}

for line in ffff:
    line = line.strip('\n')
    arr=line.split(" ")
    if((len(arr)<2)):
        print("Source API and name must be defined with space seperation")
        exit(1)
    key=arr[1]
    api=arr[0]
    sources[key]=api

ffff.close()

ffff = open('sinks.txt','r')

sinks =[]
for line in ffff:
    line = line.strip('\n')
    sinks.append(line)

ffff.close()



# IMEI="Landroid/telephony/TelephonyManager;.getDeviceId:()Ljava/lang/String;"
# AndroidID="Landroid/content/Context;.getContentResolver"
# SERIAL="android.os.Build.SERIAL"
# IMSI="Landroid/telephony/TelephonyManager;.getSubscriberId():()Ljava/lang/String;"
# MacAddress="Landroid/net/wifi/WifiInfo;.getMacAddress:()Ljava/lang/String;"
# AdvertisingID="Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;"
# UUID="Ljava/util/UUID;.randomUUID:()Ljava/util/UUID;"




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
    if "SHA" in lines:
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
    if "SHA" in lines:
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
                    #print('line: ', num)
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
                    #print('line: ', num)
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


def search_method(search_text,filename,source):
    global id_methods
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

        if source in id_methods:
            val=id_methods[source]
            val+=text_calling_methods
            id_methods[source]=val
        else:
            id_methods[source]=text_calling_methods





def process_id_methods(idmethods,file,source):
    ims=idmethods
    for idmetho in ims:
        arr=idmetho.split('/')
        if idmetho[-1] == 'V' or idmetho[-1] == 'Z' or idmetho[-1] == 'I':
            continue
        if arr[0]=="`Ljava" or arr[0]=="`Landroid":
            continue
        search_method(idmetho,file,source)




methodHash={}
Foundlines = []
printed_methods = []
methods = {}
id_methods={}
all_id_methods=[]
own_package_count=0


def find_registers(lines):
    registers={}
    for i in range(0,len(lines)):
        cur_line=lines[i]
        for source in sources:
            if(source=="IMEI"):
                if(sources[source] in cur_line or "getTelephonyDeviceId" in cur_line):
                    next_line=lines[i+1]
                    arr1=next_line.split(":=")
                    left_side=arr1[0]
                    arr2=left_side.split(".")
                    right_side=arr2[1]
                    reg=right_side.strip()
                    registers["IMEI"]=reg
                    break
            if(source=="IMSI"):
                if(sources[source] in cur_line or "getSubscriberId()" in cur_line):
                    next_line=lines[i+1]
                    arr1=next_line.split(":=")
                    left_side=arr1[0]
                    arr2=left_side.split(".")
                    right_side=arr2[1]
                    reg=right_side.strip()
                    registers["IMSI"]=reg
                    break
            if(source=="AndroidID"):
                if(sources[source] in cur_line or "getAndroidId" in cur_line):
                    next_line=lines[i+1]
                    arr1=next_line.split(":=")
                    left_side=arr1[0]
                    arr2=left_side.split(".")
                    right_side=arr2[1]
                    reg=right_side.strip()
                    registers["AndroidID"]=reg
                    break
            if(source=="Mac"):
                if(sources[source] in cur_line or "getWifiMacAddress" in cur_line):
                    next_line=lines[i+1]
                    arr1=next_line.split(":=")
                    left_side=arr1[0]
                    arr2=left_side.split(".")
                    right_side=arr2[1]
                    reg=right_side.strip()
                    registers["Mac"]=reg
                    break
            if(sources[source] in cur_line):
                next_line=lines[i+1]
                arr1=next_line.split(":=")
                left_side=arr1[0]
                arr2=left_side.split(".")
                right_side=arr2[1]
                reg=right_side.strip()
                registers[source]=reg
                break

    return registers


def update_hashed_registers(lines, registers):
    hashed={}
    hashes=[]
    hashes.append("hashCode")
    hashes.append("MessageDigest")
    hashes.append("nameUUIDFromBytes")
    hashes.append("md5")
    hashes.append("digest")
    for i in range(0,len(lines)):
        cur_line=lines[i]
        for hash in hashes:
            if hash in cur_line:
                for key in registers:
                    val=registers[key]
                    if val in cur_line:
                        hashed[key]=1
                        next_line=lines[i+1]
                        arr1=next_line.split(":=")
                        left_side=arr1[0]
                        arr2=left_side.split(".")
                        right_side=arr2[1]
                        reg=right_side.strip()
                        registers[key]=reg
    return hashed,registers


def find_combineds(lines, registers):
    combineds={}
    combinations=[]
    combinations.append("Ljava/util/UUID")
    combinations.append("Ljava/lang/StringBuilder;.append")
    for i in range(0,len(lines)):
        cur_line=lines[i]
        for combination in combinations:
            if combination in cur_line:
                for key in registers:
                    val=registers[key]
                    if val in cur_line:
                        combineds[key]=1
    return combineds


def getSignatureMethod(method,file):
    filename=file
    lines=[]
    signature=""
    with open(filename) as File:
        file_variable = open(filename)
        all_lines = file_variable.readlines()
        for num, line in enumerate(File, 1):
            if method in line:
                methodname,method_start_line=find_the_method_slice(all_lines,num)
                if(methodname!=""):
                    break
        while(method_start_line<len(all_lines)):
            line=all_lines[method_start_line-1].strip()
            lines.append(line)

            if line=="})" or line=="}})" or line=="}}})":
                break
            method_start_line=method_start_line+1

    # if method=="Lio/intercom/android/sdk/commons/utilities/DeviceUtils;.generateDeviceId:(Landroid/content/Context;)Ljava/lang/String;":
    #     for line in lines:
    #         print(line)
    registers=find_registers(lines)
    hashed,registers=update_hashed_registers(lines,registers)

    combineds=find_combineds(lines,registers)
    combineds.pop('GUID', None)
    if(len(combineds)>1):
        signature+="("
        for key in combineds:
            if key in hashed:
                signature+=" h("+key+") ^"
            else:
                signature+=" "+key+" ^"
        signature=signature[:-1]
        signature+=")"

    for key in registers:
        if (len(combineds)>1):
            if key not in combineds:
                if key in hashed:
                    signature+="+ h("+key+") "
                else:
                    signature+=" + "+key+" "
        else:
            if key in hashed:
                signature+="+ h("+key+") "
            else:
                signature+=" + "+key+" "

    #print("Signatue:  ",signature)
    return signature


for file in Apps:

    for source in sources:
        if source=="AndroidID":
            id_methods[source]=find_AndroidID_methods(sources[source],file)
        else:
            id_methods[source]=find_methods(sources[source],file)

    for source in sources:
        process_id_methods(id_methods[source],file,source)

    for source in sources:
        for id_method in id_methods[source]:
            all_id_methods.append(id_method)


    all_id_methods = list(dict.fromkeys(all_id_methods))
    Ids=""
    schemes=[]
    #print("methods count: ",len(all_id_methods))
    for method in all_id_methods:
        hashed=0
        third_party=0
        #print("Method: ",method)
        if method=="":
            continue
        c=0
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

        for source in sources:
            source_methods=id_methods[source]
            if method in source_methods:
                c+=1
                if hashed==1 and "Adv" not in source and "GUID" not in source:
                    Ids+="h("+source+") + "
                else:
                    Ids+=source+" + "

        if (c>1):
            #print("method: ", method)
            Ids=getSignatureMethod(method,file)
            Ids=Ids.strip()
            if(Ids==""):
                continue
        if third_party==1:
            Ids+=" (Third Party Leak)"
        else:
            Ids+=" (Own Code Leak)"
        schemes.append(Ids)

        Ids=""
    schemes = list( dict.fromkeys(schemes) )

    base=os.path.basename(file)
    filename=os.path.splitext(base)[0]
    fw=open(filename+"_signature.txt",'w')
    print("..........Leaked signatures: ..............")
    for scheme in schemes:
        print(scheme)
        fw.write(scheme)
        fw.write('\n')
    fw.close()




    # fw.write(str(file)  + ',' +str(im_hash_tp)+','+ str(im_raw_tp) + ',' +str(im_hash_o)+','+ str(im_raw_o) + ',' + str(
    #     ims_hash_tp) + ','+str(ims_raw_tp)+ ',' + str(
    #     ims_hash_o) + ','+str(ims_raw_o)+','+  str(aid_hash_tp) + ','+str(aid_raw_tp)+','+  str(aid_hash_o) + ','+str(aid_raw_o)+','+  str(sid_hash_tp) + ','+str(sid_raw_tp)+','+  str(sid_hash_o) + ','+str(sid_raw_o)+ ','+ str(mac_hash_tp)+ ','+str(mac_raw_tp)+ ','+ str(mac_hash_o)+ ','+str(mac_raw_o)+ ',' + str(adid_tp)+ ',' + str(adid_o)  + ',' + str(guid_tp)+ ',' + str(guid_o))
    # fw.write('\n')

