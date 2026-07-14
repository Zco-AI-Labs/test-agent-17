## 📋 9. Implementation Tasks

This checklist maps the precise, step-by-step coding and configuration changes required to implement the Car Expert Agent. Mark tasks as `[ ]` (unstarted), `[/]` (in progress), or `[x]` (completed) as you execute the implementation.

---

### Phase 1: Configuration & Metadata

- [ ] In `app/agent.py`: Set `name="car_expert_agent"` on the `AdkAgent` instance.
- [ ] In `app/agent.py`: Set `description="An AI automotive expert that compares cars, provides buying recommendations, and manages a shared hub garage."` on the `AdkAgent` instance.

---

### Phase 2: System Instructions

- [ ] Replace the contents of `app/SKILL.md` with the system instructions defined in `5_architecture_capabilities.md` (Section: System Instructions).
- [ ] Ensure the YAML frontmatter sets `name: car-expert-agent` and an accurate `description`.

---

### Phase 3: Tool Implementation

Implement each tool as a standalone Python file under `app/scripts/`:

- [ ] Create `app/scripts/compare_cars.py` — implement `compare_cars(tool_context, vehicle_a, vehicle_b, vehicle_c="")` per the signature in Section 5.
- [ ] Create `app/scripts/get_car_recommendations.py` — implement `get_car_recommendations(tool_context, budget, use_case, fuel_type="any", size_class="any", priority="balanced")` per the signature in Section 5.
- [ ] Create `app/scripts/save_hub_vehicle.py` — implement `save_hub_vehicle(tool_context, make, model, year, notes="")` with hub-scope Firestore write using `context.save_agent_data("hub", "hub_garage", doc_id, data)`.
- [ ] Create `app/scripts/list_hub_vehicles.py` — implement `list_hub_vehicles(tool_context)` with hub-scope Firestore read using `context.list_agent_data("hub", "hub_garage")`.
- [ ] Create `app/scripts/delete_hub_vehicle.py` — implement `delete_hub_vehicle(tool_context, doc_id)` with hub-scope Firestore delete using `context.delete_agent_data("hub", "hub_garage", doc_id)`.
- [ ] Verify all tools use `async def` and include complete docstrings with `Args:` section (required for ADK function declaration parsing).
- [ ] Verify all tools handle missing `hub_id` gracefully (return `{"success": False, "error": "..."}` instead of raising).

---

### Phase 4: UI / Widget Definitions

- [ ] Create `app/ui/widgets/car_comparison_card.json` with the Lego block JSON defined in Section 7.
- [ ] Create `app/ui/widgets/car_recommendations_card.json` with the Lego block JSON defined in Section 7.
- [ ] Create `app/ui/widgets/hub_garage_card.json` with the Lego block JSON defined in Section 7.
- [ ] Verify all widget JSON files parse without errors (valid JSON syntax).
- [ ] Cross-reference widget field names against `docs/UI_ELEMENTS.md` to confirm layout type compatibility.

---

### Phase 5: Verification & Testing

- [ ] Create unit tests in `tests/unit/test_compare_cars.py` covering happy path and edge cases.
- [ ] Create unit tests in `tests/unit/test_get_car_recommendations.py` covering valid and boundary inputs.
- [ ] Create unit tests in `tests/unit/test_hub_garage.py` covering all CRUD operations (save, list, delete) with and without hub context.
- [ ] Run `uv run pytest tests/unit -v` and confirm all tests pass.
- [ ] Perform manual sandbox testing via Holodeck (`http://localhost:8090`) against the manual verification checklist in Section 8.
- [ ] Confirm UI mode renders all three widget cards correctly.
- [ ] Confirm SMS simulation returns plain-text responses for all 4 features.
- [ ] Confirm Voice simulation returns concise, natural spoken responses for all 4 features.
