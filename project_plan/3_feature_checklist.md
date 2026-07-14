## 📂 3. Feature Checklist & Interaction Modes

---

### Feature 1: Car Comparison

*   **Description:** Compares two or more car models side-by-side across key specs (price range, MPG, horsepower, seating, cargo, safety rating, pros/cons). Returns a structured comparison the user can read or save.
*   **Visual Interaction Mode:**
    *   *Trigger:* User sends a message like "Compare the Toyota RAV4 vs Honda CR-V" or "Which is better: Tesla Model 3 or BMW 3 Series?"
    *   *UI Rendered:* `car_comparison_card` widget — a two-column table card showing each vehicle's key attributes side-by-side.
    *   *Form Actions:* User may click "Save to Hub Garage" button on the card to persist the comparison to hub scope.
*   **Non-Visual Interaction Mode (SMS/Voice Fallback):**
    *   *SMS Transcript Flow:* Agent replies with a plain-text bulleted list comparing key stats (price, MPG, HP) for each vehicle.
    *   *Voice/Phone Flow:* Agent reads a concise verbal summary (e.g., "The RAV4 gets better fuel economy while the CR-V has a more spacious interior. Both are priced similarly around thirty thousand dollars.")
    *   *Natural Language Parameters Extracted:* `vehicle_a`, `vehicle_b` (and optionally `vehicle_c`), comparison attributes.
*   **Acceptance Criteria (Given-When-Then):**
    *   *Scenario A (Happy Path):*
        *   **GIVEN** A user is authenticated and sends a comparison query with two valid vehicle names.
        *   **WHEN** The agent calls `compare_cars` with `vehicle_a` and `vehicle_b`.
        *   **THEN** The agent returns a structured comparison (widget in UI mode, plain text in SMS/Voice) with at least 5 spec categories.
    *   *Scenario B (Fallback/Error Path):*
        *   **GIVEN** The user mentions a vehicle the LLM has insufficient knowledge about (e.g., obscure regional model).
        *   **WHEN** The agent calls `compare_cars`.
        *   **THEN** The agent transparently states the limitation and offers to compare with better-known alternatives.

---

### Feature 2: Personalized Buying Advice

*   **Description:** Given a user's stated budget, use case (family, commute, off-road, sport, etc.), and preferences (fuel type, size class), the agent produces a ranked shortlist of recommended vehicles with reasoning.
*   **Visual Interaction Mode:**
    *   *Trigger:* User sends "What car should I buy under $35,000 for a family of four?" or "I need an electric SUV under $50K."
    *   *UI Rendered:* A list card `car_recommendations_card` displaying 3–5 recommended vehicles with thumbnail, price range, and a brief pros summary.
    *   *Form Actions:* Each recommendation card has a "Compare This" button that triggers the comparison feature.
*   **Non-Visual Interaction Mode (SMS/Voice Fallback):**
    *   *SMS Transcript Flow:* Agent replies with a numbered list of 3 recommended vehicles with one-sentence reasoning each.
    *   *Voice/Phone Flow:* Agent verbally presents top 3 picks and asks if the user wants more detail on any of them.
    *   *Natural Language Parameters Extracted:* `budget`, `use_case`, `fuel_type`, `size_class`, `priority` (e.g., safety, fuel economy, cargo).
*   **Acceptance Criteria (Given-When-Then):**
    *   *Scenario A (Happy Path):*
        *   **GIVEN** A user provides a budget and use case in their query.
        *   **WHEN** The agent calls `get_car_recommendations` with the extracted parameters.
        *   **THEN** The agent returns 3–5 ranked recommendations with justification for each.
    *   *Scenario B (Fallback/Error Path):*
        *   **GIVEN** The user provides a budget that is unusually low (e.g., under $5,000) or contradictory constraints.
        *   **WHEN** The agent calls `get_car_recommendations`.
        *   **THEN** The agent flags the constraint issue, sets realistic expectations, and still provides the best available suggestions within the constraints.

---

### Feature 3: Hub Garage (Shared Vehicle Profiles)

*   **Description:** Hub members can save vehicle profiles (make, model, year, notes) to a shared "hub garage" collection. Any member of the hub can view, update, or remove vehicles from the hub garage.
*   **Visual Interaction Mode:**
    *   *Trigger:* User sends "Add a 2023 Ford F-150 to our hub garage" or "Show me the hub garage."
    *   *UI Rendered:* `hub_garage_card` widget — a grid of saved vehicle profile cards, each showing make, model, year, and notes.
    *   *Form Actions:* "Add Vehicle" form with fields for make, model, year, and notes. "Remove" button on each card.
*   **Non-Visual Interaction Mode (SMS/Voice Fallback):**
    *   *SMS Transcript Flow:* Agent confirms save with "Added 2023 Ford F-150 to the hub garage." or lists vehicles as a numbered text list.
    *   *Voice/Phone Flow:* Agent reads back confirmed additions or lists the first 5 hub garage vehicles verbally.
    *   *Natural Language Parameters Extracted:* `make`, `model`, `year`, `notes`.
*   **Acceptance Criteria (Given-When-Then):**
    *   *Scenario A (Happy Path):*
        *   **GIVEN** A user with hub membership requests to save a vehicle.
        *   **WHEN** The agent calls `save_hub_vehicle` with valid make/model/year.
        *   **THEN** The vehicle is persisted to hub-scoped Firestore and a confirmation is returned.
    *   *Scenario B (Fallback/Error Path):*
        *   **GIVEN** A user without hub membership or insufficient permissions attempts to add a vehicle.
        *   **WHEN** The agent checks `context.auth.has_permission("HUB_MEMBER")`.
        *   **THEN** The agent returns an error message explaining the permission requirement.

---

### Feature 4: Conversational Car Q&A

*   **Description:** A general-purpose Q&A mode where users can ask any automotive question — maintenance tips, car history, terminology explanations, towing capacity, etc. — and receive an expert-level answer.
*   **Visual Interaction Mode:**
    *   *Trigger:* Any open-ended car question not matching structured features above (e.g., "What does torque mean?" or "Is diesel worth it for highway driving?").
    *   *UI Rendered:* Standard markdown text response (no custom widget needed).
    *   *Form Actions:* None.
*   **Non-Visual Interaction Mode (SMS/Voice Fallback):**
    *   *SMS Transcript Flow:* Concise plain-text answer, under 160 characters if possible, with an offer to elaborate.
    *   *Voice/Phone Flow:* Spoken conversational answer, 2–3 sentences max.
    *   *Natural Language Parameters Extracted:* Topic extracted from query (no tool call required; LLM responds directly).
*   **Acceptance Criteria (Given-When-Then):**
    *   *Scenario A (Happy Path):*
        *   **GIVEN** A user asks a general car question.
        *   **WHEN** The agent evaluates the query and determines no tool call is needed.
        *   **THEN** The agent replies directly with an accurate, expert-level answer.
    *   *Scenario B (Fallback/Error Path):*
        *   **GIVEN** The user asks something completely outside the automotive domain (e.g., "Plan my vacation").
        *   **WHEN** The agent receives the query.
        *   **THEN** The agent politely redirects: "I'm a car expert and can only help with automotive topics."
