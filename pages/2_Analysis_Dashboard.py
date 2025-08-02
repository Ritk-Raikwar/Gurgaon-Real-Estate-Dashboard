import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import ast

# Set the title and layout for the Streamlit page
st.set_page_config(page_title="Gurgaon Property Analysis", layout="wide")

st.title("Gurgaon Property Analysis Dashboard")

# --- File Paths ---
# This script assumes the following files are in the same root directory (CORE/).
PROPERTIES_CSV = 'data/gurgaon_properties_missing_value_imputation.csv'
COORDINATES_CSV = 'data/gurgaon_sectors_lat_long.csv'
PROPERTIES_RAW_CSV = 'data/gurgaon_properties.csv'

# --- Load Data ---
# Use st.cache_data to load data only once to improve performance
@st.cache_data
def load_data():
    """Loads all necessary data files."""
    try:
        props_df = pd.read_csv(PROPERTIES_CSV)
        coords_df = pd.read_csv(COORDINATES_CSV)
        props_raw_df = pd.read_csv(PROPERTIES_RAW_CSV)
        
        # Merge to get the 'features' column into the main dataframe
        # Using a left merge to keep all properties from the main cleaned file
        wordcloud_df = pd.merge(props_df, props_raw_df[['society', 'features']], on='society', how='left')
        
        return props_df, coords_df, wordcloud_df
    except FileNotFoundError as e:
        st.error(f"Error: A required data file was not found.")
        st.info(f"Details: {e}. Please make sure '{PROPERTIES_CSV}', '{COORDINATES_CSV}', and '{PROPERTIES_RAW_CSV}' are in your project's root directory.")
        return None, None, None

props_df, coords_df, wordcloud_base_df = load_data()

