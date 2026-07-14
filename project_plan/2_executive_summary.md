## 📄 2. Executive Summary

### Product Goal
The **Car Expert Agent** is a conversational AI agent deployed on the Hubscape platform. Its primary purpose is to serve as an authoritative, always-available automotive advisor. Users can ask the agent to compare car models, receive personalized buying advice based on their budget and needs, and explore detailed vehicle specifications—all through natural conversation.

The agent stores vehicle profiles and saved comparisons at the **Hub scope**, enabling teams (e.g., fleet managers, dealership staff, or automotive groups) to share and reference vehicle data collaboratively.

### High-Level Success Criteria
1. A user can ask the agent to compare two or more car models and receive a clear, structured response (or widget card in UI mode).
2. A user can specify their budget and use case (e.g., family SUV under $40K) and receive ranked buying recommendations.
3. Hub members can save vehicles to a shared hub "garage" and retrieve them in future sessions.
4. The agent gracefully handles voice and SMS interactions with plain-text, concise replies free of markdown or JSON.
5. All hub-scoped data writes are gated behind appropriate hub permissions.

### Out of Scope (v1.0)
- External API integrations (e.g., Edmunds, CarMD, NHTSA) — relies on LLM training knowledge only.
- Real-time pricing or inventory lookups.
- VIN decoding.
