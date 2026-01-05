import numpy as np
import random
from typing import Dict, Any, List

def score_to_risk(score: float) -> str:
    score = float(score) 
    if score >= 0.8: return "critical"
    if score >= 0.6: return "high"
    if score >= 0.4: return "moderate"
    return "low"

def execute_model(disaster_type: str, model: Any, data: Dict[str, Any]) -> List[Dict[str, Any]]:
    results = [] 
    
    if model is None:
        if disaster_type == 'drought': return [] 
        random_score = random.uniform(0.1, 0.95)
        return [{
            "risk_score": float(round(random_score * 100, 2)),
            "risk_level": score_to_risk(random_score),
            "location_name": f"Simulated {disaster_type.capitalize()} Zone",
            "population_at_risk": int(random_score * 100000)
        }]

    try:
        # Fetch shared features
        features = data.get('general_features', {})

        if disaster_type == 'flood':
            # Reshape input to (Batch, Height, Width, Channels) to fix MaxPooling error
            input_data = np.array(data['flood_input_data'])
            input_data = input_data.reshape(1, 256, 256, 1)
            raw_output = model.predict(input_data, verbose=0) 
            mean_risk = float(np.mean(raw_output))
            
            results.append({
                "risk_score": float(round(mean_risk * 100, 2)), 
                "risk_level": score_to_risk(mean_risk),
                "location_name": "East Delta Region",
                "population_at_risk": int(mean_risk * 50000) 
            })
            
        elif disaster_type == 'landslide':
            # Structure features as expected by your .joblib model
            manual_features = np.array([[
                float(features.get('rain', 0.0)), 
                float(features.get('slope_stability', 0.5))
            ]])
            raw_score = float(model.predict(manual_features)[0]) 
            
            results.append({
                "risk_score": float(round(raw_score * 100, 2)), 
                "risk_level": score_to_risk(raw_score),
                "location_name": "West Coast Zone",
                "population_at_risk": int(raw_score * 20000) 
            })

        elif disaster_type in ['cyclone', 'earthquake', 'heatwave']:
            temp = float(features.get('temp', 25.0))
            wind = float(features.get('wind_speed', 10.0))
            score = float((temp * 0.01 + wind * 0.02) * random.uniform(0.5, 1.5))
            score = min(score, 0.99)
            
            results.append({
                "risk_score": float(round(score * 100, 2)), 
                "risk_level": score_to_risk(score),
                "location_name": f"{disaster_type.capitalize()} Region",
                "population_at_risk": int(score * 100000) 
            })

    except Exception as e:
        print(f"ERROR: Prediction failed for {disaster_type}: {e}")
        results.append({
            "risk_score": 5.0,
            "risk_level": "safe",
            "location_name": "Unknown Zone",
            "population_at_risk": 0 
        })

    return results