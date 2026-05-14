import requests
import pandas as pd


r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
data = r.json()


competitors = data['events'][0]['competitions'][0]['competitors']
rows = []
for c in competitors:
    rows.append({
        'PLAYER': c['athlete']['displayName'],
        'SCORE': c['score']['displayValue']
    })

df = pd.DataFrame(rows)
from utils import team_set, limit_df
df = limit_df(df)
df = team_set(df)
print(df.head())