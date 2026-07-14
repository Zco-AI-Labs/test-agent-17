from app.core import hubscape_adk

async def compare_cars(
    tool_context: hubscape_adk.RemoteContext,
    vehicle_a: str,
    vehicle_b: str,
    vehicle_c: str = ""
) -> dict:
    """
    Compares two (or optionally three) car models side-by-side across key attributes
    including price range, MPG, horsepower, cargo volume, seating capacity, and safety.

    Args:
        vehicle_a: The first vehicle to compare, e.g. "Toyota Camry 2024".
        vehicle_b: The second vehicle to compare, e.g. "Honda Accord 2024".
        vehicle_c: An optional third vehicle to include in the comparison. Leave empty if not needed.

    Returns:
        A dict containing comparison data for each vehicle and a recommendation summary.
    """
    vehicles = [vehicle_a, vehicle_b]
    if vehicle_c:
        vehicles.append(vehicle_c)

    return {
        "action": "compare_cars",
        "vehicles": vehicles,
        "widget": "car_comparison_card",
    }
