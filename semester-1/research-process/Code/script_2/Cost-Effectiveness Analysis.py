def cost_effectiveness_analysis(df, importance_df):
    """Analyze which high-impact stats are most cost-effective"""
    
    # This is where you'd integrate salary/wage data
    # For demonstration, we'll use some assumptions
    
    # Common cost proxies (you'd replace with real wage data)
    cost_factors = {
        'Gls': 'High',        # Goalscorers are expensive
        'xG': 'Medium',       # Chance creators moderately expensive  
        'PrgP': 'Low',        # Progressive passers can be found cheaper
        'Conversion_Rate': 'Medium',  # Efficient scorers
        'GA': 'High',         # Good defenders are expensive
        'SoTA': 'Medium',     # Shot prevention
        'Age': 'Variable'     # Young = potential, Old = experience
    }
    
    # Create cost-effectiveness score
    analysis = []
    for feature in importance_df['feature']:
        importance = importance_df[importance_df['feature'] == feature]['importance'].values[0]
        cost = cost_factors.get(feature, 'Medium')
        
        # Simple cost scoring (you'd refine this)
        cost_score = {'High': 1, 'Medium': 2, 'Low': 3, 'Variable': 2}[cost]
        
        analysis.append({
            'Statistic': feature,
            'Predictive_Importance': importance,
            'Cost_Factor': cost,
            'Cost_Effectiveness': importance * cost_score  # Higher = better value
        })
    
    ce_df = pd.DataFrame(analysis).sort_values('Cost_Effectiveness', ascending=False)
    
    # Plot cost-effectiveness
    plt.figure(figsize=(12, 8))
    colors = {'High': 'red', 'Medium': 'orange', 'Low': 'green', 'Variable': 'blue'}
    
    for i, row in ce_df.iterrows():
        plt.scatter(row['Predictive_Importance'], row['Cost_Effectiveness'], 
                   c=colors[row['Cost_Factor']], s=100, label=row['Cost_Factor'] if i == 0 else "")
    
    plt.xlabel('Predictive Importance')
    plt.ylabel('Cost-Effectiveness Score')
    plt.title('Cost-Effectiveness of Different Statistics')
    plt.legend(title='Cost Level')
    
    # Add labels for each point
    for i, row in ce_df.iterrows():
        plt.annotate(row['Statistic'], (row['Predictive_Importance'], row['Cost_Effectiveness']),
                    xytext=(5, 5), textcoords='offset points', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('cost_effectiveness.png', dpi=300, bbox_inches='tight')
    
    return ce_df

ce_analysis = cost_effectiveness_analysis(team_data_clean, importance_df)