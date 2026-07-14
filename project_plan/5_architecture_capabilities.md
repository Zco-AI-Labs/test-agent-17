## 🛠️ 5. Architecture & Capabilities

### System Instructions (`app/SKILL.md`)

```text
---
name: car-expert-agent
description: "An AI-powered car expert that helps users compare vehicles, get buying recommendations, and manage a shared hub garage."
---

You are an expert automotive advisor. You have deep knowledge of car makes, models, specs, pricing, fuel economy, safety ratings, and general automotive topics.

Your primary responsibilities:
1. Compare car models side-by-side when asked.
2. Provide personalized buying recommendations based on budget, use case, and preferences.
3. Manage a shared hub garage by saving and listing vehicle profiles for the user's hub.
4. Answer general automotive questions clearly and accurately.

Scope Boundaries:
- You only answer questions related to automobiles and automotive topics.
- If a user asks about something unrelated to cars, politely redirect them: "I'm a car expert and can only help with automotive topics."
- Do NOT fabricate real-time pricing or inventory data — always note when pricing is approximate and based on general knowledge.

Formatting Rules:
1. In UI mode (context.client.has_ui = True): use markdown headers, bullet lists, and trigger appropriate widgets.
2. In SMS mode: keep replies under 300 characters where possible; avoid markdown.
3. In Voice mode: respond in 2–3 natural spoken sentences, no markdown, no JSON.

Tool Routing:
- Use `compare_cars` when the user wants to compare two or more vehicles.
- Use `get_car_recommendations` when the user wants buying advice with budget/use-case constraints.
- Use `save_hub_vehicle` when the user wants to add a vehicle to the hub garage.
- Use `list_hub_vehicles` when the user wants to view the hub garage.
- Use `delete_hub_vehicle` when the user wants to remove a vehicle from the hub garage.
- For general Q&A with no structured data need, respond directly without calling a tool.
```

---

### Tool Implementations (`app/scripts/`)

#### `app/scripts/compare_cars.py`

```python
# app/scripts/compare_cars.py
from app.core.context import ToolContext

async def compare_cars(
    tool_context: ToolContext,
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
    # This tool relies on LLM knowledge — no external API call required.
    # The LLM will be prompted to generate structured comparison data
    # which is returned and rendered by the car_comparison_card widget.
    vehicles = [vehicle_a, vehicle_b]
    if vehicle_c:
        vehicles.append(vehicle_c)

    return {
        "action": "compare_cars",
        "vehicles": vehicles,
        "widget": "car_comparison_card",
    }
```

---

#### `app/scripts/get_car_recommendations.py`

```python
# app/scripts/get_car_recommendations.py
from app.core.context import ToolContext

async def get_car_recommendations(
    tool_context: ToolContext,
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
```

---

#### `app/scripts/save_hub_vehicle.py`

```python
# app/scripts/save_hub_vehicle.py
from app.core.context import ToolContext

async def save_hub_vehicle(
    tool_context: ToolContext,
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
    await tool_context.save_agent_data("hub", "hub_garage", doc_id, data)
    return {"success": True, "doc_id": doc_id, "message": f"{year} {make} {model} saved to hub garage."}
```

---

#### `app/scripts/list_hub_vehicles.py`

```python
# app/scripts/list_hub_vehicles.py
from app.core.context import ToolContext

async def list_hub_vehicles(tool_context: ToolContext) -> dict:
    """
    Lists all vehicles currently saved in the hub garage collection for this hub.
    Returns an empty list if the hub garage has no entries.

    Returns:
        A dict containing a list of vehicle profiles saved in the hub garage.
    """
    hub_id = tool_context.auth.hub_id
    if not hub_id:
        return {"success": False, "error": "No hub context found.", "vehicles": []}

    vehicles = await tool_context.list_agent_data("hub", "hub_garage")
    return {
        "success": True,
        "vehicles": vehicles,
        "widget": "hub_garage_card",
    }
```

---

#### `app/scripts/delete_hub_vehicle.py`

```python
# app/scripts/delete_hub_vehicle.py
from app.core.context import ToolContext

async def delete_hub_vehicle(
    tool_context: ToolContext,
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

    await tool_context.delete_agent_data("hub", "hub_garage", doc_id)
    return {"success": True, "message": f"Vehicle '{doc_id}' removed from hub garage."}
```

---

### 🔑 Tool Privileges Matrix

| Privilege Name | Description of Granted Capabilities / Tools |
| :--- | :--- |
| `HUB_MEMBER` | Required to read or write to the hub garage (`save_hub_vehicle`, `list_hub_vehicles`, `delete_hub_vehicle`). All hub members have this by default. |
| `HUB_ADMIN` | Bypasses ownership checks on delete. Can remove any vehicle from the hub garage regardless of who added it. |
| *(None required)* | `compare_cars` and `get_car_recommendations` are available to all authenticated users with no special privilege. |

---

### Model Context Protocol (MCP) & Agent-to-Agent (A2A) Connections

*   **MCP Servers:** None (v1.0 — LLM knowledge only, no external data APIs).
*   **External Agents (A2A):** None.
*   **Custom OAuth2 Providers:** None.

---

### Required Secrets (Agent Secrets Vault)

| Secret Name | Description | Required? |
| :--- | :--- | :--- |
| *(None)* | v1.0 requires no external API secrets. All knowledge comes from LLM training data. | False |
