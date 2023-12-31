import streamlit as st
import pandas as pd
import base64
import plotly.express as px

st.set_page_config(
    page_title="NBA Player Stats Explorer",
    page_icon="🏀",
    layout="wide"
)

st.title('NBA Player Stats Explorer')
st.write(
    "Welcome to the NBA Player Stats Explorer! "
    "Select the year, team, and position to explore player statistics."
)

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Select Year:', list(reversed(range(1950, 2022))))

@st.cache(allow_output_mutation=True)
def load_data(year):
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats

playerstats = load_data(selected_year)

if playerstats is not None:
    sorted_unique_team = sorted(playerstats.Tm.unique())
    selected_team = st.sidebar.multiselect('Select Team(s)', sorted_unique_team, sorted_unique_team)

    unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
    selected_pos = st.sidebar.multiselect('Select Position(s)', unique_pos, unique_pos)

    df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

    if not df_selected_team.empty:
        st.header('Displaying Player Stats')
        st.write(f'Data Dimension: {df_selected_team.shape[0]} rows and {df_selected_team.shape[1]} columns.')
        st.dataframe(df_selected_team)

        def file_download(df):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
            return href

        st.markdown(file_download(df_selected_team), unsafe_allow_html=True)

        if st.button('Generate Intercorrelation Heatmap'):
            st.header('Intercorrelation Matrix Heatmap')

        # Exclude non-numeric columns before calculating correlation
            numeric_cols = df_selected_team.select_dtypes(include='number')

            if not numeric_cols.empty:
                corr = numeric_cols.corr()
                fig = px.imshow(corr, x=corr.index, y=corr.columns, color_continuous_scale='Viridis', labels=dict(color='Correlation'))
                fig.update_layout(title_text='Intercorrelation Matrix Heatmap', width=800, height=600)
                st.plotly_chart(fig)
            else:
                st.warning("No numeric columns to generate the heatmap.")
else:
    st.warning("No data to display based on the selected filters.")

