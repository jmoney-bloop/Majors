from config import TEAMS, URL
import pandas as pd
import streamlit as st

def get_stats():
    df = pd.read_html(URL, flavor = 'lxml')
    return df[0]

def limit_df(df):
    df_list = []
    for owner, team in TEAMS.items():
        filtered = df[df['PLAYER'].isin(team)].copy()
        filtered['Owner'] = owner
        df_list.append(filtered)
    return pd.concat(df_list)

def parse_score(df):
    df = df.copy()
    df['SCORE'] = df['SCORE'].apply(lambda x: 0 if x == 'E' else x)
    df['SCORE'] = df['SCORE'].apply(lambda x: 15 if x == 'CUT' else x)
    df['SCORE'] = pd.to_numeric(df['SCORE'])
    df = df.sort_values(by='SCORE')
    return df

def team_scores(df):
    rows = []
    for owner, group in df.groupby('Owner'):
        best = group.nsmallest(4, 'SCORE')
        total = best['SCORE'].sum()
        players = group['PLAYER'].tolist()
        scores = group['SCORE'].tolist()
        row = {'Owner': owner, 'Total': total}
        for i, (player, score) in enumerate(zip(players, scores), 1):
            row[f'G{i}'] = f'{player} ({score})'
        rows.append(row)

    result = pd.DataFrame(rows).sort_values('Total').reset_index(drop=True)
    return result
@st.cache_data
def get_df():
    stats = get_stats()
    df = limit_df(stats)
    df = parse_score(df)
    df = team_scores(df)
    return df