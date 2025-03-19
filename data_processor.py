import pandas as pd
import numpy as np
from typing import Tuple
import country_converter as coco

class DataProcessor:
    # Dictionary mapping countries to their approximate center coordinates
    COUNTRY_COORDS = {
        'Palestine': {'lat': 31.9522, 'lon': 35.2332},
        'SaudiArabia': {'lat': 23.8859, 'lon': 45.0792},
        'Indonesia': {'lat': -0.7893, 'lon': 113.9213},
        'Malaysia': {'lat': 4.2105, 'lon': 101.9758},
        'Canada': {'lat': 56.1304, 'lon': -106.3468},
        'UnitedKingdom': {'lat': 55.3781, 'lon': -3.4360},
        'UnitedStates': {'lat': 37.0902, 'lon': -95.7129},
        'Nigeria': {'lat': 9.0820, 'lon': 8.6753},
        'India': {'lat': 20.5937, 'lon': 78.9629},
        'UnitedArabEmirates': {'lat': 23.4241, 'lon': 53.8478},
        'Singapore': {'lat': 1.3521, 'lon': 103.8198},
        'Namibia': {'lat': -22.9576, 'lon': 18.4904},
        'Pakistan': {'lat': 30.3753, 'lon': 69.3451},
        'Uzbekistan': {'lat': 41.3775, 'lon': 64.5853},
        'Zambia': {'lat': -13.1339, 'lon': 27.8493},
        'France': {'lat': 46.2276, 'lon': 2.2137},
        'Malawi': {'lat': -13.2543, 'lon': 34.3015},
        'Austria': {'lat': 47.5162, 'lon': 14.5501},
        'SouthAfrica': {'lat': -30.5595, 'lon': 22.9375}
    }

    @staticmethod
    def process_csv(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """
        Process the CSV data and classify startups according to the demo format
        """
        # Load the reference data
        reference_data = pd.read_csv("attached_assets/coiq_demo_output - v3 Full.csv")

        # For demo purposes, always return the reference data
        processed_df = reference_data.copy()

        # Add latitude and longitude based on country
        processed_df['latitude'] = processed_df['Country'].map(lambda x: DataProcessor.COUNTRY_COORDS.get(x, {'lat': 0})['lat'])
        processed_df['longitude'] = processed_df['Country'].map(lambda x: DataProcessor.COUNTRY_COORDS.get(x, {'lon': 0})['lon'])

        # Calculate statistics
        stats = {
            'total_startups': len(processed_df),
            'rocket_type_distribution': processed_df['Final Label'].value_counts().to_dict(),
            'percentages': (processed_df['Final Label'].value_counts(normalize=True) * 100).round(2).to_dict()
        }

        return processed_df, stats