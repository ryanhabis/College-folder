import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Define what "success" means
SUCCESS_METRICS = {
    'Points': 'Final league points',
    'Position': 'Final league position (inverse)',
    'Goal_Difference': 'Goals scored - goals conceded',
    'Wins': 'Number of wins'
}