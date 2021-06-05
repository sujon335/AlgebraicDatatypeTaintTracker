import sys
import re
import os
import csv
path = sys.argv[1]
cwd = os.getcwd()

## read path
fin = open(cwd + "/" + path)
##path name
#head, tail = os.path.split(path)

head = path.replace(".txt", "")
fout = open(cwd + "/table.csv", "a")

foutline = open(cwd + "/codeline.txt", "a")
apkname = [head]
package =[]

flag11 = []
flag12 = []
flag13 = []
flag14 = []
flag15 = []
flag16 = []
flag17 = []
flag18 = []

flag21 = []
flag22 = []
flag23 = []
flag24 = []
flag25 = []
flag26 = []
flag27 = []
flag28 = []

'''
obfuscationlist = []

fnotdomains = open(cwd + "/" + "notdomains.txt")
for line in fnotdomains:
    line = line.rstrip("\n")
    obfuscationlist.append(str(line))
fnotdomains.close()
'''

def booleanobfuscate(l):
    #for i in range(0, len(obfuscationlist)):
    #    if l in obfuscationlist[i]:
    #        print(l, obfuscationlist[i])
    #        return True
    if "/" in l:
        if len(l.strip().split("/")[0]) == 1:
            return True
        else:
            return False
    else:
        return True

fpackagename = open(cwd + "/" + head + "/" + "AndroidManifest.xml")

for line in fpackagename:
    if "package=" in line:
        packagename = str(line.strip().split("package=")[1]).strip().split(" ")[0]
        packagename = packagename.replace("\"","")
        packagename = packagename.replace(">","")
        packagename = str(packagename)
fpackagename.close()

for line in fin:
    line = line.rstrip("\n")
    smalifile = open(cwd + "/" + line)  
    
    owncode = False
    for codeline in smalifile:
        
        if codeline.strip().split(" ")[0] == ".class":
            p1 = packagename.strip().split(".")[0]
            p2 = packagename.strip().split(".")[1]
            name = str(codeline.strip().split(" ")[-1])
            name = name.strip().split(";")[0]
            name = str(name)
            name1 = name.strip().split("L")[1]
            name = name1.replace("/", ".")

            p = p1 + "." + p2
            if p in name:
                owncode = True

        if booleanobfuscate(name1) == True:
            
            break

        if owncode == True:

            if "landroid/telephony/telephonymanager;->getdeviceid()" in codeline.lower() or "landroid/telephony/telephonymanager;->getmeid()" in codeline.lower() or "landroid/telephony/telephonymanager;->getimei()" in codeline.lower():
                flag11.append(packagename)
            elif "getmeid(" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-virtual":
                flag11.append(packagename)
            elif "getmeid(" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-static":
                flag11.append(packagename)
            elif "getimei(" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-virtual":
                flag11.append(packagename)
            elif "getimei(" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-static":
                flag11.append(packagename)

            if "landroid/telephony/telephonymanager;->getsubscriberid()" in codeline.lower():
                flag12.append(packagename)
            
            if "getmacaddress(" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-virtual":
                flag13.append(packagename)
            elif "getmacaddress(" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-static":
                flag13.append(packagename)

            if "landroid/os/build;->serial" in codeline.lower() or "landroid/os/build;->getserial": 
                flag14.append(packagename)

            if "landroid/provider/settings$secure;->getstring(landroid/content/contentresolver;Ljava/lang/String;)" in codeline.lower():
                flag15.append(packagename)
            elif "android_id" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-virtual":
                flag15.append(packagename)
            elif "android_id" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-static":
                flag15.append(packagename)
            elif "android_id" in codeline.lower() and codeline.strip().split(" ")[0] == "const-string":
                flag15.append(packagename)

            if "lcom/google/android/gms/iid/instanceid;->getinstance()" in codeline.lower() or "lcom/google/firebase/iid/firebaseinstanceid;->getinstance()" in codeline.lower():
                flag16.append(packagename)

            if "ljava/util/uuid;->randomuuid()ljava/util/uuid" in codeline.lower():
                flag17.append(packagename)

            if "getadvertisingidinfo(" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-static":
                flag18.append(packagename)
            elif "advertisingIdClient" in codeline.lower() and "getId(" in codeline.lower():
                flag18.append(packagename)
        else:
            if "landroid/telephony/telephonymanager;->getdeviceid()" in codeline.lower() or "landroid/telephony/telephonymanager;->getmeid()" in codeline.lower() or "landroid/telephony/telephonymanager;->getimei()" in codeline.lower():
                
                flag21.append(name)   
            elif "getmeid(" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-virtual":
                flag21.append(name)               
            elif "getmeid(" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-static":
                flag21.append(name)               
            elif "getimei(" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-virtual":
                flag21.append(name)                
            elif "getimei(" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-static":
                flag21.append(name)
                
            if "landroid/telephony/telephonymanager;->getsubscriberid()" in codeline.lower():
                flag22.append(name)                
            
            if "getmacaddress(" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-virtual":
                flag23.append(name)                
            elif "getmacaddress(" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-static":
                flag23.append(name)                

            if "landroid/os/build;->serial" in codeline.lower() or "landroid/os/build;->getserial" in codeline.lower(): 
                flag24.append(name)
                
            if "landroid/provider/settings$secure;->getstring(landroid/content/contentresolver;Ljava/lang/String;)" in codeline.lower():
                flag25.append(name)            
            elif "android_id" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-virtual":
                flag25.append(name)               
            elif "android_id" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-static":
                flag25.append(name)
            elif "android_id" in codeline.lower() and codeline.strip().split(" ")[0] == "const-string":
                flag25.append(name)          

            if "lcom/google/android/gms/iid/instanceid;->getinstance()" in codeline.lower() or "lcom/google/firebase/iid/firebaseinstanceid;->getinstance()" in codeline.lower():
                flag26.append(name)

            if "ljava/util/uuid;->randomuuid()ljava/util/uuid" in codeline.lower():
                flag27.append(name)               

            if "getadvertisingidinfo(" in codeline.lower() and codeline.strip().split(" ")[0] == "invoke-static":
                flag28.append(name)                
            elif "advertisingIdClient" in codeline.lower() and "getId(" in codeline.lower():
                flag28.append(name)
     
    smalifile.close()
