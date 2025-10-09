def build_predictive_model(df, target='Pts'):
    """Build model to identify most important predictors"""
    
    # Feature selection
    potential_features = [
        'Gls', 'GA', 'xG', 'xGA', 'Poss', 'SoT', 'SoTA', 
        'Cmp%', 'PrgP', 'PrgC', 'Age', 'Conversion_Rate'
    ]
    
    # Only use features that exist in data
    features = [f for f in potential_features if f in df.columns]
    
    X = df[features].fillna(0)
    y = df[target]
    
    # Random Forest for feature importance
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    # Get feature importance
    importance_df = pd.DataFrame({
        'feature': features,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    # Plot feature importance
    plt.figure(figsize=(10, 6))
    plt.barh(importance_df['feature'], importance_df['importance'])
    plt.xlabel('Feature Importance')
    plt.title('Random Forest Feature Importance for Predicting Success')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    
    return importance_df, rf

importance_df, model = build_predictive_model(team_data_clean)