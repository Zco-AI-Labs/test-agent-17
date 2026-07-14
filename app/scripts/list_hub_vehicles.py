from app.core import hubscape_adk

async def list_hub_vehicles(tool_context: hubscape_adk.RemoteContext) -> dict:
    """
    Lists all vehicles currently saved in the hub garage collection for this hub.
    Returns an empty list if the hub garage has no entries.

    Returns:
        A dict containing a list of vehicle profiles saved in the hub garage.
    """
    hub_id = tool_context.auth.hub_id
    if not hub_id:
        return {"success": False, "error": "No hub context found.", "vehicles": []}

    vehicles = tool_context.list("hub", "hub_garage")
    
    # Format vehicles for rendering inside the hub_garage_card widget
    for v in vehicles:
        v["year_make_model"] = f"{v.get('year', '')} {v.get('make', '')} {v.get('model', '')}".strip()
        v["added_by_name"] = v.get("created_by", "Member")
        
    # Queue the hub garage card widget
    tool_context.show_widget("hub_garage_card", {"vehicles": vehicles})
    
    return {
        "success": True,
        "vehicles": vehicles,
        "widget": "hub_garage_card",
    }
