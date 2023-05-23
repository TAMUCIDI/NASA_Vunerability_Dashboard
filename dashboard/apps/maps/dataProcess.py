from pyDecision.algorithm import waspas_method

def calculate_vulneral_score(df, weights, criterion):
    # shape check
    if df.shape[1] != weights.shape[0] or df.shape[1] != len(criterion):
        print("shape not match")
        return None, None, None
    Score_WSM, Score_WPM, Score_WASPAS = waspas_method(dataset=df.values, criterion_type=criterion, weights=weights, lambda_value=0.5)
    return Score_WSM, Score_WPM, Score_WASPAS