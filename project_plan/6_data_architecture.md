## 🗄️ 6. Data Architecture

### Data Scope Summary

| Scope | Collection | Purpose |
| :--- | :--- | :--- |
| `hub` | `hub_garage` | Stores shared vehicle profiles visible to all hub members. |

> [!NOTE]
> v1.0 uses **hub scope only**. There is no user-scoped or org-scoped data in this version. The agent does not store comparison results or recommendation history persistently.

---

### Hub-Scoped Collection: `hub_garage`

**Collection path (resolved by ADK):** `hubs/{hub_id}/agents/car_expert_agent/hub_garage/{doc_id}`

#### Document ID Format
```
{make_lowercase}_{model_lowercase_underscored}_{year}
```
**Examples:**
- `toyota_camry_2024`
- `ford_f-150_2023`
- `tesla_model_3_2024`

> [!IMPORTANT]
> If a user adds the same make/model/year twice, the document will be **merged/overwritten** (upsert behavior from `save_agent_data`). This is intentional to avoid duplicate entries.

#### Document Schema

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `make` | `string` | Vehicle manufacturer. | `"Toyota"` |
| `model` | `string` | Vehicle model name. | `"Camry"` |
| `year` | `integer` | 4-digit model year. | `2024` |
| `notes` | `string` | Optional free-text notes. | `"Company fleet vehicle"` |
| `added_by` | `string` | User UUID who added the vehicle. | `"usr_abc123"` |
| `added_by_name` | `string` | Display name of the user who added it. | `"Alex Smith"` |
| `created_at` | `timestamp` | Auto-injected by `save_agent_data` auditing. | *(auto)* |
| `updated_at` | `timestamp` | Auto-injected by `save_agent_data` auditing. | *(auto)* |

---

### ADK Data Access Pattern

All reads and writes use the high-level ADK Firestore helpers:

```python
# Write (upsert)
await context.save_agent_data("hub", "hub_garage", doc_id, data)

# Read all
vehicles = await context.list_agent_data("hub", "hub_garage")

# Delete
await context.delete_agent_data("hub", "hub_garage", doc_id)
```
