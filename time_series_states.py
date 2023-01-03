import requests
import base64
from io import StringIO
import pandas as pd


url = 'https://api.github.com/repos/CSSEGISandData/COVID-19/contents/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'

response = requests.get(url)
sha = response.json()['sha']

url = f'https://api.github.com/repos/CSSEGISandData/COVID-19/git/blobs/{sha}'
response = requests.get(url)
content = response.json()['content']

csv = base64.b64decode(content).decode("utf-8")


buffer = StringIO(csv)
df = pd.read_csv(buffer)

df = df.groupby('Province_State', as_index=False).sum()

df.to_csv('time-series.csv', index=False)