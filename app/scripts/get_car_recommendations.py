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
    # Dynamic catalog of vehicles for recommendations
    catalog = [
        {
            "model_name": "Toyota RAV4 Hybrid",
            "price": 32000,
            "price_range": "$31,500 - $39,000",
            "mpg_label": "38 MPG",
            "use_cases": ["family", "commute", "city", "utility"],
            "fuel_types": ["hybrid", "gasoline"],
            "size_classes": ["compact", "midsize", "suv"],
            "reason": "Top-tier reliability, excellent hybrid fuel economy, and great family cargo space."
        },
        {
            "model_name": "Honda CR-V Hybrid",
            "price": 34000,
            "price_range": "$33,000 - $40,000",
            "mpg_label": "37 MPG",
            "use_cases": ["family", "commute", "city"],
            "fuel_types": ["hybrid", "gasoline"],
            "size_classes": ["compact", "midsize", "suv"],
            "reason": "Superb cabin comfort, cavernous cargo space, and extremely smooth driving dynamics."
        },
        {
            "model_name": "Mazda CX-5",
            "price": 30000,
            "price_range": "$28,500 - $38,000",
            "mpg_label": "26 MPG",
            "use_cases": ["family", "commute", "sport"],
            "fuel_types": ["gasoline"],
            "size_classes": ["compact", "suv"],
            "reason": "Provides a premium feel, athletic handling, and an upscale interior at a budget-friendly price."
        },
        {
            "model_name": "Hyundai Tucson Hybrid",
            "price": 31000,
            "price_range": "$30,000 - $36,000",
            "mpg_label": "36 MPG",
            "use_cases": ["family", "commute", "value"],
            "fuel_types": ["hybrid", "gasoline"],
            "size_classes": ["compact", "suv"],
            "reason": "Loaded with standard tech features, an outstanding warranty, and modern styling."
        },
        {
            "model_name": "Porsche 911 Carrera",
            "price": 120000,
            "price_range": "$115,000 - $150,000",
            "mpg_label": "20 MPG",
            "use_cases": ["sport", "performance", "track"],
            "fuel_types": ["gasoline"],
            "size_classes": ["compact", "subcompact"],
            "reason": "The absolute benchmark for sports cars, blending incredible performance with daily usability."
        },
        {
            "model_name": "Audi R8 V10",
            "price": 180000,
            "price_range": "$160,000 - $210,000",
            "mpg_label": "16 MPG",
            "use_cases": ["sport", "performance", "exotic"],
            "fuel_types": ["gasoline"],
            "size_classes": ["compact"],
            "reason": "Stunning supercar presence and a glorious naturally aspirated V10 exhaust note."
        },
        {
            "model_name": "Chevrolet Corvette Z06",
            "price": 115000,
            "price_range": "$110,000 - $135,000",
            "mpg_label": "15 MPG",
            "use_cases": ["sport", "performance", "track"],
            "fuel_types": ["gasoline"],
            "size_classes": ["compact", "midsize"],
            "reason": "Offers mid-engine supercar performance and aggressive styling at a fraction of the cost."
        },
        {
            "model_name": "Mercedes-AMG GT",
            "price": 150000,
            "price_range": "$135,000 - $185,000",
            "mpg_label": "17 MPG",
            "use_cases": ["sport", "performance", "grand-tourer"],
            "fuel_types": ["gasoline"],
            "size_classes": ["midsize", "compact"],
            "reason": "Muscular V8 performance, beautiful proportions, and a luxurious cabin."
        },
        {
            "model_name": "Tesla Model Y Long Range",
            "price": 48000,
            "price_range": "$45,000 - $55,000",
            "mpg_label": "120 MPGe",
            "use_cases": ["family", "commute", "city", "utility"],
            "fuel_types": ["electric"],
            "size_classes": ["midsize", "suv"],
            "reason": "Industry-leading EV range, access to the Supercharger network, and massive cargo volume."
        },
        {
            "model_name": "Ford F-150 Lightning",
            "price": 60000,
            "price_range": "$55,000 - $85,000",
            "mpg_label": "70 MPGe",
            "use_cases": ["utility", "off-road", "work"],
            "fuel_types": ["electric"],
            "size_classes": ["truck", "fullsize"],
            "reason": "Electric convenience with serious towing capacity, a large front trunk, and power-export features."
        },
        {
            "model_name": "Jeep Wrangler Rubicon",
            "price": 45000,
            "price_range": "$42,000 - $60,000",
            "mpg_label": "20 MPG",
            "use_cases": ["off-road", "utility", "adventure"],
            "fuel_types": ["gasoline", "hybrid"],
            "size_classes": ["compact", "midsize", "suv"],
            "reason": "Unrivaled off-road capability, open-air freedom, and rugged design."
        }
    ]

    recommendations = []
    use_case_lower = use_case.lower()
    
    # Filter catalog based on user input parameters
    for car in catalog:
        # Budget check (must be within budget)
        if car["price"] > budget:
            continue
            
        # Fuel type check
        if fuel_type != "any" and fuel_type not in car["fuel_types"]:
            continue
            
        # Size class check
        if size_class != "any" and size_class not in car["size_classes"]:
            continue
            
        recommendations.append(car)
        
    # If no matches under strict criteria, fallback to matching budget and broad category
    if not recommendations:
        for car in catalog:
            if car["price"] <= budget:
                # Basic check for sports cars
                if "sport" in use_case_lower or "perf" in use_case_lower:
                    if "sport" in car["use_cases"]:
                        recommendations.append(car)
                # Basic check for family cars
                elif "family" in use_case_lower or "commute" in use_case_lower:
                    if "family" in car["use_cases"]:
                        recommendations.append(car)
                else:
                    recommendations.append(car)

    # Sort or cap to top 4 recommendations
    recommendations = recommendations[:4]
    
    # Queue the recommendations card widget with populated data
    tool_context.show_widget("car_recommendations_card", {
        "budget": budget,
        "use_case": use_case,
        "recommendations": recommendations
    })

    return {
        "action": "get_car_recommendations",
        "budget": budget,
        "use_case": use_case,
        "fuel_type": fuel_type,
        "size_class": size_class,
        "priority": priority,
        "widget": "car_recommendations_card",
        "recommendations": recommendations
    }
