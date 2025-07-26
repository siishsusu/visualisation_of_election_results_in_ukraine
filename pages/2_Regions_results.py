import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from scipy.stats import gaussian_kde


map_path = 'data/maps/ua.json'


st.set_page_config(page_title="Election Results Per Regions Viewer", layout="centered")

st.title("📊 Regions' Election Results Dashboard")

if "selected_file" not in st.session_state:
    st.session_state.selected_file = None

if not st.session_state.selected_file:
    st.info("👋 Welcome! Please select a file below to view the data.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("**2019**"):
        st.session_state.selected_file = 'data/preprocessed/2019/regions_2019.csv'

with col2:
    if st.button("**2014**"):
        st.session_state.selected_file = 'data/preprocessed/2014/regions_2014.csv'

with col3:
    if st.button("**2010**"):
        st.session_state.selected_file = 'data/preprocessed/2010/regions_2010.csv'

with col4:
    if st.button("**2004**"):
        st.session_state.selected_file = 'data/preprocessed/2004/regions_2004.csv'

if st.session_state.selected_file:
    df = pd.read_csv(st.session_state.selected_file)

if st.session_state.selected_file:
    df = pd.read_csv(st.session_state.selected_file)

    st.subheader("📋 Raw Data Preview")
    st.dataframe(df)

    st.subheader("📈 Basic Summary Stats")
    st.markdown(f":green[**Total Regions:**] {df['region'].nunique()}")
    st.markdown(f":green[**Total Candidates:**] {df['candidate'].nunique()}")
    st.markdown(f":green[**Total Votes (sum):**] {df['num_voters_per_region'].sum():,}")
    st.markdown(f":orange[**What is the average percentage of votes received per candidate?**] \
                {df['percent_votes'].mean():.2f}%")
    st.markdown(f":orange[**Which candidate received the highest number of votes overall?**] \
                {df.loc[df['num_voters_per_region'].idxmax(), 'candidate']}")

    st.subheader("📌 Select Candidate to View Details")
    selected = st.selectbox("Choose a candidate:", df['candidate'].unique())
    candidate_data = df[df['candidate'] == selected].iloc[0]

    st.markdown(f":green[**Candidate:**] {selected}")
    st.markdown(f":green[**Votes:**] {candidate_data['num_voters_per_region'].sum():,}")
    st.markdown(f":green[**% of Total:**] {candidate_data['percent_votes'].sum()}%")

    df_candidate = df[df['candidate'] == candidate_data['candidate']]

    st.dataframe(df_candidate)

    # 1. In which regions did chosen candidate perform the best and worst?
    st.info(f':orange[In which regions did chosen candidate\
             (*{candidate_data["candidate"]}*) perform the best and worst?]')
    
    df_places = gpd.read_file(map_path)
    df_places = df_places.merge(df_candidate, left_on='name', right_on='region_eng', how='left')
    df_places['num_voters_per_region'] = df_places['num_voters_per_region'].fillna(0)

    df_places['centroid_lon'] = df_places.geometry.centroid.x
    df_places['centroid_lat'] = df_places.geometry.centroid.y

    geojson_data = df_places.__geo_interface__

    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=df_places.index,
        z=df_places['num_voters_per_region'],
        colorscale='Reds',
        marker_opacity=0.6,
        marker_line_width=0.5,
        text=df_places['region_eng'],
        hoverinfo='text+z'
    ))

    fig.add_trace(go.Scattermapbox(
        lon=df_places['centroid_lon'],
        lat=df_places['centroid_lat'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=df_places['num_voters_per_region'] / 20000,  
            color='red',
            opacity=0.4
        ),
        text=df_places['region_eng'] + '<br>Votes: ' +\
              df_places['num_voters_per_region'].astype(str),
        hoverinfo='text'
    ))

    fig.update_layout(
        mapbox_style='open-street-map',
        mapbox_zoom=4.5,
        mapbox_center={'lat': 48.3, 'lon': 31},
        margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=f'Number of Voters per Region for {candidate_data["candidate"]}'
    )

    st.plotly_chart(fig)

    st.markdown(f":orange[**Answer:**] the candidate *{candidate_data['candidate']}* \
                performed the best at \
                *{df_candidate[df_candidate['num_voters_per_region'] == df_candidate['num_voters_per_region'].max()]['region'].values[0]} область* \
                    and the worst at \
                        *{df_candidate[df_candidate['num_voters_per_region'] == df_candidate['num_voters_per_region'].min()]['region'].values[0]} область*")

    st.subheader("📉 General Visualizations")
