# Architecture

Answer each of these, in your own words, once the system has taken real shape.

- What are the moving pieces, and how do they talk to each other?
- Where does each piece run?
- What is the request path for one representative user action, end to end?
- What did you decide *not* to build, and why?


# Architecture

## 1. What are the moving pieces, and how do they talk to each other?

The Inventory Management System is built using a layered architecture.

The main moving pieces are:

- **Streamlit UI** – Handles the user interface, including login, dashboard, item management, and category management.
- **Application Pages** – Pages such as `items.py` and `category.py` contain the page-level logic and interact with the service layer.
- **Service Layer** – Files such as `item_service.py`, `category_service.py`, and `auth.py` handle communication between the application and the database.
- **Supabase** – Provides the backend database and stores application data.
- **PostgreSQL Database** – Stores users, categories, items, locations, stock movements, item history, and low-stock alerts.

The general flow is:

Streamlit UI → Page Logic → Service Layer → Supabase → PostgreSQL Database

Data returned from the database travels back through the same path and is displayed in the Streamlit interface.

## 2. Where does each piece run?

The Streamlit application runs in the Python application environment.

The frontend UI and page logic run together inside the Streamlit application. The service layer also runs as part of the same Python application and communicates with Supabase using the Supabase Python client.

The database runs separately on Supabase, where PostgreSQL stores and manages the application data.

## 3. What is the request path for one representative user action, end to end?

One representative user action is adding a new inventory item.

1. A manager opens the Items page.
2. The manager clicks the **Add Item** button.
3. The manager enters the SKU, item name, category, unit of measure, reorder level, and optional description.
4. The Items page retrieves available categories from the `categories` table.
5. When the manager clicks **Save Item**, the page sends the item data to the `create_item()` function in `item_service.py`.
6. The service layer uses the Supabase client to insert the item into the `items` table.
7. PostgreSQL validates the data using the database schema and constraints.
8. Supabase returns the result to the service layer.
9. The Streamlit application reruns and displays the newly added item in the Items table.

## 4. What did you decide *not* to build, and why?

The current project does not use a separate custom REST API backend because the application is built directly with Streamlit and Supabase. This reduced development complexity and allowed the project to focus on the required inventory management features.

The application also does not use microservices because the project is a single inventory management application and a layered structure is sufficient for the current scale.

Some advanced features, such as complex role-permission management, external integrations, and real-time collaboration, were not added because they were outside the core scope of the project.