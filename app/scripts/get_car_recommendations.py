from app.core import hubscape_adk

async def get_car_recommendations(
    tool_context: hubscape_adk.RemoteContext,
    budget: int,
    use_case: str,
    fuel_type: str = "any",
    size_class: str = "any",
    priority: str = "balanced"
) -> dict:
    """
    Returns a ranked list of vehicle recommendations based on the user's budget,
    intended use case, preferred fuel type, size class, and optimization priority.

    Args:
        budget: Maximum budget in USD (e.g. 35000).
        use_case: The primary purpose of the vehicle, e.g. "family commute", "off-road", "sport", "city driving".
        fuel_type: Preferred fuel type. One of: "gasoline", "hybrid", "electric", "diesel", "any".
        size_class: Preferred vehicle size. One of: "subcompact", "compact", "midsize", "fullsize", "suv", "truck", "minivan", "any".
        priority: What the user values most. One of: "safety", "fuel_economy", "performance", "cargo", "value", "balanced".

    Returns:
        A dict containing a ranked list of recommended vehicles with justifications.
    """
    return {
        "action": "get_car_recommendations",
        "budget": budget,
        "use_case": use_case,
        "fuel_type": fuel_type,
        "size_class": size_class,
        "priority": priority,
        "widget": "car_recommendations_card",
    }