foutline.close()
fin.close()

flag11 = list(set(flag11))
flag11.sort()
flag12 = list(set(flag12))
flag12.sort()
flag13 = list(set(flag13))
flag13.sort()
flag14 = list(set(flag14))
flag14.sort()
flag15 = list(set(flag15))
flag15.sort()
flag16 = list(set(flag16))
flag16.sort()
flag17 = list(set(flag17))
flag17.sort()
flag18 = list(set(flag18))
flag18.sort()

flag21 = list(set(flag21))
flag21.sort()
flag22 = list(set(flag22))
flag22.sort()
flag23 = list(set(flag23))
flag23.sort()
flag24 = list(set(flag24))
flag24.sort()
flag25 = list(set(flag25))
flag25.sort()
flag26 = list(set(flag26))
flag26.sort()
flag27 = list(set(flag27))
flag27.sort()
flag28 = list(set(flag28))
flag28.sort()

def get_first(l):
    if l: 
        return l[0]
    else:
        return ""

def remove_first(l):
    if l:
        del l[0]
    return l

def get_length(l):
    if l == [] or l == None:
        return 0
    else:
        return(len(l))

#with open(cwd + "/packagename.csv", 'a',newline='') as mypackage:
#    wr = csv.writer(mypackage,  delimiter=',')
#    wr.writerow(packagename)

#mypackage.close()

l = max(get_length(flag11), get_length(flag12), get_length(flag13), get_length(flag14), get_length(flag15), get_length(flag16), get_length(flag17), get_length(flag18), get_length(flag21), get_length(flag22), get_length(flag23), get_length(flag24), get_length(flag25), get_length(flag26), get_length(flag27), get_length(flag28))

with open(cwd + "/table_newest.csv", 'a', newline='') as myfile:
    wr = csv.writer(myfile, delimiter=',')
    
    for i in range(0, l):
        package = []
        if i == 0:
            package.append(head)
        else:
            package.append("")

        package.append(get_first(flag11))
        flag11 = remove_first(flag11)
        package.append(get_first(flag21))
        flag21 = remove_first(flag21)
        package.append(get_first(flag12))
        flag12 = remove_first(flag12)
        package.append(get_first(flag22))
        flag22 = remove_first(flag22)
        package.append(get_first(flag13))
        flag13 = remove_first(flag13)
        package.append(get_first(flag23))
        flag23 = remove_first(flag23)
        package.append(get_first(flag14))
        flag14 = remove_first(flag14)
        package.append(get_first(flag24))
        flag24 = remove_first(flag24)
        package.append(get_first(flag15))
        flag15 = remove_first(flag15)
        package.append(get_first(flag25))
        flag25 = remove_first(flag25)
        package.append(get_first(flag16))
        flag16 = remove_first(flag16)
        package.append(get_first(flag26))
        flag26 = remove_first(flag26)
        package.append(get_first(flag17))
        flag17 = remove_first(flag17)
        package.append(get_first(flag27))
        flag27 = remove_first(flag27)
        package.append(get_first(flag18))
        flag18 = remove_first(flag18)
        package.append(get_first(flag28))
        flag28 = remove_first(flag28)

        wr.writerow(package)

myfile.close()