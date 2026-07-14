from app.core import hubscape_adk

async def show_rmv_portal(tool_context: hubscape_adk.RemoteContext) -> dict:
    """
    Triggers the Massachusetts RMV portal link widget, providing a direct button
    to visit the Registry of Motor Vehicles services website.

    Returns:
        A dict confirmation payload with the widget identifier.
    """
    # Enqueue showing the RMV link card widget
    tool_context.show_widget("rmv_link_card")
    return {
        "success": True,
        "widget": "rmv_link_card",
        "message": "Displaying Massachusetts RMV link card."
    }
