from pyDecision.algorithm import waspas_method

def calculate_vulneral_score(df, weights, criterion):
    Score_WSM, Score_WPM, Score_WASPAS = waspas_method(dataset=df, criterion_type=criterion, weights=weights, lambda_value=0.5)
    return Score_WSM, Score_WPM, Score_WASPAS