def create_alert_message(disaster_type: str, location: str, severity: str, population: int):
    loc = location if isinstance(location, str) else f"{location[0]},{location[1]}"
    population_str = f"{population}" if population else "unknown"
    msg = f"ALERT: {disaster_type.upper()} detected at {loc}. Severity: {severity}. Population at risk: {population_str}."
    return msg
