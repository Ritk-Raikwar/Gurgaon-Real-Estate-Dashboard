import streamlit as st
import pandas as pd
import numpy as np
import joblib
import re

# --- Page Configuration ---
st.set_page_config(
    page_title="Real Estate Recommender",
    page_icon="🏠",
    layout="wide"
)

# --- Load Data and Models ---
@st.cache_resource
def load_data():
    """
    Loads all the pre-processed data files and similarity matrices.
    Using st.cache_resource to avoid reloading these large files on each interaction.
    """
    try:
        df = joblib.load('data/df_processed.pkl')
        cosine_sim_facilities = joblib.load('data/cosine_sim_facilities.pkl')
        cosine_sim_price = joblib.load('data/cosine_sim_price.pkl')
        cosine_sim_location = joblib.load('data/cosine_sim_location.pkl')
        return df, cosine_sim_facilities, cosine_sim_price, cosine_sim_location
    except FileNotFoundError:
        st.error("Processed data files not found. Please ensure 'df_processed.pkl', 'cosine_sim_facilities.pkl', 'cosine_sim_price.pkl', and 'cosine_sim_location.pkl' are in the same directory as your home.py file.")
        return None, None, None, None

df, cosine_sim_facilities, cosine_sim_price, cosine_sim_location = load_data()

if df is not None:
    # Create a mapping from property name to its integer index
    indices = pd.Series(df.index, index=df['PropertyName'])

# --- UI Layout ---
st.title("🏡 Society Recommender System")
st.markdown("""
This is a two-level recommender system. 
1.  **First**, filter society by selecting a specific sector.
2.  **Second**, adjust the weights for different features to get personalized recommendations for a selected society.
""")

# --- Level 1: Location-based Filtering ---
st.header("Level 1: Location-based Filtering")

if df is not None:
    # Get unique sectors, sort them, and add an 'Overall Gurgaon' option
    unique_sectors = sorted(df['sector'].unique())
    if 'Unknown' in unique_sectors:
        unique_sectors.remove('Unknown')
    location_options = ['Overall Gurgaon'] + unique_sectors
    selected_location = st.selectbox("Select a Sector/Location to browse society:", location_options)

    # Filter dataframe based on the selected sector
    if selected_location == 'Overall Gurgaon':
        filtered_df = df
    else:
        filtered_df = df[df['sector'] == selected_location]

    st.info(f"Found **{len(filtered_df)}** society in **{selected_location}**.")

    # --- Level 2: Feature-based Recommendation ---
    if not filtered_df.empty:
        st.header("Level 2: Feature-based Recommendation")
        
        # Get property names from the filtered dataframe
        property_list = filtered_df['PropertyName'].tolist()
        selected_property = st.selectbox("Select a Property to get recommendations for:", property_list)

        st.subheader("Adjust Feature Weights")
        st.markdown("Use the sliders below to specify how important each feature is for your recommendation.")
        
        w_col1, w_col2, w_col3 = st.columns(3)
        with w_col1:
            w_facilities = st.slider("Importance of Amenities/Facilities", 0, 100, 33)
        with w_col2:
            w_price = st.slider("Importance of Price/Area/Type", 0, 100, 33)
        with w_col3:
            w_location = st.slider("Importance of Nearby Locations", 0, 100, 34)

        if st.button("Get Recommendations", type="primary"):
            if selected_property:
                try:
                    # Get the index of the selected property
                    idx = indices[selected_property]

                    # Get the similarity scores for the selected property from each matrix
                    sim_scores_facilities = list(enumerate(cosine_sim_facilities[idx]))
                    sim_scores_price = list(enumerate(cosine_sim_price[idx]))
                    sim_scores_location = list(enumerate(cosine_sim_location[idx]))

                    # Combine scores with weights
                    # We normalize weights to sum to 1 to keep scores comparable
                    total_weight = w_facilities + w_price + w_location
                    if total_weight == 0:
                        st.warning("Please set at least one weight above zero.")
                    else:
                        # Calculate weighted average score for all properties
                        final_scores = []
                        for i in range(len(df)):
                            weighted_score = (w_facilities * sim_scores_facilities[i][1] + 
                                              w_price * sim_scores_price[i][1] + 
                                              w_location * sim_scores_location[i][1]) / total_weight
                            final_scores.append((i, weighted_score))

                        # Filter scores to only include properties from the location-filtered list
                        filtered_indices = indices[filtered_df['PropertyName']].tolist()
                        
                        # Exclude the selected property itself from the recommendations
                        if idx in filtered_indices:
                            filtered_indices.remove(idx)

                        filtered_final_scores = [(i, score) for i, score in final_scores if i in filtered_indices]

                        # Sort the filtered properties based on the final score
                        sorted_scores = sorted(filtered_final_scores, key=lambda x: x[1], reverse=True)

                        # Get the top 5 recommendations
                        top_5_recommendations = sorted_scores[:5]
                        top_indices = [i[0] for i in top_5_recommendations]
                        
                        st.success("Here are your top 5 recommendations:")
                        
                        # Display results in columns
                        if top_indices:
                            num_results = len(top_indices)
                            result_cols = st.columns(num_results)
                            for i, rec_idx in enumerate(top_indices):
                                with result_cols[i]:
                                    prop_details = df.iloc[rec_idx]
                                    st.markdown(f"**{i+1}. {prop_details['PropertyName']}**")
                                    st.markdown(f"*{prop_details['PropertySubName']}*")
                                    st.link_button("View Details", prop_details['Link'])
                        else:
                            st.warning("No other similar properties found in the selected location.")
                            
                except KeyError:
                    st.error("Could not find the selected property. Please try another one.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    else:
        st.warning("No properties found in this sector. Please select another one.")

