import pandas as pd
import streamlit as st
import plotly.express as px

# Load the data
def load_data():
    return pd.read_csv('streamlitdata.csv')

def main():
    # Set the page title
    st.title("Malaysia Invasive Plant Species Distribution Dashboard")
    
    # Load the data
    df = load_data()

    # Sidebar - Species selection for Distribution Map and Species Count
    st.sidebar.subheader("Select Species for Distribution Map")
    species_list = df['scientific_name'].unique()
    selected_species = st.sidebar.multiselect('Select Species', species_list, species_list)

    # Sidebar - Data Summary
    st.sidebar.subheader("Data Summary")
    st.sidebar.write(f"Total species: {df['scientific_name'].nunique()}")
    st.sidebar.write(f"Total locations: {df[['latitude', 'longitude']].drop_duplicates().shape[0]}")
    st.sidebar.write(f"Total records: {df.shape[0]}")

    # Sidebar - Species selection for Comparison Map (2 to 8 species)
    st.sidebar.subheader("Select Species for Comparison Map")
    selected_comparison_species = st.sidebar.multiselect('Select Species to Compare', species_list, species_list[:2], max_selections=8)

    # Sidebar - Species selection for Density Heatmap
    st.sidebar.subheader("Select Species for Density Heatmap")
    selected_heatmap_species = st.sidebar.selectbox('Select Species', species_list)

    # Filter function
    filtered_df = df[df['scientific_name'].isin(selected_species)]

    # Check if the filtered DataFrame is not empty
    if filtered_df.empty:
        st.warning("No data available for the selected species.")
    else:
        # Set your Mapbox access token
        px.set_mapbox_access_token("your_actual_mapbox_access_token")

        # Species Distribution Map
        st.subheader("Species Distribution Map")
        fig = px.scatter_mapbox(
            filtered_df, 
            lat='latitude', 
            lon='longitude', 
            color='scientific_name',
            hover_name='common_name',
            hover_data={'latitude': True, 'longitude': True},
            zoom=5,
            height=600,
            title="Species Distribution Map"
        )
        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig)
        
        # Species Comparison Map
        if len(selected_comparison_species) >= 2:
            st.subheader("Species Comparison Map")
            comparison_df = df[df['scientific_name'].isin(selected_comparison_species)]
            fig_compare = px.scatter_mapbox(
                comparison_df, 
                lat='latitude', 
                lon='longitude', 
                color='scientific_name',
                hover_name='common_name',
                hover_data={'latitude': True, 'longitude': True},
                zoom=5,
                height=600,
                title="Species Comparison Map"
            )
            fig_compare.update_layout(mapbox_style="carto-positron")
            st.plotly_chart(fig_compare)

        # Density Heatmap
        st.subheader("Species Density Heatmap")
        if selected_heatmap_species:
            species_df = df[df['scientific_name'] == selected_heatmap_species]
            heatmap_df = species_df[['latitude', 'longitude']]
            fig_heatmap = px.density_mapbox(
                heatmap_df, 
                lat='latitude', 
                lon='longitude',
                radius=10,
                zoom=5,
                height=600,
                title=f"{selected_heatmap_species} Density Heatmap"
            )
            fig_heatmap.update_layout(mapbox_style="stamen-toner")
            st.plotly_chart(fig_heatmap)

    # Species Count by Location
    if not filtered_df.empty:
        st.subheader("Species Count by Location")
        species_count = filtered_df.groupby('scientific_name').size().reset_index(name='counts')
        species_bar_chart = px.bar(species_count, x='scientific_name', y='counts', title='Species Count')
        st.plotly_chart(species_bar_chart)

if __name__ == "__main__":
    main()
