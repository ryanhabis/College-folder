# team_analysis_basic.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def collect_team_data():
    """Collect team data from FBref"""
    print("📊 Collecting data from FBref...")
    
    seasons = {
        '2023-24': 'https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats',
    }
    
    all_data = []
    
    for season, url in seasons.items():
        try:
            tables = pd.read_html(url)
            
            for table in tables:
                if 'Squad' in str(table.columns) and len(table) == 20:
                    table['Season'] = season
                    all_data.append(table)
                    print(f"✅ Collected {season} data")
                    break
                    
        except Exception as e:
            print(f"❌ Error collecting {season}: {e}")
            # Create sample data as fallback
            return create_sample_data()
    
    return pd.concat(all_data, ignore_index=True) if all_data else create_sample_data()

def create_sample_data():
    """Create realistic sample data"""
    print("📝 Creating sample data for analysis...")
    
    teams = [
        'Manchester City', 'Liverpool', 'Arsenal', 'Aston Villa', 'Tottenham',
        'Manchester Utd', 'West Ham', 'Brighton', 'Wolves', 'Newcastle',
        'Chelsea', 'Fulham', 'Bournemouth', 'Crystal Palace', 'Brentford',
        'Everton', 'Nottm Forest', 'Luton Town', 'Burnley', 'Sheffield Utd'
    ]
    
    data = []
    for i, team in enumerate(teams):
        data.append({
            'Squad': team,
            'MP': 38,
            'W': 38 - i - 10 if i < 10 else 38 - i - 5,  # More realistic distribution
            'D': 5 + (i % 5),
            'L': i if i < 10 else i - 5,
            'GF': 90 - i * 3,  # Goals For
            'GA': 30 + i * 2,  # Goals Against
            'GD': 60 - i * 5,  # Goal Difference
            'Pts': 90 - i * 3, # Points
            'xG': 80 - i * 2.5, # Expected Goals
            'xGA': 35 + i * 1.5, # Expected Goals Against
            'Poss': 65 - i * 1.5, # Possession %
            'SoT': 180 - i * 6,   # Shots on Target
            'SoTA': 120 + i * 3,  # Shots on Target Against
            'Age': 26 + (i % 5) * 0.5, # Squad Age
        })
    
    df = pd.DataFrame(data)
    df['Conversion_Rate'] = df['GF'] / df['SoT']
    return df

