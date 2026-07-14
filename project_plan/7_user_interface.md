## 🎨 7. User Interface (Lego Block Widgets)

> [!NOTE]
> Widget JSON must be placed as individual `.json` files inside `app/ui/widgets/`. Each file's base name is the `widget_template_id` used in `context.show_widget(widget_template_id, data)`.

---

### Widget 1: `car_comparison_card`

**File:** `app/ui/widgets/car_comparison_card.json`
**Trigger:** Rendered by `compare_cars` tool result.
**Purpose:** Side-by-side spec comparison of two or three vehicles.

```json
{
  "widget_template_id": "car_comparison_card",
  "layout": "comparison_grid",
  "title": "Vehicle Comparison",
  "columns": "{{vehicles}}",
  "rows": [
    { "label": "Starting Price", "field": "price_range" },
    { "label": "City / Hwy MPG", "field": "mpg" },
    { "label": "Horsepower", "field": "horsepower" },
    { "label": "Seating", "field": "seating" },
    { "label": "Cargo (cu ft)", "field": "cargo_volume" },
    { "label": "NHTSA Safety", "field": "safety_rating" },
    { "label": "Key Pros", "field": "pros" }
  ],
  "actions": [
    {
      "label": "Save to Hub Garage",
      "action_id": "save_vehicle_to_hub",
      "style": "primary",
      "payload_fields": ["make", "model", "year"]
    }
  ]
}
```

---

### Widget 2: `car_recommendations_card`

**File:** `app/ui/widgets/car_recommendations_card.json`
**Trigger:** Rendered by `get_car_recommendations` tool result.
**Purpose:** Displays 3–5 recommended vehicles as list tiles with summary info.

```json
{
  "widget_template_id": "car_recommendations_card",
  "layout": "list_tiles",
  "title": "Top Picks for You",
  "subtitle": "Based on your budget of ${{budget}} for {{use_case}}",
  "items": "{{recommendations}}",
  "item_fields": {
    "primary": "model_name",
    "secondary": "price_range",
    "detail": "reason",
    "badge": "mpg_label"
  },
  "actions": [
    {
      "label": "Compare This",
      "action_id": "trigger_comparison",
      "style": "secondary",
      "payload_fields": ["model_name"]
    }
  ]
}
```

---

### Widget 3: `hub_garage_card`

**File:** `app/ui/widgets/hub_garage_card.json`
**Trigger:** Rendered by `list_hub_vehicles` tool result.
**Purpose:** Grid view of all vehicles saved in the hub garage.

```json
{
  "widget_template_id": "hub_garage_card",
  "layout": "card_grid",
  "title": "Hub Garage",
  "subtitle": "Shared vehicles for this hub",
  "items": "{{vehicles}}",
  "item_fields": {
    "primary": "year_make_model",
    "secondary": "notes",
    "meta": "added_by_name"
  },
  "actions": [
    {
      "label": "Remove",
      "action_id": "delete_hub_vehicle",
      "style": "danger",
      "payload_fields": ["doc_id"],
      "confirm": "Are you sure you want to remove this vehicle from the hub garage?"
    }
  ],
  "header_actions": [
    {
      "label": "+ Add Vehicle",
      "action_id": "open_add_vehicle_form",
      "style": "primary"
    }
  ]
}
```
