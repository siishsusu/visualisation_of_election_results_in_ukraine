import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from scipy.stats import gaussian_kde


st.set_page_config(page_title="Election Results Viewer", layout="centered")

st.title("📊 Election Results Dashboard")

if "selected_file" not in st.session_state:
    st.session_state.selected_file = None

if not st.session_state.selected_file:
    st.info("👋 Welcome! Please select a file below to view the data.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("**2019**"):
        st.session_state.selected_file = 'data/preprocessed/2019/final_2019.csv'

with col2:
    if st.button("**2014**"):
        st.session_state.selected_file = 'data/preprocessed/2014/final_2014.csv'

with col3:
    if st.button("**2010**"):
        st.session_state.selected_file = 'data/preprocessed/2010/final_2010.csv'

with col4:
    if st.button("**2004**"):
        st.session_state.selected_file = 'data/preprocessed/2004/final_2004.csv'

if st.session_state.selected_file:
    df = pd.read_csv(st.session_state.selected_file)

    st.subheader("📋 Raw Data Preview")
    st.dataframe(df)

    st.subheader("📈 Basic Summary Stats")
    st.markdown(f":green[**Total Candidates:**] {df['candidate'].nunique()}")
    st.markdown(f":green[**Total Voters (sum):**] {df['number_voters'].sum():,}")
    st.markdown(f":orange[**What is the average percentage of votes received per candidate?**] \
                {df['percent_voters'].mean():.2f}%")
    st.markdown(f":orange[**Which candidate received the highest number of votes overall?**] \
                {df.loc[df['number_voters'].idxmax(), 'candidate']}")

    st.subheader("📌 Select Candidate to View Details")
    selected = st.selectbox("Choose a candidate:", df['candidate'].unique())
    candidate_data = df[df['candidate'] == selected].iloc[0]

    st.markdown(f":green[**Candidate:**] {selected}")
    st.markdown(f":green[**Votes:**] {candidate_data['number_voters']:,}")
    st.markdown(f":green[**% of Total:**] {candidate_data['percent_voters']}%")

    st.subheader("📉 General Visualizations")
    
    # 1. Who are the top candidates by number of votes?
    st.info(f":orange[Who are the top candidates by number of votes?]")
    top_candidates = df.sort_values('number_voters', ascending=False).iloc[:5]
    
    max_val = max(top_candidates['percent_voters'])
    colors = {
        candidate: (
            'red' if percent == max_val
            else 'maroon' if percent == candidate_data['percent_voters']
            else 'grey'
        )
        for candidate, 
        percent in zip(top_candidates['candidate'], 
                       top_candidates['percent_voters'])
    }

    fig = px.bar(top_candidates, 
                  x="percent_voters", 
                  y="candidate", 
                  title="Top candidates by the number of total votes received", 
                  color='candidate',
                  color_discrete_map=colors)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig)
    st.markdown(f":orange[**Answer:**] Top {top_candidates.shape[0]} \
                candidates, who received the most votes are: \
                {', '.join(top_candidates['candidate'].values)}.")
    

    # 2. What is the distribution of vote percentages across all candidates?
    st.info(f":orange[What is the distribution of vote percentages across all candidates?]")
    data = df['percent_voters'].values

    kde = gaussian_kde(data)
    x_range = np.linspace(min(data), max(data), 500)
    kde_values = kde(x_range)

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=data,
        histnorm='probability density',
        name='Histogram',
        marker_color='maroon'
    ))

    fig.add_trace(go.Scatter(
        x=x_range,
        y=kde_values,
        mode='lines',
        line=dict(color='red', width=2)
    ))

    fig.update_layout(
        title='Distribution of vote percentages across all candidates',
        xaxis_title='Percent of Voters',
        yaxis_title='Density',
        bargap=0.05
    )
    
    st.plotly_chart(fig)

    # 3. How is the total vote share distributed among candidates?
    st.info(f":orange[How is the total vote share distributed among candidates?]")
    
    fig = px.pie(df, 
                  values="percent_voters", 
                  names="candidate", 
                  title="Total vote share distributed among candidates", 
                  color='candidate',
                  color_discrete_sequence=px.colors.sequential.solar)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig)
    max_votes = df['number_voters'].max()
    min_votes = df['number_voters'].min()
    st.markdown(f":orange[**Answer:**] votes are distributed between {df.shape[0]} \
                candidates. The most votes (*{max_votes}*) has \
                    {', '.join(df[df['number_voters'] == max_votes]['candidate'].values)}. The least \
                    (*{min_votes}*) — {', '.join(df[df['number_voters'] == min_votes]['candidate'].values)}.")
    

    # 4. What is the cumulative vote percentage by candidate rank?
    st.info(f":orange[What is the cumulative vote percentage by candidate rank?]")
    df['cum_percent'] = df['percent_voters'].cumsum()
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['candidate'],
        y=df['percent_voters'],
        name='Percentage of votes per candidate',
        marker=dict(color='maroon'),
        yaxis='y1'
    ))

    fig.add_trace(go.Scatter(
        x=df['candidate'],
        y=df['cum_percent'],
        name='Cumulative % of votes',
        yaxis='y2',
        mode='lines+markers',
        marker=dict(color='red')
    ))


    fig.update_layout(
        yaxis=dict(
            title='Total Percent of Votes Candidate Received',
            side='left'
        ),
        yaxis2=dict(
            title='Cumulative % of Votes',
            overlaying='y',
            side='right',
            range=[0, 110]
        )
    )

    st.plotly_chart(fig)

    # 5. What is the drop-off in number of voters between each ranked candidate?
    st.info(f":orange[What is the drop-off in number of voters between each ranked candidate?]")
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df['candidate'], y=df['number_voters'], 
                   mode='lines+markers',
                   marker=dict(color='red'), 
                   name='Drop-off in number of voters between each ranked candidate')
    )

    st.plotly_chart(fig)

    # 6. What portion of total votes went to candidates with <5% support?
    st.info(f":orange[What portion of total votes went to candidates with <5% support?]")
    fig = go.Figure()

    above_5 = df[df['percent_voters'] >= 5.0]

    # >= 5.0%
    fig.add_trace(go.Bar(
        x=above_5['candidate'],
        y=above_5['percent_voters'],
        name='>= 5% support',
        marker_color='green'
    ))
    
    below_5 = df[df['percent_voters'] < 5.0]
    # < 5.0%
    fig.add_trace(go.Bar(
        x=below_5['candidate'],
        y=below_5['percent_voters'],
        name='< 5% support',
        marker_color='red '
    ))

    fig.update_layout(
        title='Candidates by Vote Percentage: Above and Below 5%',
        xaxis_title='Candidate',
        yaxis_title='% of Voters',
        barmode='group',
        xaxis_tickangle=-45,
        height=600
    )

    st.plotly_chart(fig)
    
    st.markdown(f":orange[**Answer:**] The portion of votes went to candidates \
                with <5% support is (*{below_5['number_voters'].sum()}*) \
                    {below_5.shape[0] / df.shape[0]:.2f}%")
