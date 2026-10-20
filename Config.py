import json
import math

def load_config(filename="config.json"):
    with open(filename, "r") as file:
        config = json.load(file)

    required = [
        "mission_name",
        "altitude_km",
        "time_step_seconds",
        "animation_interval_ms",
        "min_altitude_km",
        "max_altitude_km",
        "min_speed_km_s",
        "max_speed_km_s"
    ]

    for key in required:
        if key not in config:
            raise ValueError(f"Missing configuration: {key}")

    if not isinstance(config["mission_name"], str) or not config["mission_name"].strip():
        raise ValueError("Invalid mission name")

    numeric_keys = [
        "altitude_km",
        "time_step_seconds",
        "animation_interval_ms",
        "min_altitude_km",
        "max_altitude_km",
        "min_speed_km_s",
        "max_speed_km_s"
    ]

    for key in numeric_keys:
        value = config[key]

        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
        ):
            raise ValueError(f"Invalid numerical setting: {key}")

    positive_keys = [
        "altitude_km",
        "time_step_seconds",
        "animation_interval_ms",
        "min_altitude_km",
        "max_altitude_km",
        "min_speed_km_s",
        "max_speed_km_s"
    ]

    for key in positive_keys:
        if config[key] <= 0:
            raise ValueError(f"{key} must be positive")

    if config["min_altitude_km"] > config["max_altitude_km"]:
        raise ValueError("Minimum altitude cannot exceed maximum altitude")

    if config["min_speed_km_s"] > config["max_speed_km_s"]:
        raise ValueError("Minimum speed cannot exceed maximum speed")

    return config

if __name__ == "__main__":
    try:
        settings = load_config()
        print("Configuration loaded successfully")
        print(settings)
    except (ValueError, json.JSONDecodeError) as error:
        print(f"Configuration error: {error}")
    except OSError as error:
        print(f"File error: {error}")
