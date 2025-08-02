import joblib
import numpy as np
import pandas as pd
import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Gurgaon Property Price Predictor",
    page_icon="💲",
    layout="wide"
)

# --- Load All Necessary Files ---
@st.cache_resource
def load_assets():
    """Loads all necessary files for the app to function."""
    try:
        model = joblib.load('data/gurgaon_property_prediction_pipeline.joblib')
        sector_map = joblib.load('data/sector_map.joblib')
        df = joblib.load('data/X_dataframe.joblib')
        return model, sector_map, df
    except FileNotFoundError:
        st.error("Model or necessary data files not found. Please ensure all .joblib files are in the root directory.")
        return None, None, None

model, sector_map, df = load_assets()

# --- Main App UI ---
st.title("Gurgaon Property Price Predictor")
st.markdown("Enter the details of the property to get an estimated price.")

if df is not None:
    # --- Create Input Widgets in Columns ---
    st.header("Property Details")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Location & Type")
        property_type = st.selectbox('Property Type', df['property_type'].unique())
        sector = st.selectbox('Sector', sorted(sector_map.index.tolist()))
        agePossession = st.selectbox('Age of Possession', sorted(df['agePossession'].unique().tolist()))

    with col2:
        st.subheader("Rooms & Area")
        bedRoom = st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist()))
        bathroom = st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist()))
        built_up_area = st.number_input('Built-up Area (sq. ft.)', min_value=500, max_value=20000, value=1500)

    with col3:
        st.subheader("Amenities & Furnishing")
        balcony = st.selectbox('Number of Balconies', sorted(df['balcony'].unique().tolist()))
        servant_room = st.selectbox('Servant Room', ['Yes', 'No'])
        store_room = st.selectbox('Store Room', ['Yes', 'No'])
        furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
        luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
        floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

    # --- Prediction Logic ---
    if st.button('Predict Price', type="primary"):
        # Convert Yes/No to 1/0
        servant_room_num = 1 if servant_room == 'Yes' else 0
        store_room_num = 1 if store_room == 'Yes' else 0

        # 1. Create the base DataFrame from user inputs
        input_dict = {
            'property_type': [property_type], 'bedRoom': [bedRoom], 'bathroom': [bathroom],
            'balcony': [balcony], 'agePossession': [agePossession], 'built_up_area': [built_up_area],
            'servant room': [servant_room_num], 'store room': [store_room_num],
            'furnishing_type': [furnishing_type], 'luxury_category': [luxury_category],
            'floor_category': [floor_category]
        }
        input_df = pd.DataFrame(input_dict)

        # 2. Engineer the NEW features exactly as in the training script
        input_df['sector_score'] = sector_map.get(sector, 0)
        input_df['area_x_sector_score'] = input_df['built_up_area'] * input_df['sector_score']
        input_df['area_x_room'] = input_df['built_up_area'] / (input_df['bedRoom'] + 1)
        input_df['bed_bath_ratio'] = input_df['bedRoom'] / (input_df['bathroom'] + 1)

        # 3. Ensure column order is the same as the training data
        final_cols = ['property_type', 'bedRoom', 'bathroom', 'balcony', 'agePossession',
                      'built_up_area', 'servant room', 'store room', 'furnishing_type',
                      'luxury_category', 'floor_category', 'sector_score',
                      'area_x_sector_score', 'area_x_room', 'bed_bath_ratio']
        
        input_final_df = input_df[final_cols]

        # 4. Predict
        try:
            predicted_log_price = model.predict(input_final_df)
            predicted_price = np.expm1(predicted_log_price)[0]

            # Display the result in a more prominent way
            st.subheader("Predicted Price")
            st.markdown(f"<h2 style='text-align: center; color: #28a745;'>₹ {predicted_price:,.2f}</h2>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")





# import joblib
# import numpy as np
# import pandas as pd
# import streamlit as st

