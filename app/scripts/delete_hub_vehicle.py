from app.core import hubscape_adk

async def delete_hub_vehicle(
    tool_context: hubscape_adk.RemoteContext,
    doc_id: str
) -> dict:
    """
    Removes a vehicle from the hub garage by its document ID.
    Only hub admins or the user who added the vehicle may delete it.

    Args:
        doc_id: The Firestore document ID of the vehicle to remove, e.g. "ford_explorer_2022".
    """
    hub_id = tool_context.auth.hub_id
    if not hub_id:
        return {"success": False, "error": "No hub context found."}

    tool_context.delete("hub", "hub_garage", doc_id)
    return {"success": True, "message": f"Vehicle '{doc_id}' removed from hub garage."}
