import requests
import base64
from datetime import datetime, timedelta
from io import StringIO
import pandas as pd
import argparse

states = [
    'Alabama','Alaska','American Samoa','Arizona',
    'Arkansas','California','Colorado','Connecticut','Delaware',
    'Diamond Princess','District of Columbia','Florida','Georgia',
    'Grand Princess','Guam','Hawaii','Idaho','Illinois',
    'Indiana','Iowa','Kansas','Kentucky','Louisiana',
    'Maine','Maryland','Massachusetts','Michigan','Minnesota',
    'Mississippi','Missouri','Montana','Nebraska',
    'Nevada','New Hampshire','New Jersey','New Mexico',
    'New York','North Carolina','North Dakota','Northern Mariana Islands',
    'Ohio','Oklahoma','Oregon','Pennsylvania','Puerto Rico',
    'Rhode Island','South Carolina','South Dakota','Tennessee',
    'Texas','Utah','Vermont','Virgin Islands','Virginia',
    'Washington','West Virginia','Wisconsin','Wyoming'
]

def get_date_stats(date, token=None):
    date_string = date.strftime('%m-%d-%Y') 
    url = f'https://api.github.com/repos/CSSEGISandData/COVID-19/contents/csse_covid_19_data/csse_covid_19_daily_reports_us/{date_string}.csv'
    
    if token:
        response = requests.get(url, headers={'Authorization' : f'token {token}'})
    else:
        response = requests.get(url)

    sha = response.json()['sha']
    url = f'https://api.github.com/repos/CSSEGISandData/COVID-19/git/blobs/{sha}'

    if token:
        response = requests.get(url, headers={'Authorization' : f'token {token}'})
    else:
        response = requests.get(url)

    content = response.json()['content']
    csv = base64.b64decode(content).decode('utf-8')

    buffer = StringIO(csv)
    df = pd.read_csv(buffer)

    return list(df['Confirmed']), list(df['Deaths'])


def init_data(confirmed_file, deaths_file, token):
    date = datetime.strptime('4-12-2020', '%m-%d-%Y')
    today = datetime.today()

    confirmed = {'State' : states}
    deaths = {'State': states}

    while date.date() < today.date():
        date_string = date.strftime("%m-%d-%Y") 
        date_confirmed, date_deaths = get_date_stats(date_string)

        if len(date_confirmed) > 58:
            del date_confirmed[45]
        confirmed[date_string] = date_confirmed
        
        if len(date_deaths) > 58:
            del date_deaths[45]
        deaths[date_string] = date_deaths
    
    with open(confirmed_file, 'w') as f:
        pd.DataFrame(data=confirmed).to_csv(f, index=False)

    with open(deaths_file, 'w') as f:
        pd.DataFrame(data=deaths).to_csv(f, index=False) 
    


def update_data(confirmed_file, deaths_file):
    today = datetime.today()

    with open(confirmed_file, 'r') as f:
        confirmed_df = pd.read_csv(f)
    
    with open(deaths_file, 'r') as f:
        deaths_df = pd.read_csv(f)

    date = today.strftime("%m-%d-%Y") 
    confirmed, deaths = get_date_stats(date)

    confirmed_df[date] = confirmed
    deaths_df[date] = deaths

    with open(confirmed_file, 'w') as f:
        confirmed_df.to_csv(f, index=False)
    
    with open(deaths_file, 'w') as f:
        deaths_df.to_csv(f, index=False)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help='Update option (defaults to create database)', const=True, default=False)
    parser.add_argument('-t', required=False, help='Github user token')

    args = parser.parse_args()

    update = args.u

    if update:
        update_data('confirmed_us.csv', 'deaths_us.csv')
    else:
        token = args.t
        init_data('confirmed_us.csv', 'deaths_us.csv', token)