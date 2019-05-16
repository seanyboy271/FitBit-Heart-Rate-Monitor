import fitbit
import pandas as pd
import datetime
import gather_keys_oauth2 as Oauth2
import statistics
CLIENT_ID = '22DHWL'
CLIENT_SECRET = "643bca83d2b5bc091bac689297b5f3af"

#Gathering base_date, start time, end time, and fileName from user input
print("Input the date that you would like to collect data from (MM-dd-YYYY or 'today'): ")
date = input()
if not date == "today":
    dateList = date.split("-")
    month = dateList[0]
    day = dateList[1]
    year = dateList[2]
    date = year + "-" + month + "-" + day
print("Input the start time for the data you would like to collect (HH:mm) or 'All' for all of the selected date's data:")
start_time = input()
if not start_time.lower() == 'all':
    print("Input the end time for the data you would like to collect (HH:mm): ")
    end_time = input()
else:
    end_time = None
    start_time = None
print("Input the desired name for the output file. The file name must not contain any special characters (<, >, :, \", \, |, ?, *)\n"
      + " or press enter for the default file name (MM-dd-YY Results.csv)")
fileName = input()

#Ensuring that the fileName has an extension
if not fileName.__contains__(".") and not fileName == "":
    fileName = fileName + ".csv"

#Authorizing CLIENT_ID, and CLIENT_SECRET
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()

#Aquiring ACCESS_TOKEN and REFRESH_TOKEN
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

#Establishing API Connection
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

#Requesting data from API
fit_statsHR = auth2_client.intraday_time_series('activities/heart', detail_level='1sec', start_time = start_time, end_time = end_time, base_date=date)

#Formatting data into a time and value list
time_list = []
val_list = []
for i in fit_statsHR['activities-heart-intraday']['dataset']:
    val_list.append(i['value'])
    time_list.append(i['time'])

if not val_list or not time_list:
    print("No data was found. Please try again with a different date/time combination")
    exit(1)
#Determining the Max Heart rate, Time of Max Heart rate, Min Heart Rate, Time of Min Heart Rate, and Average heart rate
maxHeartRate = max(val_list)
timeIndex = val_list.index(maxHeartRate)
timeOfMax = time_list[timeIndex]

minHeartRate = min(val_list)
timeIndex = val_list.index(minHeartRate)
timeOfMin = time_list[timeIndex]

average = statistics.mean(val_list)

#Adding data to a dataframe
heartdf = pd.DataFrame({'Heart Rate':val_list,'Time':time_list})
heartdf.loc[0, 'Max Heart Rate'] = maxHeartRate
heartdf.loc[0, 'Time of Max'] = timeOfMax
heartdf.loc[0, 'Minimum Heart Rate'] = minHeartRate
heartdf.loc[0, 'Time of Minimum'] = timeOfMin
heartdf.loc[0, 'Average Heart Rate'] = average

#Establising default file name
if date.lower() == "today":
    today = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    date = today
dateList = date.split('-')
year = dateList[0]
month = dateList[1]
day = dateList[2]
fileNameDate = month + "-" + day + "-" + year
heartdf.loc[0, 'Data is from'] = fileNameDate
if not fileName:
    fileName = month + "-" + day + "-" + year + " Results.csv"

#Converting dataframe to a CSV and storing it into Results folder
heartdf.to_csv('C:/Users/BeepBoop/Desktop/FitBit Data Extraction/Results/' + fileName,
               columns=['Time','Heart Rate', 'Max Heart Rate', 'Time of Max', 'Minimum Heart Rate', 'Time of Minimum', 'Average Heart Rate', 'Data is from'], header=True,
               index = False)