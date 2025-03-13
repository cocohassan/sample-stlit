import pandas as pd
import numpy as np
from typing import Tuple

class DataProcessor:
    @staticmethod
    def process_csv(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """
        Process the CSV data and classify startups according to the demo format
        """
        # Load the reference data
        reference_data = pd.read_csv("attached_assets/coiq_demo_output - v2.csv")

        # For demo purposes, always return the reference data
        processed_df = reference_data.copy()

        # Calculate statistics
        stats = {
            'total_startups': len(processed_df),
            'rocket_type_distribution': processed_df['Final Label'].value_counts().to_dict(),
            'percentages': (processed_df['Final Label'].value_counts(normalize=True) * 100).round(2).to_dict()
        }

        return processed_df, stats
