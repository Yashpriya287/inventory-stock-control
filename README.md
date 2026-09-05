# BUSY - Inventory Management System

A role-based inventory management system built using **Streamlit, Python, Supabase, and PostgreSQL** for managing items, categories, warehouse locations, users, stock movements, inventory history, and reporting.

The system is designed for a distributor operating across multiple warehouse locations, with separate workflows and permissions for managers and warehouse staff.

---

## Features

### Authentication & Roles

The application supports two user roles:

- **Manager**
  - Full access to inventory management.
  - Manage items and categories.
  - Manage warehouse locations.
  - Manage users and staff assignments.
  - Perform all stock movement types.
  - Import and export inventory data.
  - View dashboards, stock information, low-stock alerts, and item history.

- **Warehouse Staff**
  - Access only assigned warehouse locations.
  - Perform permitted stock receipts, issues, and transfers.
  - View inventory and stock information.
  - View low-stock alerts and item history.
  - Cannot create items or locations.
  - Cannot perform stock adjustments.

---

## Inventory Management

Managers can:

- Create inventory items.
- Edit item information.
- Set reorder levels.
- Assign categories.
- Archive and restore items.
- Search and filter inventory.
- Sort inventory information.
- View available stock across locations.

Each item contains information such as:

- SKU
- Name
- Description
- Unit of Measure
- Reorder Level
- Category
- Archive Status

---

## Category & Location Management

### Categories

Managers can create and manage inventory categories.

### Locations

Managers can create and manage warehouse locations.

Warehouse staff can be assigned to multiple locations through the user-location assignment system.

Staff members are restricted to the locations assigned to them.

---

## Stock Management

The system supports four types of stock movements:

- **Receipt**
- **Issue**
- **Transfer**
- **Adjustment**

### Receipts

Increase stock at a selected location.

### Issues

Remove stock from a location while preventing stock from becoming negative.

### Transfers

Move stock from one location to another.

### Adjustments

Increase or decrease stock with a required adjustment reason.

Stock is derived from the stock movement ledger rather than being manually maintained as a separate current-stock value.

---

## Inventory Protection

Important inventory rules are enforced at the database level.

The database prevents:

- Negative stock.
- Invalid stock movement combinations.
- Invalid adjustment data.
- Unauthorized staff movement locations.
- Modification or deletion of stock movements.
- Modification or deletion of item history.

This ensures that important inventory records remain reliable even if the application layer is bypassed.

---

## Item History

The system maintains an immutable history of item-related changes.

History can record:

- Item creation.
- Item updates.
- Changed fields.
- Previous values.
- New values.
- User who performed the change.
- Notes.
- Timestamp.

Historical records cannot be edited or deleted.

---

## Inventory Search

The Items page provides:

- Search by SKU or item name.
- Category filtering.
- Location filtering.
- Archived item filtering.
- Reorder-level filtering.
- Sorting by relevant inventory fields.
- Pagination.
- Total matching item count.

Inventory data can also show stock across all locations or for a specific location.

---

## Dashboard

The dashboard provides an overview of inventory activity, including:

- Active item count.
- Items at or below reorder level.
- Stock movement activity.
- Distinct items moved during the week.
- Stock summaries by category and location.
- Receipt and issue trends over the previous eight weeks.

---

## Import & Export

The application supports CSV-based inventory operations.

### Item Import

Managers can import items using CSV files.

Invalid rows are reported individually while valid rows can still be imported.

### Receipt Import

Receipt data can be imported using CSV files containing item SKU, quantity, and location information.

### Stock Export

Current stock by location can be exported as a CSV file containing:

- SKU
- Item
- Location
- Quantity

---

## Low Stock Alerts

The application provides a Low Stock Alerts section and navigation indicator based on item stock and reorder levels.

The current implementation provides the main low-stock detection functionality.

The complete alert dismissal and reappearance lifecycle is a remaining enhancement.

---

## Technology Stack

### Frontend / Application

- Python
- Streamlit

### Backend / Database

- Supabase
- PostgreSQL

### Database Features

- PostgreSQL ENUM types
- Foreign keys
- Primary keys
- Unique constraints
- CHECK constraints
- Database views
- PostgreSQL functions
- Database triggers

---

## Project Structure

```text
busy-infotech/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── assets/
│   └── box_logo.png
│
├── database/
│   ├── schema.sql
│   ├── functions.sql
│   └── triggers.sql
│
├── docs/
│   ├── ai-prompts.md
│   ├── architecture.md
│   ├── decisions.md
│   ├── plan.md
│   └── schema.md
│
├── manager_services/
│   ├── category_service.py
│   ├── import_export_service.py
│   ├── item_history_service.py
│   ├── item_service.py
│   ├── location_service.py
│   ├── stock_movement_service.py
│   ├── stock_service.py
│   └── user_service.py
│
├── staff_services/
│   ├── staff_dashboard_service.py
│   ├── staff_import_export_service.py
│   ├── staff_item_history_service.py
│   ├── staff_item_service.py
│   ├── staff_low_stock_service.py
│   ├── staff_movement_services.py
│   └── staff_stock_overview_service.py
│
├── screens/
│   ├── auth/
│   ├── manager_pages/
│   ├── staff_pages/
│   ├── manager.py
│   └── staff.py
│
└── utils/
    ├── auth.py
    ├── database.py
    ├── footer.py
    ├── header.py
    ├── layout.py
    ├── sidebar_layout.py
    └── time_utils.py