import sys

ff = open('../Flowdroidresult_finance.txt','r')
fw=open('../Flowdroid_result_finance.csv','w+')
# fw.write('Appname'+','+'FirstOrderID'+','+'SecondOrderID'+','+'IDs'+','+'ThirdParty'+','+'Own')
# fw.write('\n')

fw.write('App'+','+'IMEI'+','+'IMSI'+','+'AndroidID'+','+'SerialNo'+','+'MacAddress'+','+'ADvID'+','+'GUID')
fw.write('\n')


Apps = []

for line in ff:
	line = line.strip('\n')
	Apps.append(line)


IMEI1="<android.telephony.TelephonyManager: java.lang.String getDeviceId()>"
IMSI1="<android.telephony.TelephonyManager: java.lang.String getSimSerialNumber()>"
AndroidID="<android.provider.Settings$Secure: java.lang.String getString(android.content.ContentResolver,java.lang.String)>"
UUID="<java.util.UUID: java.util.UUID randomUUID()>"
Serial="<android.os.Build: java.lang.String getSerial()>"
Mac="<android.net.wifi.WifiInfo: java.lang.String getMacAddress()>"
AdvertisingID="<com.google.android.gms.ads.identifier.AdvertisingIdClient.Info: java.lang.String getId()>"


for app in Apps:
	im=0
	ims=0
	aid=0
	sid=0
	mac=0
	adid=0
	guid=0
	leak=0
	appname=str(app)
	appfile="../Financeresults/"+appname
	try:
		fi=open(appfile,'r')
		for line in fi:
			line = line.strip('\n')
			if IMEI1 in line :
				im+=1
			elif IMSI1 in line :
				ims+=1
			elif AndroidID in line:
				aid+=1
			# elif Serial in line:
			# 	#print(line)
			# 	sid+=1
			elif Mac in line:
				mac+=1
			elif AdvertisingID in line:
				adid+=1
			elif UUID in line:
				guid+=1

			if "leak" in line:
				arr=line.split(' ')
				leak=int(arr[-2])

		print("App: ",appname, leak)
		fw.write(str(appname) +  ',' + str(im) + ',' + str(ims) + ',' + str(aid)  + ',' +str(sid)  + ',' + str(mac)  + ',' + str(adid) + ',' + str(guid))
		fw.write('\n')


	except:
		print('cant open')
		continue






