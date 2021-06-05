import csv

# fw=open('Flowdroid_comparison_with_amandroid_result.csv','w+')
# # fw.write('Appname'+','+'FirstOrderID'+','+'SecondOrderID'+','+'IDs'+','+'ThirdParty'+','+'Own')
# # fw.write('\n')
#
# fw.write('App'+','+'IMEI(FP)'+','+'IMEI(FN)'+','+'IMSI(FP)'+','+'IMSI(FN)'+','+'AndroidID(FP)'+','+'AndroidID(FN)'+','+'SerialNo(FP)'+','+'SerialNo(FN)'+','+'MacAddress(FP)'+','+'MacAddress(FN)'+','+'ADvID(FP)'+','+'ADvID(FN)'+','+'GUID(FP)'+','+'GUID(FN)')
# fw.write('\n')
c = 0
fp=0
fn=0
tp=0
tn=0
app_count=0
with open('OurApproach_GT_app_wise_hash_stats.csv',encoding="utf8", errors='ignore') as f:
    csvreader = csv.reader(f,delimiter=',')

    for row in csvreader:
        if c == 0:
            c+=1
            continue
        fapp=str(row[0]).strip()
        fimei_h=1
        fimei_r = 1
        fimsi_h=1
        fimsi_r = 1
        faid_h=1
        faid_r=1
        fsid_h=1
        fsid_r=1
        fmac_h=1
        fmac_r=1
        fadid=1
        fguid=1
        if(str(row[1]).strip()=="0"):
            fimei_h=0
        if(str(row[2]).strip()=="0"):
            fimei_r=0
        if(str(row[3]).strip()=="0"):
            fimsi_h=0
        if(str(row[4]).strip()=="0"):
            fimsi_r=0
        if(str(row[5]).strip()=="0"):
            faid_h=0
        if(str(row[6]).strip()=="0"):
            faid_r=0
        if(str(row[7]).strip()=="0"):
            fsid_h=0
        if(str(row[8]).strip()=="0"):
            fsid_r=0
        if(str(row[9]).strip()=="0"):
            fmac_h=0
        if(str(row[10]).strip()=="0"):
            fmac_r=0
        if(str(row[11]).strip()=="0"):
            fadid=0
        if(str(row[12]).strip()=="0"):
            fguid=0

        imei_h=1
        imei_r = 1
        imsi_h=1
        imsi_r = 1
        aid_h=1
        aid_r=1
        sid_h=1
        sid_r=1
        mac_h=1
        mac_r=1
        adid=1
        guid=1

        found=0
        with open('GroundTruth_app_wise_hash_stats.csv', encoding="utf8", errors='ignore') as ff:
            csvreader2 = csv.reader(ff, delimiter=',')
            for row2 in csvreader2:
                app=str(row2[0]).strip()
                if (app!=fapp):
                    continue
                else:
                    print("app:", app, " fapp:", fapp)
                    if (str(row2[1]).strip() == "0"):
                        imei_h = 0
                    if (str(row2[2]).strip() == "0"):
                        imei_r = 0
                    if (str(row2[3]).strip() == "0"):
                        imsi_h = 0
                    if (str(row2[4]).strip() == "0"):
                        imsi_r = 0
                    if (str(row2[5]).strip() == "0"):
                        aid_h = 0
                    if (str(row2[6]).strip() == "0"):
                        aid_r = 0
                    if (str(row2[7]).strip() == "0"):
                        sid_h = 0
                    if (str(row2[8]).strip() == "0"):
                        sid_r = 0
                    if (str(row2[9]).strip() == "0"):
                        mac_h = 0
                    if (str(row2[10]).strip() == "0"):
                        mac_r = 0
                    if (str(row2[11]).strip() == "0"):
                        adid = 0
                    if (str(row2[12]).strip() == "0"):
                        guid = 0

                    found=1
                    break


        if found==0:
            print(fapp, " not found")
            continue
        

        app_count+=1
        
        if fimei_h==1 and imei_h==0:
            fp+=1
        elif fimei_h==0 and imei_h==1:
            fn+=1
            print(app, "imei hash fn")
        elif fimei_h == 1 and imei_h == 1:
            tp += 1
        else:
            tn+=1
            
        if fimei_r==1 and imei_r==0:
            fp+=1
        elif fimei_r==0 and imei_r==1:
            fn+=1
            print(app, "imei row fn")
        elif fimei_r == 1 and imei_r == 1:
            tp += 1
        else:
            tn+=1

        if fimsi_h == 1 and imsi_h == 0:
            fp += 1
        elif fimsi_h == 0 and imsi_h == 1:
            fn += 1
            print(app, "imsi hash fn")
        elif fimsi_h == 1 and imsi_h == 1:
            tp += 1
        else:
            tn += 1

        if fimsi_r == 1 and imsi_r == 0:
            fp += 1
        elif fimsi_r == 0 and imsi_r == 1:
            fn += 1
            print(app, "imsi row fn")
        elif fimsi_r == 1 and imsi_r == 1:
            tp += 1
        else:
            tn += 1

        if faid_h == 1 and aid_h == 0:
            fp += 1
        elif faid_h == 0 and aid_h == 1:
            fn += 1
            print(app, "aid hash fn")
        elif faid_h == 1 and aid_h == 1:
            tp += 1
        else:
            tn += 1

        if faid_r == 1 and aid_r == 0:
            fp += 1
        elif faid_r == 0 and aid_r == 1:
            fn += 1
            print(app, "aid row fn")
        elif faid_r == 1 and aid_r == 1:
            tp += 1
        else:
            tn += 1

        if fsid_h == 1 and sid_h == 0:
            fp += 1
        elif fsid_h == 0 and sid_h == 1:
            fn += 1
            print(app, "sid hash fn")
        elif fsid_h == 1 and sid_h == 1:
            tp += 1
        else:
            tn += 1

        if fsid_r == 1 and sid_r == 0:
            fp += 1
        elif fsid_r == 0 and sid_r == 1:
            fn += 1
            print(app, "sid row fn")
        elif fsid_r == 1 and sid_r == 1:
            tp += 1
        else:
            tn += 1
            


        if fmac_h == 1 and mac_h == 0:
            fp += 1
        elif fmac_h == 0 and mac_h == 1:
            fn += 1
            print(app, "mac hash fn")
        elif fmac_h == 1 and mac_h == 1:
            tp += 1
        else:
            tn += 1

        if fmac_r == 1 and mac_r == 0:
            fp += 1
        elif fmac_r == 0 and mac_r == 1:
            fn += 1
            print(app, "mac row fn")
        elif fmac_r == 1 and mac_r == 1:
            tp += 1
        else:
            tn += 1


            
        if fadid == 1 and adid == 0:
            fp += 1
        elif fadid == 0 and adid == 1:
            fn += 1
            print(app, "sid row fn")
        elif fadid == 1 and adid == 1:
            tp += 1
        else:
            tn += 1

        if fguid == 1 and guid == 0:
            fp += 1
        elif fguid == 0 and guid == 1:
            fn += 1
            print(app, "sid row fn")
        elif fguid == 1 and guid == 1:
            tp += 1
        else:
            tn += 1


        

print("Total Apps:", app_count)
print("Total fp: ", fp)
print("Total fn:",fn)
print("Total Tp:" ,tp)
print("Total Tn:" ,tn)

