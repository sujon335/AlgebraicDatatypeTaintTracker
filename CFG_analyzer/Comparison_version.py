import csv

fw=open('comparison_with_updated_version_2.csv','w+')
# fw.write('Appname'+','+'FirstOrderID'+','+'SecondOrderID'+','+'IDs'+','+'ThirdParty'+','+'Own')
# fw.write('\n')

fw.write('App'+','+'IMEI(TP+H)'+','+'IMEI(TP-H)'+','+'IMEI(TP+R)'+','+'IMEI(TP-R)'+','+'IMEI(O+H)'+','+'IMEI(O-H)'+','+'IMEI(O+R)'+','+'IMEI(O-R)'+
         ','+'IMSI(TP+H)'+','+'IMSI(TP-H)'+','+'IMSI(TP+R)'+','+'IMSI(TP-R)'+','+'IMSI(O+H)'+','+'IMSI(O-H)'+','+'IMSI(O+R)'+','+'IMSI(O-R)'+
          ','+'AndroidID(TP+H)'+','+'AndroidID(TP-H)'+','+'AndroidID(TP+R)'+','+'AndroidID(TP-R)'+','+'AndroidID(O+H)'+','+'AndroidID(O-H)'+','+'AndroidID(O+R)'+','+'AndroidID(O-R)'+
         ',' + 'SerialNo(TP+H)' + ',' + 'SerialNo(TP-H)' + ',' + 'SerialNo(TP+R)' + ',' + 'SerialNo(TP-R)' + ',' + 'SerialNo(O+H)' + ',' + 'SerialNo(O-H)' + ',' + 'SerialNo(O+R)' + ',' + 'SerialNo(O-R)' +
         ',' + 'MacAddress(TP+H)' + ',' + 'MacAddress(TP-H)' + ',' + 'MacAddress(TP+R)' + ',' + 'MacAddress(TP-R)' + ',' + 'MacAddress(O+H)' + ',' + 'MacAddress(O-H)' + ',' + 'MacAddress(O+R)' + ',' + 'MacAddress(O-R)' +
         ','+'ADvID(TP+)'+','+'ADvID(TP-)'+','+'ADvID(O+)'+','+'ADvID(O-)'+','+'GUID(TP+)'+','+'GUID(TP-)'+','+'GUID(O+)'+','+'GUID(O-)')
