# Decisions

## Decision 1

- **Chose:** A layered Streamlit architecture with separate pages and service modules.
- **Rejected:** Putting database queries and all application logic directly inside the Streamlit pages.
- **Why:** Separating page/UI logic from database and business logic made the project easier to organize, debug, and extend. Manager and staff functionality could also be kept separate while sharing common utilities.

## Decision 2

- **Chose:** Separate manager and warehouse staff functionality into different pages and service modules.
- **Rejected:** Using one set of pages with every feature visible to every user and relying only on UI controls to restrict access.
- **Why:** Managers and staff have significantly different permissions. Separating their interfaces makes the intended workflow clearer, while service-layer checks provide actual permission enforcement instead of relying only on hidden buttons.

## Decision 3

- **Chose:** Use the stock movement ledger as the source of truth and derive current stock from stock movement data.
- **Rejected:** Storing and manually updating a separate current-stock value whenever a movement occurs.
- **Why:** A movement-based approach preserves the history of inventory changes and avoids having multiple independently maintained stock values that could become inconsistent.

## Decision 4

- **Chose:** Keep item history append-only and prevent existing history records from being edited or deleted.
- **Rejected:** Allowing managers or staff to modify or delete historical records after they were created.
- **Why:** Inventory history needs to remain trustworthy. Changes are recorded as new history entries so that the previous state and the user responsible for the change remain available.

## Decision 5

- **Chose:** Preserve existing working service functions when adding new functionality and create separate functions when the required data format or behaviour is different.
- **Rejected:** Modifying an existing shared function simply to support a new page.
- **Why:** Existing pages depended on the original behaviour of shared functions. Keeping that behaviour reduced the risk of breaking working features while allowing new requirements such as server-side filtering and pagination to be implemented separately.

### Later reversed:

Initially, the Manager Items implementation changed `get_items()` so that it returned the new filtered/paginated data structure. This caused the existing Manager Stock Movements page to fail because it expected `get_items()` to return a list of items.

After identifying the dependency, the change was reversed. The original `get_items()` behaviour was restored and a separate `get_manager_items()` function was introduced for the Manager Items page.

This changed the approach from modifying the shared function to keeping the existing function stable and isolating the new functionality.

## Decision 6

- **Chose:** Use Supabase/PostgreSQL directly through the Supabase Python client instead of introducing a separate custom backend API.
- **Rejected:** Building a separate REST API layer between the Streamlit application and the database.
- **Why:** The project requirements could be implemented with the existing Streamlit and Supabase setup. Adding another backend layer would increase the amount of code and maintenance without providing enough benefit for the scope of this project.