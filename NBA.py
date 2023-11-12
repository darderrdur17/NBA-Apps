import requests
import pandas as pd
import base64
import matplotlib.pyplot as plt
import requests
import pandas as pd
import base64
import numpy as np
import streamlit as st
import plotly.express as px

st.title("National Basketball Association[NBA] Player Stats Explorer")
st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year:', list(reversed(range(1950, 2022))))

@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats

def main():
    selected_year = st.sidebar.slider('Select Year', 2000, 2023, 2022)
    playerstats = load_data(selected_year)

    sorted_unique_team = sorted(playerstats.Tm.unique())
    selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

    unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
    selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

    df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

    st.header('Display Player Stats of Selected Team(s)')
    st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')

    fig = px.scatter(
        df_selected_team,
        x='PTS', y='TRB',
        color='Pos',
        size='Age',
        hover_name='Player',
        title='NBA Player Stats',
        labels={'PTS': 'Points per Game', 'TRB': 'Total Rebounds per Game'},
        template='plotly_dark'
    )
    st.plotly_chart(fig)

    # Download CSV file link
    st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

    # Intercorrelation Heatmap
    if st.button('Intercorrelation Heatmap'):
        st.header('Intercorrelation Matrix Heatmap')
        correlation_heatmap(df_selected_team)

if __name__ == "__main__":
    main()

