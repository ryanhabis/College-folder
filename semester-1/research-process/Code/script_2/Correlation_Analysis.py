def analyze_correlations(df, target='Pts'):
    """Analyze which stats correlate most with success"""
    
    # Select only numeric columns for correlation
    numeric_df = df.select_dtypes(include=[np.number])
    
    # Calculate correlations with the target
    if target in numeric_df.columns:
        correlations = numeric_df.corr()[target].sort_values(ascending=False)
        
        # Plot top correlations
        plt.figure(figsize=(10, 8))
        top_corr = correlations[1:11]  # Exclude target itself
        colors = ['green' if x > 0 else 'red' for x in top_corr.values]
        
        plt.barh(range(len(top_corr)), top_corr.values, color=colors)
        plt.yticks(range(len(top_corr)), top_corr.index)
        plt.xlabel('Correlation with ' + target)
        plt.title(f'Top 10 Statistics Correlated with {target}')
        plt.tight_layout()
        plt.savefig('correlation_analysis.png', dpi=300, bbox_inches='tight')
        
        return correlations
    else:
        print(f"Target column '{target}' not found")
        return None

correlations = analyze_correlations(team_data_clean, 'Pts')