def analyze_correlations_basic(df):
    """Basic correlation analysis without scikit-learn"""
    print("🔍 Analyzing correlations...")
    
    # Calculate correlations with Points
    numeric_df = df.select_dtypes(include=[np.number])
    
    if 'Pts' in numeric_df.columns:
        correlations = numeric_df.corr()['Pts'].sort_values(ascending=False)
        
        # Plot top correlations
        plt.figure(figsize=(10, 8))
        top_corr = correlations[1:11]  # Exclude Pts itself
        
        colors = ['green' if x > 0 else 'red' for x in top_corr.values]
        plt.barh(range(len(top_corr)), top_corr.values, color=colors)
        plt.yticks(range(len(top_corr)), top_corr.index)
        plt.xlabel('Correlation with Points')
        plt.title('Top Statistics Correlated with Team Success (Points)')
        
        # Add correlation values on bars
        for i, v in enumerate(top_corr.values):
            plt.text(v + 0.01 if v > 0 else v - 0.05, i, f'{v:.3f}', 
                    va='center', fontsize=10)
        
        plt.tight_layout()
        plt.savefig('correlation_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return correlations
    return None

def cost_effectiveness_basic(df, correlations):
    """Basic cost-effectiveness analysis"""
    print("💰 Analyzing cost-effectiveness...")
    
    # Define cost factors for different stats
    cost_factors = {
        'GF': 'High',        # Goals are expensive
        'xG': 'Medium',      # Expected goals moderately expensive
        'GA': 'High',        # Good defense is expensive  
        'GD': 'High',        # Goal difference requires both
        'Poss': 'Medium',    # Possession players
        'SoT': 'Medium',     # Shot creators
        'Conversion_Rate': 'Medium', # Efficient scorers
        'xGA': 'Medium',     # Defensive organization
        'Age': 'Variable'    # Youth vs experience
    }
    
    # Create analysis dataframe
    analysis = []
    for stat, corr in correlations.items():
        if stat in cost_factors and stat != 'Pts':
            cost = cost_factors[stat]
            cost_score = {'High': 1, 'Medium': 2, 'Low': 3, 'Variable': 2}[cost]
            
            analysis.append({
                'Statistic': stat,
                'Correlation': abs(corr),  # Use absolute value for importance
                'Cost_Factor': cost,
                'Cost_Effectiveness': abs(corr) * cost_score
            })
    
    ce_df = pd.DataFrame(analysis).sort_values('Cost_Effectiveness', ascending=False)
    
    # Plot cost-effectiveness
    plt.figure(figsize=(12, 8))
    colors = {'High': 'red', 'Medium': 'orange', 'Low': 'green', 'Variable': 'blue'}
    
    for i, row in ce_df.head(10).iterrows():
        plt.scatter(row['Correlation'], row['Cost_Effectiveness'], 
                   c=colors[row['Cost_Factor']], s=100, 
                   label=row['Cost_Factor'] if i == 0 else "")
    
    plt.xlabel('Correlation with Success (Absolute Value)')
    plt.ylabel('Cost-Effectiveness Score')
    plt.title('Cost-Effectiveness of Team Statistics')
    plt.legend(title='Cost Level')
    
    # Add labels
    for i, row in ce_df.head(10).iterrows():
        plt.annotate(row['Statistic'], (row['Correlation'], row['Cost_Effectiveness']),
                    xytext=(5, 5), textcoords='offset points', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('cost_effectiveness_basic.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return ce_df

def generate_insights_basic(ce_df):
    """Generate insights from the analysis"""
    print("\n" + "="*60)
    print("TEAM BUILDING INSIGHTS REPORT")
    print("="*60)
    
    print("\n🎯 TOP PREDICTORS OF SUCCESS:")
    top_predictors = ce_df.head(5)
    for i, row in top_predictors.iterrows():
        print(f"  {i+1}. {row['Statistic']} (Correlation: {row['Correlation']:.3f})")
    
    print("\n💰 MOST COST-EFFECTIVE STATS:")
    cost_effective = ce_df.head(5)
    for i, row in cost_effective.iterrows():
        print(f"  {i+1}. {row['Statistic']} (Cost: {row['Cost_Factor']})")
    
    print("\n📈 ACTIONABLE STRATEGIES:")
    
    strategies = []
    if any('xG' in row['Statistic'] for row in ce_df.head(3).itertuples()):
        strategies.append("• Focus on expected goals (xG) - indicates chance quality")
    
    if any('Conversion' in row['Statistic'] for row in ce_df.head(5).itertuples()):
        strategies.append("• Improve conversion rate through better finishing")
    
    if any('GA' in row['Statistic'] for row in ce_df.head(5).itertuples()):
        strategies.append("• Strong defense remains crucial for success")
    
    strategies.append("• Balance expensive star players with cost-effective role players")
    strategies.append("• Data-driven recruitment can provide competitive advantage")
    
    for strategy in strategies:
        print(strategy)
    
    print(f"\n📊 Analysis based on {len(df)} teams")
    print("💡 Note: For deeper analysis, integrate wage and transfer fee data")

# Main execution
if __name__ == "__main__":
    print("🚀 Starting Basic Team Success Analysis...")
    
    # Collect data
    df = collect_team_data()
    print(f"✅ Data ready: {len(df)} teams loaded")
    
    # Run analysis
    correlations = analyze_correlations_basic(df)
    
    if correlations is not None:
        ce_analysis = cost_effectiveness_basic(df, correlations)
        generate_insights_basic(ce_analysis)
        print("\n✅ Analysis complete! Check generated PNG files.")
    else:
        print("❌ Analysis failed - check your data")
