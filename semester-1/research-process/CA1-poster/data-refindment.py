import pandas as pd
    
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup

"""
    The code fetches and analyzes Premier League player data from FBref, creates visualizations like top
    scorers chart and team goals comparison, and handles cases where real data cannot be fetched by
    generating sample data.
    
    :return: The code provided defines functions to fetch and analyze Premier League player data from
    FBref. The main execution section attempts to fetch real data using the `fetch_fbref_player_data()`
    function. If successful, it prints the number of records found and displays basic information about
    the players. 
    
    It then creates three visualizations:
     Top scorers chart
     Team goals comparison chart
     A goals vs assists scatter
    """

def fetch_fbref_player_data():
    """Fetch Premier League PLAYER data from FBref"""
    # Use the player stats URL instead of team stats
    url = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
    
    try:
        print("Attempting to fetch player data from FBref...")
        tables = pd.read_html(url)
        print(f"Found {len(tables)} tables")
        
        # Let's look for the player stats table - it usually has more rows
        for i, table in enumerate(tables):
            print(f"\n--- Table {i} ---")
            print(f"Shape: {table.shape}")
            if table.shape[0] > 50:  # Player table has many rows
                print("✅ This looks like the player stats table (many rows)")
                df = table
                break
        else:
            # If no table with many rows, try a different approach
            print("Trying alternative URL for player data...")
            return fetch_fbref_alternative()
        
        # Clean the data
        df = clean_fbref_data(df)
        return df
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return fetch_fbref_alternative()

def fetch_fbref_alternative():
    """Alternative method using a different FBref page"""
    try:
        # Try the "Player Stats" specific page
        url = "https://fbref.com/notes/study-guides/panda-data-test.pyen/comps/9/stats/2023-2024/Premier-League-Stats"
        print(f"Trying alternative URL: {url}")
        
        tables = pd.read_html(url)
        for i, table in enumerate(tables):
            if table.shape[0] > 100:  # Look for table with many players
                print(f"Found player table with {table.shape[0]} rows")
                df = table
                return clean_fbref_data(df)
        
        # If still no luck, create sample data for demonstration
        return create_sample_data()
        
    except Exception as e:
        print(f"Alternative method failed: {e}")
        return create_sample_data()

def create_sample_data():
    """Create sample football data for demonstration"""
    print("Creating sample data for demonstration...")
    
    sample_players = [
        'Erling Haaland', 'Mohamed Salah', 'Harry Kane', 'Heung-min Son', 
        'Bukayo Saka', 'Kevin De Bruyne', 'Bruno Fernandes', 'Marcus Rashford',
        'Phil Foden', 'Ollie Watkins', 'Jarrod Bowen', 'Alexander Isak'
    ]
    
    sample_teams = [
        'Manchester City', 'Liverpool', 'Bayern Munich', 'Tottenham',
        'Arsenal', 'Manchester City', 'Manchester Utd', 'Manchester Utd',
        'Manchester City', 'Aston Villa', 'West Ham', 'Newcastle'
    ]
    
    sample_positions = ['FW', 'FW', 'FW', 'FW', 'MF', 'MF', 'MF', 'FW', 'MF', 'FW', 'FW', 'FW']
    
    import random
    data = {
        'Player': sample_players,
        'Squad': sample_teams,
        'Pos': sample_positions,
        'Gls': [random.randint(15, 25) for _ in range(12)],
        'Ast': [random.randint(5, 15) for _ in range(12)],
        'MP': [random.randint(20, 35) for _ in range(12)],
        'Min': [random.randint(1500, 3000) for _ in range(12)],
        'Age': [random.randint(22, 30) for _ in range(12)]
    }
    
    df = pd.DataFrame(data)
    df = df.sort_values('Gls', ascending=False).reset_index(drop=True)
    df['Rk'] = range(1, len(df) + 1)
    
    return df

