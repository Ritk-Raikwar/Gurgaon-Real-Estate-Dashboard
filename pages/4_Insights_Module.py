import streamlit as st
import pandas as pd
import numpy as np
import joblib

# --- Page Configuration ---
st.set_page_config(
    page_title="Gurgaon Real Estate Insights",
    page_icon="💡",
    layout="wide"
)

# --- Load Required Files ---
@st.cache_resource
def load_assets():
    """
    Loads all the final pickle files for the insights module.
    Caches the result to prevent reloading on every interaction.
    """
    try:
        df = joblib.load('data/insights_df_final.pkl') 
        model = joblib.load('data/ridge_model_final.pkl')
        scaler = joblib.load('data/scaler_final.pkl')
        columns = joblib.load('data/model_columns_final.pkl')
        return df, model, scaler, columns
    except FileNotFoundError:
        st.error("One or more required model files are missing. Please run the `train_final_model.py` script first.")
        return None, None, None, None

df, model, scaler, model_columns = load_assets()

# --- UI Layout ---
st.title("💡 Real Estate Price Insights ")
st.markdown("""
This tool uses an advanced machine learning model with feature interactions to estimate property prices in Gurgaon. 
Adjust the property details below to see how different features impact the final price.
""")

if df is not None:
    # Create a mapping from sector names to their average price per sqft for calculations
    sector_price_map = df.groupby('sector')['sector_avg_price'].mean()

    # --- Level 1: Location Filter ---
    st.header("Step 1: Select Location")
    
    unique_sectors = sorted(df['sector'].unique())
    selected_sector = st.selectbox("Select a Sector", unique_sectors)

    # --- Level 2: Feature Input ---
    st.header("Step 2: Define Property Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        property_type = st.selectbox("Property Type", df['property_type'].unique(), format_func=lambda x: 'House' if x == 1 else 'Flat')
        bedRoom = st.slider("Number of Bedrooms", 1, 10, 3)
        bathroom = st.slider("Number of Bathrooms", 1, 10, 3)
        servant_room = st.radio("Servant Room", [0, 1], format_func=lambda x: 'Yes' if x == 1 else 'No')

    with col2:
        built_up_area = st.number_input("Built-up Area (in sq. ft.)", min_value=100, max_value=10000, value=1500)
        agePossession = st.selectbox("Age of Possession", df['agePossession'].unique())
        furnishing_type = st.selectbox("Furnishing Type", df['furnishing_type'].unique(), format_func=lambda x: 'Unfurnished' if x == 0 else ('Semi-furnished' if x == 1 else 'Furnished'))
        
    with col3:
        luxury_category = st.selectbox("Luxury Category", df['luxury_category'].unique(), format_func=lambda x: 'Low' if x == 0 else ('Medium' if x == 1 else 'High'))

    # --- Prediction Logic ---
    if st.button("Estimate Price", type="primary"):
        
        # 1. Create a dictionary with the basic user inputs
        input_data = {
            'property_type': property_type,
            'bedRoom': bedRoom,
            'bathroom': bathroom,
            'built_up_area': built_up_area,
            'servant room': servant_room,
            'furnishing_type': furnishing_type,
            'luxury_category': luxury_category,
        }
        
        # 2. Add the pre-calculated advanced features
        input_data['sector_avg_price'] = sector_price_map.get(selected_sector, 0)
        input_data['area_x_sector_avg_price'] = built_up_area * input_data['sector_avg_price']
        input_data['area_by_room'] = built_up_area / (bedRoom + 1)
        input_data['bed_bath_ratio'] = bedRoom / (bathroom + 1)
        
        # 3. Create a DataFrame from the complete feature set
        input_df = pd.DataFrame([input_data])
        
        # 4. One-hot encode 'agePossession'
        input_df['agePossession'] = agePossession
        input_df = pd.get_dummies(input_df, columns=['agePossession'], drop_first=True)

        # 5. Align columns with the model's training columns
        final_input_df = pd.DataFrame(columns=model_columns).reindex(columns=model_columns).fillna(0)
        final_input_df = pd.concat([final_input_df, input_df], ignore_index=True, sort=False).fillna(0)
        final_input_df = final_input_df[model_columns]

        # 6. Scale the features
        scaled_input = scaler.transform(final_input_df)

        # 7. Make the prediction
        prediction_log = model.predict(scaled_input)

        # 8. Inverse transform to get the actual price
        predicted_price = np.expm1(prediction_log)[0]
        
        # --- Display Results ---
        st.subheader("Results")
        
        avg_price_sector = df[df['sector'] == selected_sector]['price'].mean()

        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.metric(
                label="Estimated Price for Your Property",
                value=f"₹ {predicted_price:.2f} Cr"
            )
        
        with res_col2:
            st.metric(
                label=f"Average Price in {selected_sector}",
                value=f"₹ {avg_price_sector:.2f} Cr",
                delta=f"{((predicted_price - avg_price_sector) / avg_price_sector) * 100:.2f}% vs. Average"
            )
        
        st.info("The 'delta' shows how the price of your configured property compares to the average property price in the selected sector.")