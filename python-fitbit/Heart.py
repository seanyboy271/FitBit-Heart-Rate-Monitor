import fitbit
import pandas as pd
import datetime
import gather_keys_oauth2 as Oauth2
CLIENT_ID = '22DHWL'
CLIENT_SECRET = "643bca83d2b5bc091bac689297b5f3af"


print("Input the date that you would like to collect data from (yyyy-MM-dd or 'today'): ")
date = input()
print("Input the start time for the data you would like to collect (HH:mm) or 'All' for all of the selected date's data:")
start_time = input()
if not start_time.lower() == 'all':
    print("Input the end time for the data you would like to collect (HH:mm): ")
    end_time = input()
else:
    end_time = None
    start_time = None


server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)


yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
today = str(datetime.datetime.now().strftime("%Y-%m-%d"))


fit_statsHR = auth2_client.intraday_time_series('activities/heart', detail_level='1sec', start_time = start_time, end_time = end_time, base_date=date)


time_list = []
val_list = []
for i in fit_statsHR['activities-heart-intraday']['dataset']:
    val_list.append(i['value'])
    time_list.append(i['time'])
heartdf = pd.DataFrame({'Heart Rate':val_list,'Time':time_list})



if date.lower() == "today":
    date = today
dateList = date.split('-')
year = dateList[0]
month = dateList[1]
day = dateList[2]


fileName = day + "-" + month + "-" + year + " Results.csv"
heartdf.to_csv('C:/Users/BeepBoop/Desktop/FitBit Data Extraction/Results/' + fileName, \
               columns=['Time','Heart Rate'], header=True, \
               index = False)