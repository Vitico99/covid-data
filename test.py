import pandas as pd

with open('confirmed_us.csv', 'r') as f:
    df = pd.read_csv(f)

a = [0] * len(df['10-10-2020'])
df['abc'] = a

with open('confirmed_us.csv', 'w') as f:
    df.to_csv(f, index=False)