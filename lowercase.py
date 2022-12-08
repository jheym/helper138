import pandas as pd

df = pd.read_csv('transcript.csv')

df['text'] = df['text'].str.lower()


df.to_csv('lowercase-transcript.csv')
