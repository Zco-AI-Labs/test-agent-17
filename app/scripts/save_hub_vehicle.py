from app.core import hubscape_adk

async def save_hub_vehicle(
    tool_context: hubscape_adk.RemoteContext,
    make: str,
    model: str,
    year: int,
    notes: str = ""
) -> dict:
    """
    Saves a vehicle profile to the hub-scoped garage collection so all hub members can see it.
    Requires the user to be an authenticated hub member.

    Args:
        make: The vehicle manufacturer, e.g. "Ford".
        model: The vehicle model name, e.g. "Explorer".
        year: The model year as a 4-digit integer, e.g. 2023.
        notes: Optional free-text notes about the vehicle, e.g. "Leased, returns March 2025".
    """
    hub_id = tool_context.auth.hub_id
    if not hub_id:
        return {"success": False, "error": "No hub context found. Please use this feature within a hub."}

    doc_id = f"{make.lower()}_{model.lower().replace(' ', '_')}_{year}"
    data = {
        "make": make,
        "model": model,
        "year": year,
        "notes": notes,
        "added_by": tool_context.auth.get_user_id(),
        "added_by_name": tool_context.auth.name,
    }
    tool_context.save("hub", "hub_garage", doc_id, data)
    return {"success": True, "doc_id": doc_id, "message": f"{year} {make} {model} saved to hub garage."}
