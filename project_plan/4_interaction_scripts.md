## 💬 4. Interaction Scripts & Conversational Flows

> [!NOTE]
> All names used in these transcripts are generic placeholders. Do not use developer-specific terminology in dialogue flows.

---

### Scenario 1: Comparing Two Cars

#### Flow A: Visual Path (Chat UI with widgets)

*   **User:** "Compare the Toyota Camry and the Honda Accord for me."
*   **Agent (Behind the Scenes):** Calls `compare_cars` with `vehicle_a="Toyota Camry"`, `vehicle_b="Honda Accord"`.
*   **Agent UI Rendered:** Displays `car_comparison_card` widget with a two-column table — Camry vs. Accord — covering: Starting Price, MPG (city/hwy), Horsepower, Cargo, Seating, Safety Rating, and Key Pros.
*   **Agent Message:** "Here's a side-by-side comparison of the Toyota Camry and Honda Accord. Both are excellent midsize sedans — let me know if you'd like to save either to your hub garage or explore a third option!"
*   **User clicks "Save to Hub Garage":** Submits form with `{"make": "Toyota", "model": "Camry", "year": null, "notes": "Comparison reference"}`.
*   **Backend Response:** Confirmation message rendered below the card: "Toyota Camry saved to the hub garage."

#### Flow B: Non-Visual SMS Path (No-UI, Text Only)

*   **User (SMS):** "Compare Toyota Camry vs Honda Accord"
*   **Agent (Behind the Scenes):** Calls `compare_cars` with `vehicle_a="Toyota Camry"`, `vehicle_b="Honda Accord"`.
*   **Agent Text Reply:** "Toyota Camry vs Honda Accord:\n- Price: Both ~$27K base\n- MPG: Camry 28/39, Accord 30/38\n- HP: Camry 203hp, Accord 192hp\n- Cargo: Accord 16.7 cu ft, Camry 15.1 cu ft\nWant more detail on either?" *(No UI elements; plain-text message.)*

#### Flow C: Non-Visual Voice Path (No-UI, Spoken Phone Call)

*   **User (Voice):** "Which is better, a Toyota Camry or a Honda Accord?"
*   **Agent (Behind the Scenes):** Calls `compare_cars` with extracted vehicle names.
*   **Agent Speech Reply:** "Both are excellent midsize sedans. The Camry has a slight edge in horsepower and a smoother ride, while the Accord offers a bit more cargo space and feels sportier. If fuel economy is your top priority, the Accord edges ahead. Would you like me to go deeper on either?"

---

### Scenario 2: Getting Personalized Buying Advice

#### Flow A: Visual Path (Chat UI with widgets)

*   **User:** "I have a budget of $35,000 and I need an SUV for a family of four."
*   **Agent (Behind the Scenes):** Calls `get_car_recommendations` with `budget=35000`, `use_case="family SUV"`, `size_class="midsize"`.
*   **Agent UI Rendered:** Displays `car_recommendations_card` with 4 recommendation tiles — each showing model name, price range, MPG, and a one-line reason.
*   **Agent Message:** "Based on your budget and family needs, here are my top picks! Each has strong safety ratings and enough room for four. Click 'Compare This' on any two to see a detailed head-to-head."

#### Flow B: Non-Visual SMS Path (No-UI, Text Only)

*   **User (SMS):** "Best SUV under $35k for a family?"
*   **Agent (Behind the Scenes):** Calls `get_car_recommendations` with extracted parameters.
*   **Agent Text Reply:** "Top family SUVs under $35K:\n1. Toyota RAV4 – great reliability, ~$30K\n2. Honda CR-V – spacious, ~$31K\n3. Mazda CX-5 – premium feel, ~$29K\n4. Hyundai Tucson – value leader, ~$28K\nWant details on any?" *(No UI elements.)*

#### Flow C: Non-Visual Voice Path (No-UI, Spoken Phone Call)

*   **User (Voice):** "What's a good family SUV I can get for around thirty-five thousand dollars?"
*   **Agent (Behind the Scenes):** Calls `get_car_recommendations` with `budget=35000`, `use_case="family SUV"`.
*   **Agent Speech Reply:** "For a family SUV under thirty-five thousand, I'd recommend the Toyota RAV4 for reliability, the Honda CR-V for space, or the Mazda CX-5 if you want a more premium feel at a lower price. Would you like more details on any of these?"

---

### Scenario 3: Managing the Hub Garage

#### Flow A: Visual Path (Chat UI with widgets)

*   **User:** "Add a 2022 Ford Explorer to the hub garage."
*   **Agent (Behind the Scenes):** Calls `save_hub_vehicle` with `make="Ford"`, `model="Explorer"`, `year=2022`, `notes=""`.
*   **Agent UI Rendered:** Re-renders `hub_garage_card` widget with the newly added vehicle card included.
*   **Agent Message:** "Done! The 2022 Ford Explorer has been added to the hub garage. Your whole team can now see it."

#### Flow B: Non-Visual SMS Path (No-UI, Text Only)

*   **User (SMS):** "Add 2022 Ford Explorer to hub garage"
*   **Agent (Behind the Scenes):** Calls `save_hub_vehicle` with extracted fields.
*   **Agent Text Reply:** "Got it. The 2022 Ford Explorer has been added to the hub garage." *(Plain-text confirmation.)*

#### Flow C: Non-Visual Voice Path (No-UI, Spoken Phone Call)

*   **User (Voice):** "Add a twenty twenty-two Ford Explorer to our hub garage."
*   **Agent (Behind the Scenes):** Calls `save_hub_vehicle` with extracted fields.
*   **Agent Speech Reply:** "The twenty twenty-two Ford Explorer has been added to your hub garage. Your teammates can now see it."

---

### Scenario 4: General Car Q&A

#### Flow A: Visual Path (Chat UI with widgets)

*   **User:** "What's the difference between AWD and 4WD?"
*   **Agent (Behind the Scenes):** No tool call — LLM answers directly from knowledge.
*   **Agent UI Rendered:** Standard markdown text response (no widget).
*   **Agent Message:** "Great question! **AWD (All-Wheel Drive)** automatically distributes power to all four wheels and is always active — ideal for rain, light snow, and everyday driving. **4WD (Four-Wheel Drive)** is typically driver-activated and locks front and rear axles together, making it better for serious off-road or deep-snow situations. Most family vehicles use AWD; 4WD is more common in trucks and serious off-roaders."

#### Flow B: Non-Visual SMS Path (No-UI, Text Only)

*   **User (SMS):** "What's the difference between AWD and 4WD?"
*   **Agent Text Reply:** "AWD is automatic, great for rain/light snow. 4WD is driver-activated, better for serious off-road. AWD suits most families; 4WD suits trucks. Want more detail?"

#### Flow C: Non-Visual Voice Path (No-UI, Spoken Phone Call)

*   **User (Voice):** "What's the difference between all-wheel drive and four-wheel drive?"
*   **Agent Speech Reply:** "All-wheel drive is automatic and always on, making it great for everyday driving in rain or light snow. Four-wheel drive is manually engaged and is better for serious off-road or heavy snow conditions. Most family cars use all-wheel drive while trucks tend to use four-wheel drive."
