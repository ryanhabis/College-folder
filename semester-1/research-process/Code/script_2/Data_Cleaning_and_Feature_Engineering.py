def clean_and_prepare_data(df):
    """Clean the team data and create features"""
    
    # Flatten multi-index columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
    
    # Basic cleaning
    df = df[df['Squad'] != 'Squad']  # Remove header rows
    
    # Define potential predictor variables (features)
    feature_columns = [
        # Attack metrics
        'Gls', 'Sh', 'SoT', 'Poss', 'xG', 'npxG', 'xAG', 
        # Defense metrics  
        'GA', 'SoTA', 'Save%', 'CS', 
        # Passing and possession
        'Cmp%', 'PrgP', 'PrgC',
        # Discipline
        'CrdY', 'CrdR',
        # Financial (if available - would need additional sources)
        'Age'  # Squad age as proxy for experience vs youth
    ]
    
    # Convert to numeric
    for col in feature_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Create some derived features
    if all(col in df.columns for col in ['Gls', 'Sh']):
        df['Conversion_Rate'] = df['Gls'] / df['Sh']
    
    if all(col in df.columns for col in ['xG', 'Gls']):
        df['xG_Overperformance'] = df['Gls'] - df['xG']
    
    return df

team_data_clean = clean_and_prepare_data(team_data)