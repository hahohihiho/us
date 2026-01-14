import pandas as pd
import plotly.express as px
import streamlit as st

# dashboard page and title creation
st.set_page_config(page_title="Agricaltural Exports - US 2011", page_icon=":seedling:", layout="wide")
st.title(":seedling: US Agricaltural Exports in 2011")

# data import and prep
link = "https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv"
df = pd.read_csv(link)

df.drop("category", axis=1, inplace=True)
df.rename(columns={'total fruits':'fruits', 'total veggies':'veggies', 'total exports': 'total'}, inplace=True)

# list of categories
categories = ['beef', 'pork', 'poultry', 'dairy', 'fruits', 'veggies', 'corn', 'wheat', 'cotton']

# creating misc. category
df['misc.'] = df['total'] - df[categories].sum(axis=1)
categories.append('misc.')

# Create a new list of categories with 'total exports' as the first element
choropleth_categories = ['total'] + categories
# melting the data to a long format 
df_cat = pd.melt(frame=df, id_vars=['code', 'state'], 
                 value_vars=categories, var_name='category', value_name='export')

# Sidebar for choropleth category selection
st.sidebar.header("Filter Data by Export Category: ")

# Filter functionality for choropleth using a select box in the side bar
choropleth_category = st.sidebar.selectbox("Select Category for Choropleth Map:",
                                            choropleth_categories,
                                            index=0  # this is my default setting; first element is total imports
                                          )

# figure 1: total exports by state in a choropleth

# create a title for the first figure
st.subheader(f"US Exports by State in Million USD - {choropleth_category.title()}")

st.download_button(label="Download Raw Data", data=df.to_csv(), file_name='us_ag_2011_data.csv')

# create the choropleth figure
fig = px.choropleth(data_frame=df,
                    locationmode='USA-states',
                    locations='code',
                    scope="usa",
                    color=choropleth_category,
                    hover_name="state",
                    hover_data= choropleth_category,
                    color_continuous_scale=px.colors.sequential.algae,
                    width=1700,
                    height=800
                    )

# creating a dynamic title
coro_title = choropleth_category.title()+' Exports in Million USD'

# customization of choropleth color bar
fig.update_layout(coloraxis_colorbar= dict(title=coro_title, len=0.7, thickness=50))

# display figure in dashboard
st.plotly_chart(fig, use_container_width=True)

# Create a new list of states with 'All States' as the first element
#df.sort_values('code', inplace=True) # just sorting alphabetically acc. to state
states = ['All States'] + df['state'].tolist()

# Add another side bar header
st.sidebar.header("Filter Data by State(s): ")

# Add multi-select filter for states
state_list = st.sidebar.multiselect("Choose State(s) for Bar and Donut Charts", options=states, 
                                    default=['All States'])

# logic for the state selection
if state_list==['All States']:
    df_states=df.copy()
    df_cat_states = df_cat.copy()
else:
    df_states=df.loc[df["state"].isin(state_list)]
    df_cat_states = df_cat.loc[df_cat['state'].isin(state_list)]
    
df_states.sort_values('total', ascending=False, inplace=True) # sorting for the bar chart

# dasboard columns creation
col1, col2 = st.columns((2))


# Figure 2: total exports by state in a bar chart for chosen states
with col1:

    formatted_states = ", ".join(state_list)
    st.subheader("Total Exports - "+formatted_states)
    
    fig=px.bar(data_frame=df_states, x='code', y="total", hover_name="state",
               color_continuous_scale=px.colors.sequential.algae,
               color="total",
               labels={'code': 'State', 'total':'Total Exports in Million USD'},
               height=500)
    st.plotly_chart(fig, use_container_width=True)

# Figure 3: categories breakdown for chosen states
with col2:
    st.subheader("Categories Breakdown - "+formatted_states)
    cat_states_agg = df_cat_states.groupby("category")[['export']].sum().reset_index()
    
    fig = px.pie(data_frame=cat_states_agg, names='category', values='export', 
             color='category', color_discrete_sequence=px.colors.qualitative.Prism,               
             hole=0.4,
             height=500, width=500)

    # Set the legend title
    fig.update_layout(legend_title=dict(text="Export Categories"))

    st.plotly_chart(fig, use_container_width=False)


# Sidebar for choropleth category selection
st.sidebar.header("Filter Data by Export Category: ")


