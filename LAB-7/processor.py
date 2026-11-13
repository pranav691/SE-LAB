import math

MAX_PETS = 1000
MAX_MINS = 24 * 60


def parse_walk_schedule(schedule_spec):
    """Parse 'pets-mins-weekend' (e.g. '2-30-YES'). Returns a summary string,
    or an 'Invalid schedule' message if the input is malformed."""
    if not isinstance(schedule_spec, str):
        return "Invalid schedule: input must be text"
    parts = schedule_spec.strip().split('-')
    if len(parts) != 3:
        return "Invalid schedule: expected format pets-mins-YES/NO"
    pets_str, mins_str, weekend_str = (p.strip() for p in parts)
    try:
        pets = int(pets_str)
        mins = int(mins_str)
    except (ValueError, OverflowError):
        return "Invalid schedule: pets and mins must be whole numbers"
    if not (1 <= pets <= MAX_PETS):
        return f"Invalid schedule: pets must be between 1 and {MAX_PETS}"
    if not (1 <= mins <= MAX_MINS):
        return f"Invalid schedule: mins must be between 1 and {MAX_MINS}"
    weekend_map = {"YES": 15.0, "NO": 0.0}
    weekend_fee = weekend_map.get(weekend_str.upper())
    if weekend_fee is None:
        return "Invalid schedule: weekend flag must be YES or NO"
    base_fee = 20.0 if mins <= 30 else 35.0
    total = base_fee + (pets * 5.0) + weekend_fee
    return f"Walk: {pets} pets, {mins} mins - Total ${total:.2f}"


def compute_pace_per_pet(walk_metrics_str):
    """Parse 'mins/pets' and return minutes per pet, or None if invalid."""
    if not isinstance(walk_metrics_str, str):
        return None
    parts = walk_metrics_str.split('/')
    if len(parts) != 2:
        return None
    try:
        mins = float(parts[0])
        pets = float(parts[1])
    except (ValueError, OverflowError):
        return None
    if not (math.isfinite(mins) and math.isfinite(pets)):
        return None
    if mins < 0 or pets <= 0:
        return None
    try:
        pace = mins / pets
    except (ZeroDivisionError, OverflowError):
        return None
    if not math.isfinite(pace):
        return None
    return round(pace, 2)


def lookup_temperament_surcharge(temperament_code):
    """Return the surcharge for a temperament code, or None if unknown."""
    if not isinstance(temperament_code, str):
        return None
    prefix = temperament_code.strip().upper()[:3]
    surcharges = {
        "CAL": 0.0,
        "PLY": 5.0,
        "REA": 12.0,
        "AGG": 20.0
    }
    return surcharges.get(prefix)


def main():
    print("==== Running parse_walk_schedule ====")
    s_input = input("Enter schedule (e.g. 2-30-YES): ")
    print(parse_walk_schedule(s_input))

    print("\n==== Running compute_pace_per_pet ====")
    p_input = input("Enter minutes/pets (e.g. 45/3): ")
    pace = compute_pace_per_pet(p_input)
    print("Pace (min/pet):", pace if pace is not None else "Invalid input (use mins/pets, pets > 0)")

    print("\n==== Running lookup_temperament_surcharge ====")
    t_input = input("Enter temperament code (e.g. CALM, PLAYFUL, AGGRESSIVE): ")
    surcharge = lookup_temperament_surcharge(t_input)
    print("Surcharge: $", surcharge if surcharge is not None else "Unknown temperament code")

if __name__ == "__main__":
    main()