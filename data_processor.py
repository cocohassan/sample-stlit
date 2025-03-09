import pandas as pd
from typing import Tuple

class DataProcessor:
    @staticmethod
    def process_csv(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """
        Process the CSV data and return processed dataframe with statistics
        """
        stats = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'numeric_columns': len(df.select_dtypes(include=['float64', 'int64']).columns),
            'missing_values': df.isnull().sum().sum()
        }
        
        # Basic processing steps
        processed_df = df.copy()
        
        # Fill missing numeric values with mean
        numeric_columns = processed_df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_columns:
            processed_df[col] = processed_df[col].fillna(processed_df[col].mean())
            
        # Fill missing categorical values with mode
        categorical_columns = processed_df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            processed_df[col] = processed_df[col].fillna(processed_df[col].mode()[0] if not processed_df[col].mode().empty else 'Unknown')
            
        # Add summary statistics for numeric columns
        stats['column_stats'] = {
            col: {
                'mean': processed_df[col].mean(),
                'std': processed_df[col].std(),
                'min': processed_df[col].min(),
                'max': processed_df[col].max()
            } for col in numeric_columns
        }
        
        return processed_df, stats
