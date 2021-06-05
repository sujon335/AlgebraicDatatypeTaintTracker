import csv


fw=open('bad_apps_ranking_hash_info.csv','w+')


fw.write('App'+','+'IMEIHashed'+','+'IMEIRaw'+','+'IMSIHashed'+','+'IMSIRaw'+','+'AndroidIDHashed'+','+'AndroidIDRaw'+','+'SerialNoHashed'+','+'SerialNoRaw'+','+'MacAddressHashed'+','+'MacAddressRaw'+','+'ADvID'+','+'GUID')
fw.write('\n')


c = 0
with open('bad_apps_ranking.csv',encoding="utf8", errors='ignore') as f:
    csvreader = csv.reader(f,delimiter=',')

    for row in csvreader:
        leak=0
        if c == 0:
            c+=1
            continue
        app=str(row[0]).strip()
        leak=str(row[1]).strip()
        if leak !="5":
            continue

        with open('app_wise_hash_stats.csv', encoding="utf8", errors='ignore') as ff:
            csvreader2 = csv.reader(ff, delimiter=',')

            for row2 in csvreader2:
                leaks=0
                fapp=str(row2[0]).strip()
                if fapp!=app:
                    continue

                im_raw =row2[2].strip()
                im_hash = row2[1].strip()
                ims_raw = row2[4].strip()
                ims_hash = row2[3].strip()
                aid_raw = row2[6].strip()
                aid_hash = row2[5].strip()
                sid_raw = row2[8].strip()
                sid_hash = row2[7].strip()
                mac_raw = row2[10].strip()
                mac_hash = row2[9].strip()
                adid = row2[11].strip()
                guid = row2[12].strip()



                break

        fw.write(str(app) + ',' + str(im_hash) + ',' + str(im_raw) + ',' + str(
            ims_hash) + ',' + str(ims_raw) + ',' + str(aid_hash) + ',' + str(aid_raw) + ',' + str(sid_hash) + ',' + str(
            sid_raw) + ',' + str(mac_hash) + ',' + str(mac_raw) + ',' + str(adid) + ',' + str(guid))
        fw.write('\n')

# fw=open('bad_apps_ranking.csv','w+')
#
#
# fw.write('App'+','+'Leaks'+','+'IMEI'+','+'IMSI'+','+'AndroidID'+','+'SerialNo'+','+'MacAddress')
# fw.write('\n')
#
# c = 0
# with open('app_wise_hash_stats.csv',encoding="utf8", errors='ignore') as f:
#     csvreader = csv.reader(f,delimiter=',')
#
#     for row in csvreader:
#         leaks=0
#         if c == 0:
#             c+=1
#             continue
#         app=str(row[0]).strip()
#         imei=1
#         imsi=1
#         aid=1
#         sid=1
#         mac=1
#
#
#         if(str(row[2]).strip()=="0"):
#             imei=0
#         if(str(row[4]).strip()=="0"):
#             imsi=0
#         if(str(row[6]).strip()=="0"):
#             aid=0
#         if(str(row[8]).strip()=="0"):
#             sid=0
#         if(str(row[10]).strip()=="0"):
#             mac=0
#
#         if imei==1:
#             leaks+=1
#         if imsi==1:
#             leaks+=1
#         if aid==1:
#             leaks+=1
#         if sid==1:
#             leaks+=1
#         if mac==1:
#             leaks+=1
#
#
#         fw.write(str(app) +','  +str(leaks) +','  +str(imei)+','+ str(imsi)  + ','+str(aid)+','+  str(sid) + ','  +str(mac))
#         fw.write('\n')

