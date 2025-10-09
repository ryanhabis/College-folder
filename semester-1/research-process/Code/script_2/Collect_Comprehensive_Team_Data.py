def collect_team_data():
    """Collect multiple seasons of team performance data"""
    
    # FBref URLs for different seasons
    seasons = {
        '2023-24': 'https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats',
        '2022-23': 'https://fbref.com/en/comps/9/2022-2023/2022-2023-Premier-League-Stats',
        '2021-22': 'https://fbref.com/en/comps/9/2021-2022/2021-2022-Premier-League-Stats'
    }
    
    all_data = []
    
    for season, url in seasons.items():
        try:
            tables = pd.read_html(url)
            
            # Find the team stats table (usually has 'Squad' column and ~20 rows)
            for table in tables:
                if 'Squad' in str(table.columns) and len(table) == 20:
                    table['Season'] = season
                    all_data.append(table)
                    print(f"✅ Collected {season} data")
                    break
                    
        except Exception as e:
            print(f"❌ Error collecting {season}: {e}")
            continue
    
    return pd.concat(all_data, ignore_index=True) if all_data else None

# Get the data
team_data = collect_team_data()