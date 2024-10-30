import streamlit as st
import plotly_express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
st.set_page_config(page_title='IndiaInFigures',page_icon=":bar_chart:",layout="wide")
st.title(" :bar_chart: IndiaInFigures")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)

census = pd.read_csv('census2011.csv')
# census.set_index('State',inplace=True)
list_of_states = list(census['State'].unique())
list_of_states.insert(0,'Overall India')

st.sidebar.header("Select Parameters")
state_selected = st.sidebar.multiselect("Select State Or Country",list_of_states)

if not state_selected:
    pass
else:
    if 'Overall India' in state_selected:
        state_df = census
    else: 
        state_df = census[census.State.isin(state_selected)].copy()

    district_selected = st.sidebar.multiselect("Select District",state_df.District.unique())

    if district_selected:
        district_df = state_df[state_df.District.isin(district_selected)].copy()
    else:
        district_df = state_df
    col_parameter,col_map = st.columns([1,5])
    # button = st.sidebar.button('Show Details')

    with col_parameter:
        parameter = st.selectbox('Select a Parameter',[
        'Population', 'Literates','Illiterates','Workers',
        'Electricty', 'Internet',
        'Secondary Education','Higher Education', 'Graduates',
        'Radios','Mobiles',  'Television',
        'Latrine facilities', 'No Latrine Facilities',
        'Drinking Water Within Household','Tapwater','DrinkingWater Source Far From Home', 
        '1-2 members','3-5 members',
        'Fuel','Lpg cylindar',
        'SC','ST','Total_minority'
        ])
    with col_map:
        fig = px.scatter_mapbox(state_df, lat="Latitude", lon="Longitude", size=parameter, color='District', zoom=6,size_max=35,
                                mapbox_style="carto-positron",hover_name='District')
        fig.update_layout(title={
            'text': "India On Map<br>Size of dot represents a parameter",  # Bold formatting in Markdown
            'x': 0.5,  # Center align title
            'xanchor': 'center'
        },width=1200,height=700)
        st.plotly_chart(fig,use_container_width=True)
    

    col1,col2,col3 = st.columns(3)
    with col1:
        st.subheader('Male vs Female Population')
        df = district_df[['Male','Female','Male_Literate','Female_Literate']].copy().sum()
        fig = px.pie(df,values=df.values[:2])
        fig.update_traces(marker=dict(colors=['blue','Red']),text = df.index.values[:2], textposition = "inside")
        fig.update_layout(width = 500, height = 350)
        st.plotly_chart(fig,use_container_width=True)



    with col2:
        st.subheader('Male vs Female Literacy')

        fig = px.bar(df,y = df.values[2:],x = df.index.values[2:],labels={'x':'','y':'population'})
        fig.update(layout_showlegend=False)
        fig.update_layout(width = 400, height = 300)
        fig.update_traces(marker=dict(color=['blue','Red']),width=0.6)
        st.plotly_chart(fig,use_container_width=True)
    with col3:

        st.subheader('Workers Male vs Female')
        df = census[census.District.isin(['Banka','Araria'])][['Male workers', 'Female workers']]
        df = df.sum()
        fig = px.pie(df,values=df.values)
        fig.update_traces(marker=dict(colors=['blue','Red']),text = df.index.values[:2], textposition = "inside")
        fig.update_layout(width = 500, height = 350)
        st.plotly_chart(fig,use_container_width=True)

    col_a,col_b = st.columns(2)
    with col_a:
        st.subheader('Literacy among States')
        fig = px.treemap(state_df,path=['State','District'],values='Literate')
        #fig = px.scatter(state_df,x = 'Latitude',y='Longitude',color='District',size='Literate',labels={'Latitude':'','Longitude':''})
        fig.update_layout(width=500,height=500)
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        st.subheader('Illiteracy among States')
        #fig = px.scatter(state_df,x = 'Latitude',y='Longitude',color='District',size='Illiterates',labels={'Latitude':'','Longitude':''})
        fig = px.sunburst(state_df,path=['State','District'],values='Illiterates')
        fig.update_layout(width=300,height=480)
        st.plotly_chart(fig, use_container_width=True)
    st.subheader('Education among people in states')
    col4,col5,col6 = st.columns([1.3,1,1.8])

    with col4:
    
        df = district_df[['Secondary Education','Higher Education','Total Educated']].sum()

        fig = px.bar(df,x=df.index,y=df.values,color=df.index,labels={'index':'','y':'Population'},log_y=True,title='Secondary vs Higher Education')
        fig.update(layout_showlegend=False)
        fig.update_layout(width = 500, height = 450)
        st.plotly_chart(fig,use_container_width=True)
    with col5:


        fig = px.sunburst(district_df,path=['State','District'],values='Total Educated')
        fig.update_layout(title={
            'text': "Total Educated among states<br>select multiple districts to compare",  # Bold formatting in Markdown
            'x': 0.5,  # Center align title
            'xanchor': 'center'
        },width = 500, height = 450)
        st.plotly_chart(fig,use_container_width=True)
    with col6:
        
        
        fig = px.scatter(state_df,x='Latitude',y='Longitude',color='District',size='Secondary - Higher',
                        labels={'Latitude':'','Longitude':''})
        #fig = px.treemap(state_df,path=['State','District'],values='Secondary - Higher')
        #fig.update(layout_showlegend=False)

        fig.update_layout(title={
            'text': "Districts where people have done <br> Secondary Education but not Higher Education",  # Bold formatting in Markdown
            'x': 0.5,  # Center align title
            'xanchor': 'center'
        },width = 500, height = 450)
        st.plotly_chart(fig,use_container_width=True)

    with st.container():
        # st.subheader('Religion Graph')
        religion = district_df[['Hindus',
        'Muslims',
        'Christians',
        'Sikhs',
        'Buddhists',
        'Jains',
        'Others_Religions']].sum()
        fig = px.bar(religion,color=religion.index,log_y=True,labels = {"index": "","value":'population'},title='Religion Practices')
        fig.update(layout_showlegend=False)
        st.plotly_chart(fig,use_container_width=True)

    col8,col9,col10 = st.columns(3)
    with col8:
        df = district_df[['Male Minority', 'Female Minority']].sum()
        fig = px.pie(df,values=df.values,title='Male vs Female Minority')
        fig.update_traces(marker=dict(colors=['blue','Red']),text = df.index.values, textposition = "inside")
        fig.update_layout(width = 300, height = 420)
        st.plotly_chart(fig,use_container_width=True)
    with col9:
    

        fig = px.treemap(state_df,path = ['State','District'],values = 'Total_minority',hover_data=['Population'])
        fig.update_layout(title={
            'text':'Tribal caste among states',  # Bold formatting in Markdown
            'x': 0.5,  # Center align title
            'xanchor': 'center'
        },width = 900, height = 420)
        st.plotly_chart(fig,use_container_width=True)
    with col10:
        df = district_df[['ST','SC','Population']].sum()

        fig = px.bar(df,x = df.index,y = df.values,labels = {'index':'caste','y':'population'},log_y=True,color=df.index,title='Tribal caste')
        fig.update(layout_showlegend=False)
        fig.update_layout(width = 300, height = 350)
        st.plotly_chart(fig,use_container_width=True)

    col11,col12,col13 = st.columns([2,2,3])
    with col11:
        df = district_df[['Electricty','Mobiles','Television','Radios','Internet']].sum()

        fig = px.bar(df,x = df.index,y = df.values,labels = {'index':'','y':'Households'},log_y=True,color=df.index,title='Utilities')
        fig.update(layout_showlegend=False)
        fig.update_layout(width = 300, height = 350)
        st.plotly_chart(fig,use_container_width=True)
    with col12:
        df = district_df[['Latrine facilities', 'No Latrine Facilities']].sum()

        fig = px.pie(df,values=df.values,color=df.index,title='Latrine Facilities')
        fig.update_traces(marker=dict(colors=['#C5B9B9','black']),text = df.index.values, textposition = "inside")
        fig.update_layout(width = 300, height = 420)
        st.plotly_chart(fig,use_container_width=True)
    with col13:
        df= district_df[['wells',
        'Handpump Tubewell Borewell', 'Spring water', 'Canal',
        'Other Sources of Water', 'Drinking Water Near Household',
        'Drinking Water Within Household', 'Watertank Pond Lakes', 'Tapwater',
        'DrinkingWater Source Far From Home']].sum()
        fig = px.bar(df,x=df.index,y=df.values,labels = {'index':'','y':'Households'},color=df.index,title='Water Sources')
        fig.update(layout_showlegend=False)
        fig.update_layout(width = 300, height = 500)
        st.plotly_chart(fig,use_container_width=True)