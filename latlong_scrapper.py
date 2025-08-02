import pandas as pd
from geopy.geocoders import Nominatim
import time

def get_gurgaon_sector_coordinates():
    """
    Scrapes latitude and longitude for Gurgaon sectors 1 to 115.

    Returns:
        pandas.DataFrame: A DataFrame with columns 'sector_name', 'lat', and 'log'.
    """
    # Initialize the geolocator with a custom user agent
    geolocator = Nominatim(user_agent="gurgaon_sector_scraper_v1")
    
    # List to store the data
    sector_data = []

    print("Starting to fetch coordinates for Gurgaon sectors 1 to 115...")

    # Loop through sectors from 1 to 115
    for i in range(1, 116):
        sector_name = f"sector {i}"
        query = f"{sector_name}, gurgaon, haryana"
        
        try:
            # Geocode the location
            # Adding a small delay to respect the usage policy of Nominatim
            time.sleep(1) 
            
            location = geolocator.geocode(query)
            
            if location:
                lat, lon = location.latitude, location.longitude
                print(f"Successfully found {sector_name}: Lat={lat}, Lon={lon}")
                sector_data.append({
                    "sector_name": sector_name,
                    "lat": lat,
                    "log": lon
                })
            else:
                print(f"Could not find coordinates for {sector_name}.")
                sector_data.append({
                    "sector_name": sector_name,
                    "lat": None,
                    "log": None
                })

        except Exception as e:
            print(f"An error occurred while processing {sector_name}: {e}")
            sector_data.append({
                "sector_name": sector_name,
                "lat": None,
                "log": None
            })

    print("\nFinished fetching coordinates.")
    
    # Create a pandas DataFrame
    df = pd.DataFrame(sector_data)
    
    return df

if __name__ == "__main__":
    # Get the DataFrame
    gurgaon_sectors_df = get_gurgaon_sector_coordinates()
    
    # Display the first few rows of the DataFrame
    print("\n--- Gurgaon Sector Coordinates DataFrame ---")
    print(gurgaon_sectors_df.head())
    
    # Display information about the DataFrame
    print("\n--- DataFrame Info ---")
    gurgaon_sectors_df.info()
    
    # Save the DataFrame to a CSV file
    output_filename = "gurgaon_sectors_lat_long.csv"
    gurgaon_sectors_df.to_csv(output_filename, index=False)
    
    print(f"\nDataFrame saved to {output_filename}")
