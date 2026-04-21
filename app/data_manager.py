import pandas as pd
import os

def load_wardrobe_data() -> pd.DataFrame:
    """
    Loads the wardrobe data from the CSV file.
    Provides a disconnected Data Layer from the Logic Layer.
    """
    # Look for the data directory relative to the current working directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "wardrobe.csv")
    
    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["id", "name", "category", "style_type", "color", "primary_tag"])

def get_items_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """Returns items filtered by a specific category."""
    return df[df['category'].str.lower() == category.lower()]
