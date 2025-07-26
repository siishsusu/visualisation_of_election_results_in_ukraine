import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from scipy.stats import gaussian_kde


map_path = 'data/maps/ua.json'


def get_scales_sizes(raw_sizes):
    min_size = 5
    max_size = 50

    normalized_sizes = (raw_sizes - raw_sizes.min()) / (raw_sizes.max() - raw_sizes.min())
    return normalized_sizes * (max_size - min_size) + min_size


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
    df['number_votes'] = (
        df['num_voters_per_region'] * (df['percent_votes'] / 100)
    ).round(0).astype(int)

    st.subheader("📋 Raw Data Preview")
    st.dataframe(df)

    st.subheader("📈 Basic Summary Stats")
    st.markdown(f":green[**Total Regions:**] {df['region'].nunique()}")
    st.markdown(f":green[**Total Candidates:**] {df['candidate'].nunique()}")
    st.markdown(f":green[**Total Votes (sum):**] {df['number_votes'].sum():,}")
    st.markdown(f":orange[**What is the average percentage of votes received per candidate?**] \
                {df['percent_votes'].mean():.2f}%")
    st.markdown(f":orange[**Which candidate received the highest number of votes overall?**] \
                {df.loc[df['number_votes'].idxmax(), 'candidate']}")

    st.subheader("📌 Select Candidate to View Details")
    selected = st.selectbox("Choose a candidate:", df['candidate'].unique())
    candidate_data = df[df['candidate'] == selected].iloc[0]

    st.markdown(f":green[**Candidate:**] {selected}")
    st.markdown(f":green[**Votes:**] {candidate_data['number_votes'].sum():,}")
    st.markdown(f":green[**% of Total:**] {candidate_data['percent_votes'].sum()}%")

    df_candidate = df[df['candidate'] == candidate_data['candidate']]

    st.dataframe(df_candidate)

    # 1. In which regions did chosen candidate perform the best and worst?
    st.info(f':orange[In which regions did chosen candidate\
             (*{candidate_data["candidate"]}*) perform the best and worst?]')
    
    df_places = gpd.read_file(map_path)
    df_candidate_map = df_places.merge(df_candidate, left_on='name', right_on='region_eng', how='left')
    df_candidate_map['number_votes'] = df_candidate_map['number_votes'].fillna(0)

    df_candidate_map['centroid_lon'] = df_candidate_map.geometry.centroid.x
    df_candidate_map['centroid_lat'] = df_candidate_map.geometry.centroid.y

    geojson_data = df_candidate_map.__geo_interface__

    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=df_candidate_map.index,
        z=df_candidate_map['number_votes'],
        colorscale='Reds',
        marker_opacity=0.6,
        marker_line_width=0.5,
        text=df_candidate_map['region_eng'],
        hoverinfo='text+z'
    ))

    scaled_sizes = get_scales_sizes(df_candidate_map['number_votes'])

    fig.add_trace(go.Scattermapbox(
        lon=df_candidate_map['centroid_lon'],
        lat=df_candidate_map['centroid_lat'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size= scaled_sizes,  
            color='red',
            opacity=0.4
        ),
        text=df_candidate_map['region_eng'] + '<br>Votes: ' +\
              df_candidate_map['number_votes'].astype(str),
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
                *{df_candidate[df_candidate['number_votes'] == df_candidate['number_votes'].max()]['region'].values[0]} область* \
                    and the worst at \
                        *{df_candidate[df_candidate['number_votes'] == df_candidate['number_votes'].min()]['region'].values[0]} область*")

    # 3. How does each candidate's vote percentage vary across regions?
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df_candidate['region'], y=df_candidate['percent_votes'], 
                   mode='lines+markers',
                   marker=dict(color='red'))
    )

    fig.update_layout(
        title='Vote percentage variation across regions.',
        yaxis=dict(
            title='Percentage of Votes Received',
            side='left'
        ),
        xaxis=dict(title='Region')
    )

    st.plotly_chart(fig)
    
    st.subheader("📉 General Visualizations")
    
    # 2. Which candidate won in each region?
    st.info(f':orange[Which candidate won in each region?]')

    df_top_candidates = (
        df
        .groupby('region')
        .apply(lambda group: group.nsmallest(1, columns='rating'))
        .reset_index(level=-1, drop=True)
    )

    df_top_candidate_map = df_places.merge(df_top_candidates, 
                                left_on='name', right_on='region_eng', 
                                how='left')
    df_top_candidate_map['number_votes'] = df_top_candidate_map['number_votes'].fillna(0)

    df_top_candidate_map['centroid_lon'] = df_top_candidate_map.geometry.centroid.x
    df_top_candidate_map['centroid_lat'] = df_top_candidate_map.geometry.centroid.y

    geojson_data = df_top_candidate_map.__geo_interface__

    fig = go.Figure()

    candidate_names = df_top_candidate_map['candidate'].unique()
    candidate_color_map = {name: i for i, name in enumerate(candidate_names)}
    df_top_candidate_map['color_id'] = df_top_candidate_map['candidate'].map(candidate_color_map)
    colors = px.colors.sequential.Reds
    custom_colorscale = [[i / (len(colors) - 1), color] for i, color in enumerate(colors[:len(candidate_names)])]
    
    fig.add_trace(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=df_top_candidate_map.index,  
        z=df_top_candidate_map['color_id'], 
        colorscale=custom_colorscale,
        marker_opacity=0.6,
        marker_line_width=0.5,
        text=(
            'Region: ' + df_top_candidate_map['region_eng'] +
            '<br>Candidate: ' + df_top_candidate_map['candidate'] +
            '<br>Voters: ' + df_top_candidate_map['number_votes'].astype(str)
        ),
        hoverinfo='text',
        showscale=False  
    ))
    
    scaled_sizes = get_scales_sizes(df_top_candidate_map['number_votes'])

    fig.add_trace(go.Scattermapbox(
        lon=df_top_candidate_map['centroid_lon'],
        lat=df_top_candidate_map['centroid_lat'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=scaled_sizes,  
            color='red',
            opacity=0.4
        ),
        text=df_top_candidate_map['candidate'] + '<br>Region: ' + df_top_candidate_map['region_eng'] + '<br>Votes: ' +\
              df_top_candidate_map['number_votes'].astype(str),
        hoverinfo='text'
    ))

    fig.update_layout(
        mapbox_style='open-street-map',
        mapbox_zoom=4.5,
        mapbox_center={'lat': 48.3, 'lon': 31},
        margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=f'Number of Voters per Region for Best Voted Candidates'
    )

    st.plotly_chart(fig)

    st.markdown(
        f""":orange[**Answer:**] There are *{df_top_candidates["candidate"].nunique()}* different winners by region: 
        *{', '.join(df_top_candidates["candidate"].unique())}*. 
        {'; '.join([f"{cand} won in {df_top_candidates['candidate'].value_counts()[cand]} regions" 
                    for cand in df_top_candidates["candidate"].unique()])}"""
    )

    # 4. Which region had the highest overall voter turnout?
    st.info(f':orange[Which region had the highest overall voter turnout?]')
    regions_data = df.groupby(by='region')[['number_votes']].sum()
    
    fig = go.Figure()

    max_row = regions_data.loc[regions_data['number_votes'].idxmax()]
    max_region = regions_data['number_votes'].idxmax()

    regions_data['color'] = ['red' if region == max_region \
                             else 'grey' for region in regions_data.index]

    fig.add_trace(go.Bar(
        x=regions_data.index,
        y=regions_data['number_votes'],
        marker_color=regions_data['color']
    ))

    fig.update_layout(
        title='Total Number of Voters Per Region',
        yaxis=dict(
            title='Total Number of Votes',
            side='left'
        ),
        xaxis=dict(
            title='Region'
        )
    )

    st.plotly_chart(fig)
    st.markdown(f":orange[**Answer:**] region with the highest number of votes is: \
                {max_region}")
    
    # 5. Which candidate had the highest average rating across all regions?
    st.info(f':orange[Which candidate had the highest average rating across all regions?]')
    candidates_regions_data = df.groupby(by='candidate')[['number_votes']].mean()

    fig = go.Figure()

    max_row = candidates_regions_data.loc[candidates_regions_data['number_votes'].idxmax()]
    average_best_candidate = candidates_regions_data['number_votes'].idxmax()
    
    candidates_regions_data['color'] = ['red' if candidate == average_best_candidate \
                             else 'grey' for candidate in candidates_regions_data.index]

    fig.add_trace(go.Bar(
        x=candidates_regions_data.index,
        y=candidates_regions_data['number_votes'],
        marker_color=candidates_regions_data['color']
    ))

    fig.update_layout(
        title='Average Number of Votes Per Candidate Across All Regions',
        yaxis=dict(
            title='Average Number of Votes',
            side='left'
        ),
        xaxis=dict(
            title='Candidate'
        )
    )

    st.plotly_chart(fig)
    st.markdown(f":orange[**Answer:**] candidate with the highest average number \
                of votes is: {average_best_candidate}")
