from config import TEAMS, URL, WILDCARDS
import pandas as pd
import streamlit as st
import requests

def get_stats():
    r = requests.get(URL, headers={'User-Agent': 'Mozilla/5/0'})
    data = r.json()

    competitors = data['events'][0]['competitions'][0]['competitors']
    rows = []

    for c in competitors:
        rows.append({
            'PLAYER': c['athlete']['displayName'],
            'SCORE': c['score']['displayValue']
        })
    return pd.DataFrame(rows)
    
def limit_df(df):
    df_list = []
    for owner, team in TEAMS.items():
        filtered = df[df['PLAYER'].isin(team)].copy()
        filtered['Owner'] = owner
        df_list.append(filtered)
    df = pd.concat(df_list)
    return df

def parse_score(df):
    df = df.copy()
    df['SCORE'] = df['SCORE'].apply(lambda x: 0 if x in ('E', '-') else x)
    df['SCORE'] = df['SCORE'].apply(lambda x: 15 if x == 'CUT' else x)
    df['SCORE'] = pd.to_numeric(df['SCORE'], errors='coerce')
    df = df.sort_values(by='SCORE')
    return df
def team_set(df):
    rows = []
    for owner, group in df.groupby('Owner'):
        players = group['PLAYER'].tolist()
        row = {'Owner': owner,}
        for i, player in enumerate(players, 1):
            row[f'G{i}'] = f'{player}'
        rows.append(row)
    result = pd.DataFrame(rows)
    return result
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
def add_wildcard(df, main_df):
    wc_rows = []
    for owner, player in WILDCARDS.items():
        row = df[df['PLAYER'] == player][['PLAYER', 'SCORE']].copy()
        row['Owner'] = owner
        row['WC'] = True
        wc_rows.append(row)
    
    wc_df = pd.concat(wc_rows)
    final_df = pd.merge(main_df, wc_df, on=['Owner', 'PLAYER', 'SCORE'], how='left')
    final_df['WC'] = final_df['WC'].fillna(False)
    return final_df
@st.cache_data
def get_df():
    stats = get_stats()
    df = limit_df(stats)
    if "SCORE" not in stats.columns:
        return team_set(df)
    df = parse_score(df)
    df = team_scores(df)
    return df
