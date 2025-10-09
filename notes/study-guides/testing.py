import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup

def fetch_fbref_data():
    """Fetch Premier League data from FBref"""
    url = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
    
    try:
        # Try to read tables from FBref
        print("Attempting to fetch data from FBref...")
        tables = pd.read_html(url)
        print(f"Found {len(tables)} tables")
        
        # Let's inspect each table to find the right one
        for i, table in enumerate(tables):
            print(f"\n--- Table {i} ---")
            print(f"Shape: {table.shape}")
            print(f"Columns: {list(table.columns)[:10]}...")  # First 10 columns
            if 'Player' in table.columns:
                print("✅ This table has 'Player' column - likely the main stats table")
                df = table
                break
        else:
            # If no break, use the first table
            df = tables[0]
        
        # Clean the data
        df = clean_fbref_data(df)
        return df
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def clean_fbref_data(df):
    """Clean FBref dataframe"""
    print("Cleaning data...")
    print(f"Original shape: {df.shape}")
    print(f"Original columns: {list(df.columns)}")
    
    # Flatten multi-level columns if they exist
    if isinstance(df.columns, pd.MultiIndex):
        print("Flattening multi-level columns...")
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
        print(f"New columns: {list(df.columns)}")
    
    # Check if 'Rk' column exists before trying to filter
    if 'Rk' in df.columns:
        print("Filtering out header rows...")
        original_len = len(df)
        df = df[df['Rk'] != 'Rk']
        print(f"Removed {original_len - len(df)} header rows")
    else:
        print("No 'Rk' column found, skipping header filtering")
    
    # Convert numeric columns - only if they exist
    numeric_columns = ['Rk', 'Age', 'MP', 'Starts', 'Min', 'Gls', 'Ast', 'CrdY', 'CrdR']
    available_numeric_cols = [col for col in numeric_columns if col in df.columns]
    
    print(f"Converting numeric columns: {available_numeric_cols}")
    for col in available_numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print(f"Cleaned data shape: {df.shape}")
    return df

def create_goals_chart(df):
    """Create and save top scorers chart"""
    if 'Gls' not in df.columns:
        print("No 'Gls' column found for goals chart")
        return
    
    # Get top 10 scorers
    top_scorers = df.nlargest(10, 'Gls')[['Player', 'Squad', 'Gls']]
    
    plt.figure(figsize=(12, 8))
    bars = plt.barh(range(len(top_scorers)), top_scorers['Gls'], 
                    color='skyblue', edgecolor='navy')
    
    plt.yticks(range(len(top_scorers)), top_scorers['Player'], fontsize=10)
    plt.xlabel('Goals', fontsize=12)
    plt.title('Top 10 Goal Scorers - Premier League', fontsize=16, fontweight='bold')
    plt.gca().invert_yaxis()
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                 f"{bar.get_width():.0f}", ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('top_scorers.png', dpi=300, bbox_inches='tight')
    print("Saved: top_scorers.png")

def create_team_analysis(df):
    """Create team goals analysis"""
    if 'Gls' not in df.columns or 'Squad' not in df.columns:
        print("Missing required columns for team analysis")
        return
    
    team_stats = df.groupby('Squad').agg({
        'Gls': 'sum',
        'Ast': 'sum',
        'MP': 'sum'
    }).reset_index()
    
    team_stats['Goals_per_Game'] = team_stats['Gls'] / team_stats['MP']
    
    plt.figure(figsize=(14, 10))
    sns.barplot(data=team_stats.sort_values('Goals_per_Game', ascending=False), 
                x='Goals_per_Game', y='Squad', palette='viridis')
    
    plt.title('Team Goals per Game - Premier League', fontsize=16, fontweight='bold')
    plt.xlabel('Goals per Game', fontsize=12)
    plt.tight_layout()
    plt.savefig('team_goals_per_game.png', dpi=300, bbox_inches='tight')
    print("Saved: team_goals_per_game.png")

# Main execution
if __name__ == "__main__":
    print("FBref Data Analysis - Debug Version")
    print("=" * 50)
    
    # Try to fetch real data
    df = fetch_fbref_data()
    
    if df is not None:
        print(f"✅ Data loaded successfully! {len(df)} players found.")
        print(f"Available columns: {list(df.columns)}")
        
        # Create visualizations with real data
        create_goals_chart(df)
        create_team_analysis(df)
        
        # Show some sample data
        if 'Player' in df.columns and 'Gls' in df.columns:
            print("\nTop 5 scorers:")
            print(df.nlargest(5, 'Gls')[['Player', 'Squad', 'Gls']].to_string(index=False))
        
    else:
        print("❌ Could not fetch data")
    
    print("Analysis complete!")