def clean_fbref_data(df):
    """Clean FBref dataframe"""
    print("Cleaning data...")
    print(f"Original shape: {df.shape}")
    
    # Flatten multi-level columns if they exist
    if isinstance(df.columns, pd.MultiIndex):
        print("Flattening multi-level columns...")
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
    
    print(f"Columns: {list(df.columns)}")
    
    # Look for common column names and rename them for consistency
    column_mapping = {}
    
    # Find and map goal-related columns
    for col in df.columns:
        if 'Gls' in col or 'Goals' in col or 'Performance_Gls' in col:
            column_mapping[col] = 'Gls'
        elif 'Ast' in col or 'Assists' in col or 'Performance_Ast' in col:
            column_mapping[col] = 'Ast'
        elif 'Player' in col:
            column_mapping[col] = 'Player'
        elif 'Squad' in col or 'Team' in col:
            column_mapping[col] = 'Squad'
        elif 'Pos' in col or 'Position' in col:
            column_mapping[col] = 'Pos'
        elif 'MP' in col or 'Matches' in col:
            column_mapping[col] = 'MP'
        elif 'Min' in col or 'Minutes' in col:
            column_mapping[col] = 'Min'
    
    if column_mapping:
        df = df.rename(columns=column_mapping)
        print(f"Mapped columns: {column_mapping}")
    
    print(f"Final columns: {list(df.columns)}")
    print(f"Cleaned data shape: {df.shape}")
    return df

def create_goals_chart(df):
    """Create and save top scorers chart"""
    if 'Gls' not in df.columns or 'Player' not in df.columns:
        print("No 'Gls' or 'Player' column found for goals chart")
        return
    
    # Get top scorers
    top_scorers = df.nlargest(10, 'Gls')[['Player', 'Squad', 'Gls']]
    
    plt.figure(figsize=(12, 8))
    bars = plt.barh(range(len(top_scorers)), top_scorers['Gls'], 
                    color='skyblue', edgecolor='navy')
    
    plt.yticks(range(len(top_scorers)), top_scorers['Player'], fontsize=10)
    plt.xlabel('Goals', fontsize=12)
    plt.title('Top Goal Scorers', fontsize=16, fontweight='bold')
    plt.gca().invert_yaxis()
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                 f"{bar.get_width():.0f}", ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('top_scorers.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: top_scorers.png")

def create_team_analysis(df):
    """Create team goals analysis"""
    if 'Gls' not in df.columns or 'Squad' not in df.columns:
        print("Missing required columns for team analysis")
        return
    
    team_stats = df.groupby('Squad').agg({
        'Gls': 'sum',
        'Ast': 'sum'
    }).reset_index()
    
    team_stats = team_stats.sort_values('Gls', ascending=False)
    
    plt.figure(figsize=(12, 8))
    bars = plt.bar(range(len(team_stats)), team_stats['Gls'], color='lightgreen')
    
    plt.xticks(range(len(team_stats)), team_stats['Squad'], rotation=45, ha='right')
    plt.ylabel('Total Goals', fontsize=12)
    plt.title('Team Goals Comparison', fontsize=16, fontweight='bold')
    
    # Add value labels on bars
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                 f"{bar.get_height():.0f}", ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('team_goals.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: team_goals.png")

def create_goals_vs_assists(df):
    """Create goals vs assists scatter plot"""
    if 'Gls' not in df.columns or 'Ast' not in df.columns:
        print("Missing columns for goals vs assists plot")
        return
    
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(df['Gls'], df['Ast'], alpha=0.7, s=60)
    
    plt.xlabel('Goals', fontsize=12)
    plt.ylabel('Assists', fontsize=12)
    plt.title('Goals vs Assists', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Annotate top performersn(df
    for i, row in df.nlargest(5, 'Gls').iterrows():
        plt.annotate(row['Player'], (row['Gls'], row['Ast']), 
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('goals_vs_assists.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: goals_vs_assists.png")

# Main execution
if __name__ == "__main__":
    print("FBref Player Data Analysis")
    print("=" * 50)
    
    # Try to fetch real data
    df = fetch_fbref_player_data()
    
    if df is not None:
        print(f"✅ Data loaded successfully! {len(df)} records found.")
        
        # Show basic info
        if 'Player' in df.columns:
            print(f"\nFirst few players: {df['Player'].head(5).tolist()}")
        
        # Create visualizations
        create_goals_chart(df)
        create_team_analysis(df)
        create_goals_vs_assists(df)
        
        # Show top scorers
        if 'Gls' in df.columns and 'Player' in df.columns:
            print(f"\nTop 5 scorers:")
            top_scorers = df.nlargest(5, 'Gls')[['Player', 'Squad', 'Gls', 'Ast']]
            print(top_scorers.to_string(index=False))
        
    print("\nAnalysis complete! Check the generated PNG files.")
