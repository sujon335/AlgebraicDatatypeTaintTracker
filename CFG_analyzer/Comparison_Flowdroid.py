import csv

fw=open('Flowdroid_comparison_with_amandroid_result.csv','w+')
# fw.write('Appname'+','+'FirstOrderID'+','+'SecondOrderID'+','+'IDs'+','+'ThirdParty'+','+'Own')
# fw.write('\n')

fw.write('App'+','+'IMEI(FP)'+','+'IMEI(FN)'+','+'IMSI(FP)'+','+'IMSI(FN)'+','+'AndroidID(FP)'+','+'AndroidID(FN)'+','+'SerialNo(FP)'+','+'SerialNo(FN)'+','+'MacAddress(FP)'+','+'MacAddress(FN)'+','+'ADvID(FP)'+','+'ADvID(FN)'+','+'GUID(FP)'+','+'GUID(FN)')
fw.write('\n')
c = 0
with open('Flowdroid_result_top_apps.csv',encoding="utf8", errors='ignore') as f:
    csvreader = csv.reader(f,delimiter=',')

    for row in csvreader:
        if c == 0:
            c+=1
            continue
        fapp=str(row[0]).strip()
        fapp=fapp.replace('_taint_result','')
        fimei=1
        fimsi=1
        faid=1
        fsid=1
        fmac=1
        fadid=1
        fguid=1
        if(str(row[2]).strip()=="0"):
            fimei=0
        if(str(row[3]).strip()=="0"):
            fimsi=0
        if(str(row[4]).strip()=="0"):
            faid=0
        if(str(row[5]).strip()=="0"):
            fsid=0
        if(str(row[6]).strip()=="0"):
            fmac=0
        if(str(row[7]).strip()=="0"):
            fadid=0
        if(str(row[8]).strip()=="0"):
            fguid=0

        imei = 1
        imsi = 1
        aid = 1
        sid = 1
        mac = 1
        adid = 1
        guid = 1
        found=0
        with open('Amandroid_taint_result_top_apps.csv', encoding="utf8", errors='ignore') as ff:
            csvreader2 = csv.reader(ff, delimiter=',')
            for row2 in csvreader2:
                app=str(row2[0]).strip()
                if (app!=fapp):
                    continue
                else:
                    print("app:", app, " fapp:", fapp)
                    if  (str(row2[2]).strip()=="0"):
                        imei=0
                    if(str(row2[3]).strip()=="0"):
                        imsi=0
                    if(str(row2[4]).strip()=="0") :
                        aid=0
                    if(str(row2[5]).strip()=="0") :
                        sid=0
                    if(str(row2[6]).strip()=="0") :
                        mac=0
                    if(str(row2[7]).strip()=="0"):
                        adid=0
                    if(str(row2[8]).strip()=="0"):
                        guid=0

                    found=1
                    break


        if found==0:
            print(fapp, " not found")
            continue
        imeifp=0
        imeifn=0
        imsifp=0
        imsifn=0
        aidfp=0
        aidfn=0
        sidfp=0
        sidfn=0
        macfp=0
        macfn=0
        adidfp=0
        adidfn=0
        guidfp=0
        guidfn=0

        if fimei==1 and imei==0:
            imeifp=1
        if fimei==0 and imei==1:
            imeifn=1

        if fimsi==1 and imsi==0:
            imsifp=1
        if fimsi==0 and imsi==1:
            imsifn=1

        if faid==1 and aid==0:
            aidfp=1
        if faid==0 and aid==1:
            aidfn=1

        if fsid==1 and sid==0:
            sidfp=1
        if fsid==0 and sid==1:
            sidfn=1

        if fmac==1 and mac==0:
            macfp=1
        if fmac==0 and mac==1:
            macfn=1

        if fadid==1 and adid==0:
            adidfp=1
        if fadid==0 and adid==1:
            adidfn=1

        if fguid == 1 and guid == 0:
            guidfp = 1
        if fguid == 0 and guid == 1:
            guidfn = 1


        fw.write(str(fapp)  + ',' +str(imeifp)+','+ str(imeifn) + ',' + str(
            imsifp) + ','+str(imsifn)+','+  str(aidfp) + ','+str(aidfn)+','+  str(sidfp) + ','+str(sidfn)+ ','+ str(macfp)+ ','+str(macfn)+ ',' + str(adidfp) + ',' + str(adidfn)+ ',' + str(guidfp)+ ',' + str(guidfn))
        fw.write('\n')

