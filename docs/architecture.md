# Architecture

## 1. What are the moving pieces, and how do they talk to each other?

The Inventory Management System follows a layered architecture using Streamlit for the application interface and Supabase/PostgreSQL for data storage.

The main components are:

- **Streamlit Application** – Provides the user interface and handles user interaction.
- **Authentication** – Handles login and determines whether the user is a manager or warehouse staff.
- **Manager Pages** – Provide manager functionality such as item management, categories, locations, users, dashboard, stock overview, stock movements, item history, and import/export.
- **Staff Pages** – Provide warehouse staff functionality such as dashboard, items, stock overview, stock movements, low-stock alerts, and item history.
- **Service Layer** – Contains the application logic and database operations. Manager and staff functionality is separated into their respective service modules.
- **Supabase Client** – Acts as the connection between the Python application and the backend database.
- **PostgreSQL Database** – Stores users, items, categories, locations, user-location assignments, stock movements, and item history. Database views/functions are also used where required for inventory calculations.

The general communication flow is:

Streamlit UI → Page → Service Layer → Supabase Client → PostgreSQL

The response then travels back through the service layer to the page, where the result is displayed in the Streamlit interface.

---

## 2. Where does each piece run?

The Streamlit application, pages, authentication logic, and service layer all run in the Python application environment.

The application is organized into separate modules:

- `screens/manager_pages/` contains manager-facing pages.
- `screens/staff_pages/` contains warehouse staff pages.
- `manager_services/` contains manager-related database and business logic.
- `staff_services/` contains staff-related database and business logic.
- `utils/` contains shared functionality such as database access, layout, sidebar handling, and time formatting.

Supabase runs separately as the backend service. PostgreSQL is hosted by Supabase and stores the application's persistent data.

---

## 3. What is the request path for one representative user action, end to end?

A representative action is a manager creating a new inventory item.

1. The manager logs into the Streamlit application.
2. The manager opens the **Items** page.
3. The manager enters the item's SKU, name, description, unit of measure, reorder level, and category.
4. The page collects the entered values and sends them to the `create_item()` function in the item service.
5. The service layer prepares the item data and uses the Supabase client to insert it into the `items` table.
6. PostgreSQL stores the new item and applies the database rules and constraints.
7. Supabase returns the result to the Python application.
8. The Streamlit page reruns and displays the newly created item.

The same basic pattern is used for other operations such as stock movements, category management, location management, and item history.

For staff operations, an additional permission check is performed so that staff can only perform the operations allowed for their role and assigned locations.

---

## 4. What did you decide not to build, and why?

A separate custom REST API backend was not built because Streamlit and the Supabase client were sufficient for the requirements of this project. Adding another backend layer would have increased development and maintenance complexity without providing a significant benefit for the current application.

Microservices were also not used because this is a single inventory management application. A modular layered structure was sufficient to keep the code organized.

The project also does not include advanced features such as external ERP integrations, complex enterprise permission management, or real-time multi-user collaboration. These were outside the core requirements and would require additional infrastructure and development time.

The focus was kept on implementing the required inventory, stock movement, role-based access, location assignment, reporting, import/export, and history functionality.