fw.write('\n')
c = 0
with open('Updated_app_wise_thirdparty_stats.csv',encoding="utf8", errors='ignore') as f:
    csvreader = csv.reader(f,delimiter=',')

    for row in csvreader:
        if c == 0:
            c+=1
            continue
        fapp=str(row[0]).strip()
        fimei_h_tp=1
        fimei_r_tp = 1
        fimei_h_o = 1
        fimei_r_o = 1
        fimsi_h_tp=1
        fimsi_r_tp = 1
        fimsi_h_o = 1
        fimsi_r_o = 1
        faid_h_tp=1
        faid_r_tp = 1
        faid_h_o = 1
        faid_r_o = 1
        fsid_h_tp=1
        fsid_r_tp = 1
        fsid_h_o = 1
        fsid_r_o = 1
        fmac_h_tp=1
        fmac_r_tp = 1
        fmac_h_o = 1
        fmac_r_o = 1
        fadid_tp = 1
        fadid_o = 1
        fguid_tp=1
        fguid_o=1

        if(str(row[1]).strip()=="0"):
            fimei_h_tp=0
        if(str(row[2]).strip()=="0"):
            fimei_r_tp=0
        if(str(row[3]).strip()=="0"):
            fimei_h_o=0
        if(str(row[4]).strip()=="0"):
            fimei_r_o=0
        if(str(row[5]).strip()=="0"):
            fimsi_h_tp=0
        if(str(row[6]).strip()=="0"):
            fimsi_r_tp=0
        if(str(row[7]).strip()=="0"):
            fimsi_h_o=0
        if(str(row[8]).strip()=="0"):
            fimsi_r_o=0
        if(str(row[9]).strip()=="0"):
            faid_h_tp=0
        if(str(row[10]).strip()=="0"):
            faid_r_tp=0
        if(str(row[11]).strip()=="0"):
            faid_h_o=0
        if(str(row[12]).strip()=="0"):
            faid_r_o=0
        if(str(row[13]).strip()=="0"):
            fsid_h_tp=0
        if(str(row[14]).strip()=="0"):
            fsid_r_tp=0
        if(str(row[15]).strip()=="0"):
            fsid_h_o=0
        if(str(row[16]).strip()=="0"):
            fsid_r_o=0
        if(str(row[17]).strip()=="0"):
            fmac_h_tp=0
        if(str(row[18]).strip()=="0"):
            fmac_r_tp=0
        if(str(row[19]).strip()=="0"):
            fmac_h_o=0
        if(str(row[20]).strip()=="0"):
            fmac_r_o=0
        if(str(row[21]).strip()=="0"):
            fadid_tp=0
        if(str(row[22]).strip()=="0"):
            fadid_o=0
        if(str(row[23]).strip()=="0"):
            fguid_tp=0
        if(str(row[24]).strip()=="0"):
            fguid_o=0



        imei_h_tp=1
        imei_r_tp = 1
        imei_h_o = 1
        imei_r_o = 1
        imsi_h_tp=1
        imsi_r_tp = 1
        imsi_h_o = 1
        imsi_r_o = 1
        aid_h_tp=1
        aid_r_tp = 1
        aid_h_o = 1
        aid_r_o = 1
        sid_h_tp=1
        sid_r_tp = 1
        sid_h_o = 1
        sid_r_o = 1
        mac_h_tp=1
        mac_r_tp = 1
        mac_h_o = 1
        mac_r_o = 1
        adid_tp = 1
        adid_o = 1
        guid_tp=1
        guid_o=1

        found=0
        with open('prev_app_wise_thirdparty_stats.csv', encoding="utf8", errors='ignore') as ff:
            csvreader2 = csv.reader(ff, delimiter=',')
            for row2 in csvreader2:
                app=str(row2[0]).strip()
                if (app!=fapp):
                    continue
                else:
                    print("app:", app, " fapp:", fapp)

                    if (str(row2[1]).strip() == "0"):
                        imei_h_tp = 0
                    if (str(row2[2]).strip() == "0"):
                        imei_r_tp = 0
                    if (str(row2[3]).strip() == "0"):
                        imei_h_o = 0
                    if (str(row2[4]).strip() == "0"):
                        imei_r_o = 0
                    if (str(row2[5]).strip() == "0"):
                        imsi_h_tp = 0
                    if (str(row2[6]).strip() == "0"):
                        imsi_r_tp = 0
                    if (str(row2[7]).strip() == "0"):
                        imsi_h_o = 0
                    if (str(row2[8]).strip() == "0"):
                        imsi_r_o = 0
                    if (str(row2[9]).strip() == "0"):
                        aid_h_tp = 0
                    if (str(row2[10]).strip() == "0"):
                        aid_r_tp = 0
                    if (str(row2[11]).strip() == "0"):
                        aid_h_o = 0
                    if (str(row2[12]).strip() == "0"):
                        aid_r_o = 0
                    if (str(row2[13]).strip() == "0"):
                        sid_h_tp = 0
                    if (str(row2[14]).strip() == "0"):
                        sid_r_tp = 0
                    if (str(row2[15]).strip() == "0"):
                        sid_h_o = 0
                    if (str(row2[16]).strip() == "0"):
                        sid_r_o = 0
                    if (str(row2[17]).strip() == "0"):
                        mac_h_tp = 0
                    if (str(row2[18]).strip() == "0"):
                        mac_r_tp = 0
                    if (str(row2[19]).strip() == "0"):
                        mac_h_o = 0
                    if (str(row2[20]).strip() == "0"):
                        mac_r_o = 0
                    if (str(row2[21]).strip() == "0"):
                        adid_tp = 0
                    if (str(row2[22]).strip() == "0"):
                        adid_o = 0
                    if (str(row2[23]).strip() == "0"):
                        guid_tp = 0
                    if (str(row2[24]).strip() == "0"):
                        guid_o = 0

                    found=1
                    break


        if found==0:
            print(fapp, " not found")
            continue

        imeihfp_tp=0
        imeihfn_tp=0
        imeirfp_tp=0
        imeirfn_tp=0
        imeihfp_o=0
        imeihfn_o=0
        imeirfp_o=0
        imeirfn_o=0
        imsihfp_tp=0
        imsihfn_tp=0
        imsirfp_tp=0
        imsirfn_tp=0
        imsihfp_o=0
        imsihfn_o=0
        imsirfp_o=0
        imsirfn_o=0
        aidhfp_tp=0
        aidhfn_tp=0
        aidrfp_tp=0
        aidrfn_tp=0
        aidhfp_o=0
        aidhfn_o=0
        aidrfp_o=0
        aidrfn_o=0
        sidhfp_tp=0
        sidhfn_tp=0
        sidrfp_tp=0
        sidrfn_tp=0
        sidhfp_o=0
        sidhfn_o=0
        sidrfp_o=0
        sidrfn_o=0
        machfp_tp=0
        machfn_tp=0
        macrfp_tp=0
        macrfn_tp=0
        machfp_o=0
        machfn_o=0
        macrfp_o=0
        macrfn_o=0
        adidfp_tp=0
        adidfn_tp=0
        adidfp_o=0
        adidfn_o=0
        guidfp_tp=0
        guidfn_tp=0
        guidfp_o=0
        guidfn_o=0


        if fimei_h_tp==1 and imei_h_tp==0:
            imeihfp_tp=1
        if fimei_h_tp==0 and imei_h_tp==1:
            imeihfn_tp=1            
        if fimei_r_tp==1 and imei_r_tp==0:
            imeirfp_tp=1
        if fimei_r_tp==0 and imei_r_tp==1:
            imeirfn_tp=1
        if fimei_h_o==1 and imei_h_o==0:
            imeihfp_o=1
        if fimei_h_o==0 and imei_h_o==1:
            imeihfn_o=1
        if fimei_r_o==1 and imei_r_o==0:
            imeirfp_o=1
        if fimei_r_o==0 and imei_r_o==1:
            imeirfn_o=1
            
            
        if fimsi_h_tp==1 and imsi_h_tp==0:
            imsihfp_tp=1
        if fimsi_h_tp==0 and imsi_h_tp==1:
            imsihfn_tp=1            
        if fimsi_r_tp==1 and imsi_r_tp==0:
            imsirfp_tp=1
        if fimsi_r_tp==0 and imsi_r_tp==1:
            imsirfn_tp=1
        if fimsi_h_o==1 and imsi_h_o==0:
            imsihfp_o=1
        if fimsi_h_o==0 and imsi_h_o==1:
            imsihfn_o=1
        if fimsi_r_o==1 and imsi_r_o==0:
            imsirfp_o=1
        if fimsi_r_o==0 and imsi_r_o==1:
            imsirfn_o=1
            
            
        if faid_h_tp==1 and aid_h_tp==0:
            aidhfp_tp=1
        if faid_h_tp==0 and aid_h_tp==1:
            aidhfn_tp=1            
        if faid_r_tp==1 and aid_r_tp==0:
            aidrfp_tp=1
        if faid_r_tp==0 and aid_r_tp==1:
            aidrfn_tp=1
        if faid_h_o==1 and aid_h_o==0:
            aidhfp_o=1
        if faid_h_o==0 and aid_h_o==1:
            aidhfn_o=1
        if faid_r_o==1 and aid_r_o==0:
            aidrfp_o=1
        if faid_r_o==0 and aid_r_o==1:
            aidrfn_o=1

        if fsid_h_tp==1 and sid_h_tp==0:
            sidhfp_tp=1
        if fsid_h_tp==0 and sid_h_tp==1:
            sidhfn_tp=1            
        if fsid_r_tp==1 and sid_r_tp==0:
            sidrfp_tp=1
        if fsid_r_tp==0 and sid_r_tp==1:
            sidrfn_tp=1
        if fsid_h_o==1 and sid_h_o==0:
            sidhfp_o=1
        if fsid_h_o==0 and sid_h_o==1:
            sidhfn_o=1
        if fsid_r_o==1 and sid_r_o==0:
            sidrfp_o=1
        if fsid_r_o==0 and sid_r_o==1:
            sidrfn_o=1

        if fmac_h_tp==1 and mac_h_tp==0:
            machfp_tp=1
        if fmac_h_tp==0 and mac_h_tp==1:
            machfn_tp=1            
        if fmac_r_tp==1 and mac_r_tp==0:
            macrfp_tp=1
        if fmac_r_tp==0 and mac_r_tp==1:
            macrfn_tp=1
        if fmac_h_o==1 and mac_h_o==0:
            machfp_o=1
        if fmac_h_o==0 and mac_h_o==1:
            machfn_o=1
        if fmac_r_o==1 and mac_r_o==0:
            macrfp_o=1
        if fmac_r_o==0 and mac_r_o==1:
            macrfn_o=1
            
            
            
        if fadid_tp==1 and adid_tp==0:
            adidfp_tp=1
        if fadid_tp==0 and adid_tp==1:
            adidfn_tp=1
        if fadid_o==1 and adid_o==0:
            adidfp_o=1
        if fadid_o==0 and adid_o==1:
            adidfn_o=1

        if fguid_tp==1 and guid_tp==0:
            guidfp_tp=1
        if fguid_tp==0 and guid_tp==1:
            guidfn_tp=1
        if fguid_o==1 and guid_o==0:
            guidfp_o=1
        if fguid_o==0 and guid_o==1:
            guidfn_o=1


        fw.write(str(fapp) + ','  +str(imeihfp_tp)+','+ str(imeihfn_tp)  + ','+str(imeirfp_tp)+','+  str(imeirfn_tp) + ','  +str(imeihfp_o)+','+ str(imeihfn_o)  + ','+str(imeirfp_o)+','+  str(imeirfn_o) + ','  +str(imsihfp_tp)+','+ str(imsihfn_tp)  + ','+str(imsirfp_tp)+','+  str(imsirfn_tp) + ','  +str(imsihfp_o)+','+ str(imsihfn_o)  + ','+str(imsirfp_o)+','+  str(imsirfn_o)
                  + ','  +str(aidhfp_tp)+','+ str(aidhfn_tp)  + ','+str(aidrfp_tp)+','+  str(aidrfn_tp) + ','  +str(aidhfp_o)+','+ str(aidhfn_o)  + ','+str(aidrfp_o)+','+  str(aidrfn_o)
                  + ','  +str(sidhfp_tp)+','+ str(sidhfn_tp)  + ','+str(sidrfp_tp)+','+  str(sidrfn_tp) + ','  +str(sidhfp_o)+','+ str(sidhfn_o)  + ','+str(sidrfp_o)+','+  str(sidrfn_o)
                  + ','  +str(machfp_tp)+','+ str(machfn_tp)  + ','+str(macrfp_tp)+','+  str(macrfn_tp) + ','  +str(machfp_o)+','+ str(machfn_o)  + ','+str(macrfp_o)+','+  str(macrfn_o)
                  + ','  +str(adidfp_tp)+','+ str(adidfn_tp)  + ','+str(adidfp_o)+','+  str(adidfn_o) + ','  +str(guidfp_tp)+','+ str(guidfn_tp)  + ','+str(guidfp_o)+','+  str(guidfn_o))
        fw.write('\n')

