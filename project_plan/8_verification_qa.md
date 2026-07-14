## ✅ 8. Verification & QA

### Automated Tests

All tests are located in the `tests/` directory.

```bash
# Run all unit and integration tests
uv run pytest tests/unit tests/integration -v

# Run only car expert agent tests
uv run pytest tests/ -k "car_expert" -v
```

---

### Unit Test Checklist

| Test | Target | Expected Outcome |
| :--- | :--- | :--- |
| `test_compare_cars_two_vehicles` | `compare_cars` | Returns dict with `"vehicles"` list of 2 items and `"widget": "car_comparison_card"`. |
| `test_compare_cars_three_vehicles` | `compare_cars` | Returns dict with `"vehicles"` list of 3 items. |
| `test_get_recommendations_valid` | `get_car_recommendations` | Returns dict with all input params echoed and `"widget": "car_recommendations_card"`. |
| `test_get_recommendations_no_hub` | `get_car_recommendations` | Returns success even without hub context (no hub required). |
| `test_save_hub_vehicle_success` | `save_hub_vehicle` | Returns `{"success": True}` and correct `doc_id` format. |
| `test_save_hub_vehicle_no_hub` | `save_hub_vehicle` | Returns `{"success": False, "error": "No hub context found."}`. |
| `test_list_hub_vehicles_empty` | `list_hub_vehicles` | Returns `{"success": True, "vehicles": []}` when garage is empty. |
| `test_delete_hub_vehicle_success` | `delete_hub_vehicle` | Returns `{"success": True}`. |
| `test_delete_hub_vehicle_no_hub` | `delete_hub_vehicle` | Returns `{"success": False, "error": "No hub context found."}`. |

---

### Manual Verification Checklist (Holodeck / Sandbox)

- [ ] Agent responds correctly to "Compare Toyota RAV4 vs Honda CR-V" in chat UI (widget rendered).
- [ ] Agent responds correctly to same query via SMS simulation (plain text, no markdown).
- [ ] Agent responds correctly via Voice simulation (concise, natural spoken reply).
- [ ] Agent returns top 4 recommendations when budget and use case are specified.
- [ ] "Save to Hub Garage" button on comparison card triggers `save_hub_vehicle` correctly.
- [ ] "Show me the hub garage" lists all saved vehicles in the `hub_garage_card` widget.
- [ ] "Remove" button on hub garage card calls `delete_hub_vehicle` with correct `doc_id`.
- [ ] Agent gracefully redirects off-topic questions (e.g., "Plan my trip to Paris").
- [ ] Agent does not fabricate real-time prices; states estimates are approximate.
- [ ] Hub garage operations fail gracefully when no `hub_id` is in context.
