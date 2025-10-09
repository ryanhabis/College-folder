def generate_insights(ce_analysis, correlations):
    """Generate actionable insights for team building"""
    
    print("=" * 60)
    print("TEAM BUILDING INSIGHTS REPORT")
    print("=" * 60)
    
    print("\n🎯 TOP PREDICTORS OF SUCCESS:")
    top_predictors = ce_analysis.head(5)
    for i, row in top_predictors.iterrows():
        print(f"  {i+1}. {row['Statistic']} (Importance: {row['Predictive_Importance']:.3f})")
    
    print("\n💰 MOST COST-EFFECTIVE STATS:")
    cost_effective = ce_analysis.sort_values('Cost_Effectiveness', ascending=False).head(5)
    for i, row in cost_effective.iterrows():
        print(f"  {i+1}. {row['Statistic']} (Cost: {row['Cost_Factor']})")
    
    print("\n📈 ACTIONABLE STRATEGIES:")
    
    # Generate specific recommendations
    strategies = []
    
    if 'PrgP' in cost_effective['Statistic'].values:
        strategies.append("• Invest in progressive passers - often cheaper than pure goalscorers")
    
    if 'Conversion_Rate' in cost_effective['Statistic'].values:
        strategies.append("• Focus on efficient finishers rather than volume shooters")
    
    if 'xG' in top_predictors['Statistic'].values:
        strategies.append("• Prioritize players who generate high-quality chances (xG)")
    
    if 'GA' in top_predictors['Statistic'].values:
        strategies.append("• Strong defense remains crucial - don't overspend only on attack")
    
    for strategy in strategies:
        print(strategy)
    
    print(f"\n📊 Data based on {len(team_data_clean)} team-seasons of analysis")

# Generate the final report
generate_insights(ce_analysis, correlations)