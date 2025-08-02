import streamlit as st

# --- Page Configuration ---
# This must be the first Streamlit command in your script.
st.set_page_config(
    page_title="Gurgaon Real Estate Analytics",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Main Page Content ---
st.title("Gurgaon Real Estate Analytics Dashboard")
st.markdown("""
Welcome to the Gurgaon Real Estate Analytics platform. This application is designed to provide comprehensive insights and tools for anyone interested in the Gurgaon property market. Whether you're a buyer, seller, or analyst, you'll find valuable information across our four specialized modules.

Navigate through the modules using the sidebar to the left.
""")

# --- Image Section ---
st.subheader("The Millennium City at a Glance")

# Create three columns
col1, col2, col3 = st.columns(3)

with col1:
    try:
        # Replace with the path to your first image
        st.image('data/gurgaon_real_estate.jpeg', caption='Modern Apartments')
    except FileNotFoundError:
        st.warning("Image 1 not found. Please place 'gurgaon_image_1.jpg' in the 'data' folder.")

with col2:
    try:
        # Replace with the path to your second image
        st.image('data/download.jpeg', caption='Lush Greenery')
    except FileNotFoundError:
        st.warning("Image 2 not found. Please place 'gurgaon_image_2.jpg' in the 'data' folder.")

with col3:
    try:
        # Replace with the path to your third image
        st.image('data/downloadd.jpeg', caption='Commercial Hubs')
    except FileNotFoundError:
        st.warning("Image 3 not found. Please place 'gurgaon_image_3.jpg' in the 'data' folder.")


st.header("Explore Our Modules")

# Using expanders to keep the main page clean
with st.expander("1. 💲 Price Predictor"):
    st.markdown("""
    - **What it does:** Predicts the price of a property based on its features.
    - **How to use:** Enter details like property type, sector, number of bedrooms, area, and other features to get an estimated market price for your property.
    - **Technology:** Powered by a machine learning model trained on a comprehensive dataset of Gurgaon properties.
    """)

with st.expander("2. 📈 Analysis Dashboard"):
    st.markdown("""
    - **What it does:** Provides a high-level statistical and visual analysis of the Gurgaon real estate market.
    - **How to use:** Explore interactive charts and graphs to understand price distributions, property trends by sector, and other key market indicators.
    - **Technology:** Visualizations are created using libraries like Plotly and Matplotlib to offer deep insights into market dynamics.
    """)

with st.expander("3. 🏡 Society Recommender"):
    st.markdown("""
    - **What it does:** Recommends the top 5 societies that best match your preferences.
    - **How to use:** First, filter properties by your desired sector. Then, select a reference property and adjust the weights for features like amenities, price, and location advantages to get personalized recommendations.
    - **Technology:** Uses a sophisticated content-based filtering system built on cosine similarity to find properties that align with your specific needs.
    """)

with st.expander("4. 💡 Price Insights Module"):
    st.markdown("""
    - **What it does:** Allows you to understand how changing a specific feature of a property affects its estimated price.
    - **How to use:** Select a sector and then modify features like the number of bedrooms or the built-up area. The tool will instantly show you the new estimated price and compare it to the sector's average.
    - **Technology:** Leverages an advanced regression model to provide real-time feedback on how different attributes contribute to a property's market value.
    """)

# --- Sidebar Content ---
st.sidebar.title("Navigation")
st.sidebar.markdown("Go to:")

# Ensure your page files are named correctly in a 'pages' folder
st.sidebar.page_link("pages/1_Price_Predictor.py", label="Price Predictor", icon="💲")
st.sidebar.page_link("pages/2_Analysis_Dashboard.py", label="Analysis Dashboard", icon="📈")
st.sidebar.page_link("pages/3_Recommender_System.py", label="Society Recommender", icon="🏡")
st.sidebar.page_link("pages/4_Insights_Module.py", label="Insights Module", icon="💡")

st.sidebar.info(
    """
    This project was created to demonstrate a comprehensive real estate analytics platform using Python, Streamlit, and Machine Learning.
    """
)