# --- Main App Logic ---
if all(df is not None for df in [props_df, coords_df, wordcloud_base_df]):
    
    # --- Sidebar for User Input ---
    st.sidebar.header("Global Filters")

    # Property type filter
    property_type = st.sidebar.selectbox(
        'Select Property Type',
        ('Both', 'House', 'Flat'),
        key='property_type_filter'
    )

    # Sector filter
    sector_list = ['Overall'] + sorted(props_df['sector'].dropna().unique().tolist())
    selected_sector = st.sidebar.selectbox('Select a Sector', sector_list, key='sector_filter')

    # --- Main Data Filtering based on sidebar selections ---
    display_df = props_df.copy()
    
    # Apply property type filter
    if property_type != 'Both':
        display_df = display_df[display_df['property_type'] == property_type.lower()]

    # Apply sector filter
    if selected_sector != 'Overall':
        display_df = display_df[display_df['sector'] == selected_sector]

    # --- Visualization Selector ---
    st.sidebar.header("Select a Visualization")
    viz_choice = st.sidebar.radio(
        "Choose a chart:",
        (
            'Sector Map Analysis', 
            'Area vs. Price Analysis', 
            'BHK Price Distribution', 
            'Property Type Distribution', 
            'Price Distribution by Type',
            'Common Amenities (Word Cloud)'
        )
    )

    # --- Display Selected Visualization ---

    if viz_choice == 'Sector Map Analysis':
        st.header("Sector-wise Property Analysis Map")
        st.write(
            "This interactive map visualizes Gurgaon's real estate market. "
            "The **color** of each point represents the average price per square foot, "
            "and the **size** of the point represents the average built-up area for that sector."
        )
        
        # NOTE: The global sector filter is ignored for this map as it shows an overview of all sectors.
        # However, the property type filter is applied.
        
        # Data processing for the map
        map_df = props_df.copy()
        if property_type != 'Both':
            map_df = map_df[map_df['property_type'] == property_type.lower()]

        map_df['sector'] = map_df['sector'].str.lower().str.strip()
        group_df = map_df.groupby('sector').agg({
            'price_per_sqft': 'mean',
            'built_up_area': 'mean'
        }).reset_index()

        coords_df_renamed = coords_df.rename(columns={'sector_name': 'sector', 'log': 'longitude', 'lat': 'latitude'})
        merged_df = pd.merge(group_df, coords_df_renamed, on='sector', how='inner')
        merged_df.dropna(subset=['latitude', 'longitude'], inplace=True)

        if not merged_df.empty:
            fig_map = px.scatter_mapbox(
                merged_df,
                lat="latitude",
                lon="longitude",
                color="price_per_sqft",
                size='built_up_area',
                color_continuous_scale=px.colors.cyclical.IceFire,
                zoom=10,
                mapbox_style="open-street-map",
                text='sector',
                hover_name='sector',
                hover_data={'price_per_sqft': ':.2f', 'built_up_area': ':.2f'},
                title=f"Gurgaon Property Analysis for {property_type} Properties"
            )
            fig_map.update_layout(
                margin={"r": 0, "t": 40, "l": 0, "b": 0},
                title={'x': 0.5, 'xanchor': 'center'}
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("No data to display for the selected filter.")

    elif viz_choice == 'Area vs. Price Analysis':
        st.header("Area vs. Price Scatter Plot")
        st.write(f"Showing relationship between built-up area and price for **{property_type}** properties in **{selected_sector}**.")
        
        if not display_df.empty:
            fig_scatter = px.scatter(
                display_df, 
                x="built_up_area", 
                y="price", 
                color="bedRoom", 
                title=f"Area Vs Price in {selected_sector} for {property_type}"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("No data available for the selected filters.")

    elif viz_choice == 'BHK Price Distribution':
        st.header("BHK Price Range Box Plot")
        st.write(f"Price distribution by number of bedrooms for **{property_type}** properties in **{selected_sector}**.")
        
        if not display_df.empty:
            temp_df = display_df[display_df['bedRoom'] <= 4]
            fig_box = px.box(
                temp_df, 
                x='bedRoom', 
                y='price', 
                title=f'BHK Price Range in {selected_sector} for {property_type}'
            )
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.warning("No data available for the selected filters.")

    elif viz_choice == 'Property Type Distribution':
        st.header("Property Type and Bedroom Distribution")
        st.write(f"Hierarchical view of properties in **{selected_sector}**.")

        if not display_df.empty:
            fig_sunburst = px.sunburst(
                display_df.dropna(subset=['bedRoom']),
                path=['property_type', 'bedRoom'],
                values='price',
                title=f"Distribution for {selected_sector}"
            )
            st.plotly_chart(fig_sunburst, use_container_width=True)
        else:
            st.warning("No data available for the selected filters.")

    elif viz_choice == 'Price Distribution by Type':
        st.header("Price Distribution for Houses vs. Flats")
        st.write(f"Comparing price distributions in **{selected_sector}**.")

        if not display_df.empty:
            # For this chart, we want to compare house vs flat, so the property_type filter is ignored if it's not 'Both'
            df_for_dist = props_df.copy()
            if selected_sector != 'Overall':
                df_for_dist = df_for_dist[df_for_dist['sector'] == selected_sector]

            house_prices = df_for_dist[df_for_dist['property_type'] == 'house']['price']
            flat_prices = df_for_dist[df_for_dist['property_type'] == 'flat']['price']
            
            hist_data = []
            group_labels = []
            if not house_prices.empty:
                hist_data.append(house_prices)
                group_labels.append('House')
            if not flat_prices.empty:
                hist_data.append(flat_prices)
                group_labels.append('Flat')

            if hist_data:
                fig_dist = ff.create_distplot(hist_data, group_labels, show_hist=False, show_rug=False)
                fig_dist.update_layout(title_text=f'Price Distribution in {selected_sector}')
                st.plotly_chart(fig_dist, use_container_width=True)
            else:
                st.warning("No data to display for the selected filters.")
        else:
            st.warning("No data available for the selected filters.")
            
    elif viz_choice == 'Common Amenities (Word Cloud)':
        st.header("Most Common Property Features")
        st.write(f"This word cloud highlights the most frequently mentioned features in property listings for **{selected_sector}**.")

        # Use the globally filtered dataframe for the word cloud
        temp_wordcloud_df = wordcloud_base_df.copy()
        temp_wordcloud_df['features'] = temp_wordcloud_df['features'].fillna('[]')
        
        if property_type != 'Both':
            temp_wordcloud_df = temp_wordcloud_df[temp_wordcloud_df['property_type'] == property_type.lower()]
        if selected_sector != 'Overall':
            temp_wordcloud_df = temp_wordcloud_df[temp_wordcloud_df['sector'] == selected_sector]

        def safe_literal_eval(val):
            try:
                return ast.literal_eval(val)
            except (ValueError, SyntaxError):
                return []

        # Check if the 'features' column exists before processing
        if 'features' in temp_wordcloud_df.columns:
            features_list = [item for sublist in temp_wordcloud_df['features'].apply(safe_literal_eval) for item in sublist]
            feature_text = ' '.join(features_list)

            if feature_text:
                wordcloud = WordCloud(width=800, height=400,
                                      background_color='white',
                                      stopwords=set(['s']),
                                      min_font_size=10).generate(feature_text)

                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")
                st.pyplot(fig)
            else:
                st.warning(f"No features data available for the selected filters to generate a word cloud.")
        else:
            st.warning("The 'features' column is not available in the dataset.")
