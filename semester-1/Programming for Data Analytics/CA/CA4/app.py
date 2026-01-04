# app.py - UPDATED FOR TEMPLATE FOLDER
from flask import Flask, jsonify, render_template, request
import pandas as pd
import os

# Initialize Flask app
app = Flask(__name__)

# Path to your CSV file
CSV_PATH = 'semester-1\Programming for Data Analytics\CA\CA4\cleaned_football_data.csv'

print(f"Loading data from: {CSV_PATH}")

# Load data
try:
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        print(f"✅ Successfully loaded {len(df)} rows")
    else:
        print(f"❌ File not found: {CSV_PATH}")
        # Create empty DataFrame if file doesn't exist
        df = pd.DataFrame()
except Exception as e:
    print(f"Error loading data: {e}")
    df = pd.DataFrame()

# ========== ROUTES ==========

@app.route('/')
def home():
    """Home page - uses templates/index.html"""
    return render_template('index.html', 
                         total_matches=len(df) if not df.empty else 0)

@app.route('/dashboard')
def dashboard():
    """Dashboard page - uses templates/dashboard.html"""
    if df.empty:
        return "No data available. Please run the scraping notebook first."
    
    # Calculate stats for the dashboard
    stats = {
        'total_matches': len(df),
        'home_win_rate': f"{df['HomeWin'].mean() * 100:.1f}%" if 'HomeWin' in df.columns else "N/A",
        'away_win_rate': f"{df['AwayWin'].mean() * 100:.1f}%" if 'AwayWin' in df.columns else "N/A",
        'draw_rate': f"{df['Draw'].mean() * 100:.1f}%" if 'Draw' in df.columns else "N/A",
        'avg_goals': f"{df['TotalGoals'].mean():.2f}" if 'TotalGoals' in df.columns else "N/A",
        'seasons': df['Season'].unique().tolist() if 'Season' in df.columns else []
    }
    
    # Get top teams for display
    top_teams = {}
    if 'HomeTeam' in df.columns and 'AwayTeam' in df.columns and 'HomeWin' in df.columns:
        home_wins = df.groupby('HomeTeam')['HomeWin'].sum()
        away_wins = df.groupby('AwayTeam')['AwayWin'].sum()
        total_wins = home_wins.add(away_wins, fill_value=0)
        top_teams = total_wins.sort_values(ascending=False).head(10).to_dict()
    
    # Sample data for table
    sample_data = df.head(10).to_dict('records') if not df.empty else []
    
    return render_template('dashboard.html',
                          stats=stats,
                          top_teams=top_teams,
                          sample_data=sample_data)

# ========== API ENDPOINTS ==========

@app.route('/api/v1/data/all', methods=['GET'])
def api_all():
    """Return all data as JSON"""
    if df.empty:
        return jsonify({'error': 'No data available'}), 404
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/v1/data/stats', methods=['GET'])
def api_stats():
    """Return statistics"""
    if df.empty:
        return jsonify({'error': 'No data available'}), 404
    
    stats = {
        'total_matches': len(df),
        'home_win_percentage': round(df['HomeWin'].mean() * 100, 2) if 'HomeWin' in df.columns else 0,
        'away_win_percentage': round(df['AwayWin'].mean() * 100, 2) if 'AwayWin' in df.columns else 0,
        'average_goals_per_match': round(df['TotalGoals'].mean(), 2) if 'TotalGoals' in df.columns else 0,
        'seasons_covered': df['Season'].unique().tolist() if 'Season' in df.columns else []
    }
    return jsonify(stats)

@app.route('/api/v1/data/filter', methods=['GET'])
def api_filter():
    """Filter data - like lecturer's example"""
    if df.empty:
        return jsonify({'error': 'No data available'}), 404
    
    team = request.args.get('team', '').strip()
    season = request.args.get('season', '').strip()
    
    filtered_df = df.copy()
    
    if team:
        filtered_df = filtered_df[
            (filtered_df['HomeTeam'].astype(str).str.contains(team, case=False)) |
            (filtered_df['AwayTeam'].astype(str).str.contains(team, case=False))
        ]
    
    if season:
        filtered_df = filtered_df[filtered_df['Season'] == season]
    
    return jsonify({
        'filters_applied': {'team': team, 'season': season},
        'match_count': len(filtered_df),
        'data': filtered_df.to_dict(orient='records')
    })

# Error handler
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)