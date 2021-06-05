import sys

infile=sys.argv[1]
#infile='graph_ML_CleanJuice.txt'
outfilename=sys.argv[2]
outfile=open(outfilename,'w+')

### SERIAL --- android.os.Build.SERIAL
### IMEI   --- Landroid/telephony/TelephonyManager;.getDeviceId:()Ljava/lang/String;
##  IMSI   --- Landroid/telephony/TelephonyManager;.getSimSerialNumber:()Ljava/lang/String;
## Advertising ID -- Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;.getAdvertisingIdInfo:(Landroid/content/Context;
### AndroidID --- Landroid/content/Context;.getContentResolver
## Random UUID -- Ljava/util/UUID;.randomUUID:()Ljava/util/UUID;
### MacAddress --- Landroid/net/wifi/WifiInfo;.getMacAddress:()Ljava/lang/String;
IMEI="Landroid/telephony/TelephonyManager;.getDeviceId:()Ljava/lang/String;"
AndroidID="Landroid/content/Context;.getContentResolver"
SERIAL="android.os.Build.SERIAL"
IMSI="Landroid/telephony/TelephonyManager;.getSimSerialNumber:()Ljava/lang/String;"
MacAddress="Landroid/net/wifi/WifiInfo;.getMacAddress:()Ljava/lang/String;"
AdvertisingID="Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;"
#UUID="Ljava/util/UUID;.randomUUID:()Ljava/util/UUID;"

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

def print_method_slice(alllines,num):
    global outfile

    while(num<len(alllines)):
        line=alllines[num-1].strip()
        print(line)
        # outfile.write(line)
        # outfile.write('\n')
        if line=="})" or line=="}})" or line=="}}})":
            break
        num=num+1


def find_methods(search_text,filename):
    global printed_methods
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
                    # outfile.write('\n')
                    # outfile.write('\n')
                    # outfile.write("Method: " + methodname)
                    # outfile.write('\n')
                    print_method_slice(all_lines, method_start_line)
    return id_methods

def find_AndroidID_methods(search_text,filename):
    global printed_methods
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
                    # outfile.write('\n')
                    # outfile.write('\n')
                    # outfile.write("Method: " + methodname)
                    # outfile.write('\n')
                    print_method_slice(all_lines, method_start_line)
    return id_methods

def search_method(search_text,filename):
    global trace
    global Foundlines
    global graph
    trace = trace+ search_text +" ----->  [ "
    with open(filename) as File:
        file_variable = open(filename)
        all_lines = file_variable.readlines()
        text_calling_methods=[]
        for num, line in enumerate(File, 1):
            if search_text in line:
                print('Found text at line: ', num)
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
                    printed_methods.append(methodname)
                    print("Method: ",methodname)
                    # outfile.write('\n')
                    # outfile.write('\n')
                    # outfile.write("Method: "+ methodname)
                    # outfile.write('\n')
                    trace = trace + methodname + "   "
                    print_method_slice(all_lines,method_start_line)
                    Foundlines.append(method_start_line)
                    Foundlines.append(method_start_line+1)
        graph[search_text] = text_calling_methods
        cou=0
        if (len (Foundlines)<10):
            for method in text_calling_methods:
                if method[-1] == 'V' or method[-1] == 'Z' or method[-1] == 'I':
                    continue
                print("tracing method....:",methodname)

                search_method(method,filename)
                cou=+1
                if (cou > 3):
                    break


printed_methods=[]
Foundlines=[]
graph={}
graph["IMEI"]=find_methods(IMEI,infile)
graph["IMSI"]=find_methods(IMSI,infile)
graph["AndroidID"]=find_AndroidID_methods(AndroidID,infile)
graph["SERIAL"]=find_methods(SERIAL,infile)
graph["MacAddress"]=find_methods(MacAddress,infile)
graph["AdvertisingID"]=find_methods(AdvertisingID,infile)
#graph["UUID"]=find_methods(UUID,infile)
id_methods=find_methods(IMEI,infile)
id_methods=id_methods + list(set(find_methods(IMSI,infile)) - set(id_methods))
id_methods=id_methods + list(set(find_AndroidID_methods(AndroidID,infile)) - set(id_methods))
id_methods=id_methods + list(set(find_methods(SERIAL,infile)) - set(id_methods))
id_methods=id_methods + list(set(find_methods(AdvertisingID,infile)) - set(id_methods))
id_methods=id_methods + list(set(find_methods(MacAddress,infile)) - set(id_methods))
#id_methods=id_methods + list(set(find_methods(UUID,infile)) - set(id_methods))
trace=""
for idmethod in id_methods:
    Foundlines=[]
    trace+=idmethod
    if idmethod[-1]=='V'or idmethod[-1] == 'Z' or idmethod[-1] == 'I':
        continue
    search_method(idmethod,infile)
    # outfile.write('\n')
    # outfile.write('\n')
    # outfile.write(trace)
    # outfile.write('\n')
    # outfile.write('\n')
    # outfile.write('\n')


print('\n')
print(".........Graph................")
for key in graph:
    print(key+ " ----> " + str(graph[key]))
    print('\n')
    outfile.write(key+ " ----> " + str(graph[key]))
    outfile.write('\n')
    outfile.write('\n')