# # --- Load All Necessary Files ---
# # Make sure these files are in the same directory as your Streamlit app
# try:
#     # Load the trained pipeline
#     model = joblib.load('gurgaon_property_prediction_pipeline.joblib')
#     # Load the sector mapping created during training
#     sector_map = joblib.load('sector_map.joblib')
#     # Load the base dataframe to get unique values for dropdowns
#     df = joblib.load('X_dataframe.joblib')
# except FileNotFoundError:
#     st.error("Model or necessary data files not found. Please run the training script first.")
#     st.stop()


# st.header('Enter the details of the property')

# # --- Create Input Widgets ---
# # property_type
# property_type = st.selectbox('Property Type', df['property_type'].unique())

# # sector
# sector = st.selectbox('Sector', sorted(sector_map.index.tolist())) # Use sector_map for sector list

# # bedRoom
# bedRoom = st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist()))

# # bathroom
# bathroom = st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist()))

# # balcony
# balcony = st.selectbox('Number of Balconies', sorted(df['balcony'].unique().tolist()))

# # agePossession
# agePossession = st.selectbox('Age of Possession', sorted(df['agePossession'].unique().tolist()))

# # built_up_area
# built_up_area = st.number_input('Built-up Area (sq. ft.)', min_value=500, max_value=20000, value=1500)

# # servant room
# servant_room = st.selectbox('Servant Room', ['Yes', 'No'])

# # store room
# store_room = st.selectbox('Store Room', ['Yes', 'No'])

# # furnishing_type
# furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))

# # luxury_category
# luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))

# # floor_category
# floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

# # --- Prediction Logic ---
# if st.button('Predict Price'):
#     # Convert Yes/No to 1/0
#     servant_room_num = 1 if servant_room == 'Yes' else 0
#     store_room_num = 1 if store_room == 'Yes' else 0

#     # --- 1. Create the base DataFrame from user inputs ---
#     # This must match the columns used in the training script BEFORE new features were made
#     input_dict = {
#         'property_type': [property_type],
#         'bedRoom': [bedRoom],
#         'bathroom': [bathroom],
#         'balcony': [balcony],
#         'agePossession': [agePossession],
#         'built_up_area': [built_up_area],
#         'servant room': [servant_room_num],
#         'store room': [store_room_num],
#         'furnishing_type': [furnishing_type],
#         'luxury_category': [luxury_category],
#         'floor_category': [floor_category]
#     }
#     input_df = pd.DataFrame(input_dict)

#     # --- 2. Engineer the NEW features exactly as in the training script ---
#     # Use the loaded sector_map to get the score for the selected sector
#     input_df['sector_score'] = sector_map.get(sector, 0) # Use 0 as default if sector not found

#     # Create the interaction features
#     input_df['area_x_sector_score'] = input_df['built_up_area'] * input_df['sector_score']
#     input_df['area_x_room'] = input_df['built_up_area'] / (input_df['bedRoom'] + 1)
#     input_df['bed_bath_ratio'] = input_df['bedRoom'] / (input_df['bathroom'] + 1)

#     # --- 3. Ensure column order is the same as the training data (X) ---
#     # The model pipeline is sensitive to the order of columns
#     final_cols = ['property_type', 'bedRoom', 'bathroom', 'balcony', 'agePossession',
#                   'built_up_area', 'servant room', 'store room', 'furnishing_type',
#                   'luxury_category', 'floor_category', 'sector_score',
#                   'area_x_sector_score', 'area_x_room', 'bed_bath_ratio']
    
#     input_final_df = input_df[final_cols]

#     # --- 4. Predict ---
#     try:
#         # Predict the log-transformed price
#         predicted_log_price = model.predict(input_final_df)
        
#         # Reverse the log transformation to get the actual price
#         predicted_price = np.expm1(predicted_log_price)[0]

#         # Display the result
#         st.success(f'The predicted price of the property is: ₹{predicted_price:,.2f}')

#     except Exception as e:
#         st.error(f"An error occurred during prediction: {e}")