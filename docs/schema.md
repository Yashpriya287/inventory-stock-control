# Schema

## 1. Table by table: what columns and types does each one have?

The application uses PostgreSQL through Supabase. The database contains the following main tables, types, and view.

### `users`

Stores application users and their roles.

| Column | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `email` | VARCHAR(255) | Unique user email |
| `password_hash` | TEXT | Stored password hash |
| `full_name` | VARCHAR(255) | User's full name |
| `role` | `user_role` | Manager or staff |
| `is_active` | BOOLEAN | Whether the account is active |
| `created_at` | TIMESTAMPTZ | Account creation time |

The `user_role` enum contains:

- `manager`
- `staff`

---

### `categories`

Stores inventory categories.

| Column | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `name` | VARCHAR(100) | Unique category name |
| `description` | TEXT | Optional description |
| `is_active` | BOOLEAN | Whether the category is active |
| `created_at` | TIMESTAMPTZ | Creation time |

---

### `locations`

Stores warehouse or distribution locations.

| Column | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `name` | VARCHAR(150) | Unique location name |
| `description` | TEXT | Optional description |
| `is_active` | BOOLEAN | Whether the location is active |
| `created_at` | TIMESTAMPTZ | Creation time |

---

### `user_locations`

This is the junction table connecting users and locations.

| Column | Type | Description |
|---|---|---|
| `user_id` | UUID | Foreign key to `users.id` |
| `location_id` | UUID | Foreign key to `locations.id` |

The combination of `user_id` and `location_id` is the primary key.

---

### `items`

Stores the inventory item master data.

| Column | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `sku` | VARCHAR(100) | Unique stock keeping unit |
| `name` | VARCHAR(255) | Item name |
| `description` | TEXT | Optional description |
| `unit_of_measure` | VARCHAR(50) | Unit used for inventory |
| `reorder_level` | NUMERIC(12,2) | Reorder threshold |
| `category_id` | UUID | Foreign key to `categories.id` |
| `is_archived` | BOOLEAN | Whether the item is archived |
| `created_at` | TIMESTAMPTZ | Creation time |
| `updated_at` | TIMESTAMPTZ | Last update time |

The database enforces that `reorder_level` cannot be negative.

---

### `stock_movements`

Stores all inventory movements.

| Column | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `item_id` | UUID | Foreign key to `items.id` |
| `movement_type` | `movement_type` | Receipt, issue, transfer, or adjustment |
| `quantity` | NUMERIC(12,2) | Movement quantity |
| `location_id` | UUID | Location for receipt, issue, or adjustment |
| `source_location_id` | UUID | Source location for transfers |
| `destination_location_id` | UUID | Destination location for transfers |
| `adjustment_reason` | TEXT | Required for adjustments |
| `adjustment_direction` | `adjustment_direction` | Increase or decrease for adjustments |
| `recorded_by` | UUID | Foreign key to `users.id` |
| `created_at` | TIMESTAMPTZ | Movement creation time |

The `movement_type` enum contains:

- `receipt`
- `issue`
- `transfer`
- `adjustment`

The `adjustment_direction` enum contains:

- `increase`
- `decrease`

Database CHECK constraints ensure that:

- Quantity is greater than zero.
- Receipts, issues, and adjustments use `location_id`.
- Transfers use `source_location_id` and `destination_location_id`.
- A transfer cannot have the same source and destination.
- Adjustments require both a reason and direction.
- Non-adjustment movements cannot contain adjustment information.

---

### `item_history`

Stores the history of changes and events related to items.

| Column | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `item_id` | UUID | Foreign key to `items.id` |
| `event_type` | VARCHAR(50) | Type of history event |
| `field_name` | VARCHAR(100) | Field affected by a change |
| `old_value` | JSONB | Previous value |
| `new_value` | JSONB | New value |
| `note` | TEXT | Optional note |
| `performed_by` | UUID | Foreign key to `users.id` |
| `created_at` | TIMESTAMPTZ | Time of the event |

The use of JSONB for `old_value` and `new_value` allows different types of item field values to be stored in a consistent history structure.

---

### `low_stock_alerts`

Stores low-stock alert state for an item at a location.

| Column | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `item_id` | UUID | Foreign key to `items.id` |
| `location_id` | UUID | Foreign key to `locations.id` |
| `is_dismissed` | BOOLEAN | Whether the alert has been dismissed |
| `dismissed_by` | UUID | User who dismissed the alert |
| `dismissed_at` | TIMESTAMPTZ | Time the alert was dismissed |
| `created_at` | TIMESTAMPTZ | Alert creation time |
| `updated_at` | TIMESTAMPTZ | Last update time |

There is a UNIQUE constraint on `(item_id, location_id)` so that an item has at most one alert record for a particular location.

---

### `current_stock_by_location`

`current_stock_by_location` is a database view rather than a physical table.

It calculates current stock from the `stock_movements` ledger.

The main columns exposed by the view are:

| Column | Type | Description |
|---|---|---|
| `item_id` | UUID | Inventory item |
| `location_id` | UUID | Location |
| `quantity_on_hand` | NUMERIC | Calculated stock |

Receipts and increases add stock, issues and decreases remove stock, and transfers remove stock from the source location and add it to the destination location.

---

## 2. Which relationships are one-to-many, and which are many-to-many?

### One-to-many relationships

The following relationships are one-to-many:

- One category can contain many items.
- One item can have many stock movements.
- One item can have many item history records.
- One user can record many stock movements.
- One user can create many item history records.
- One location can be referenced by many stock movements.
- One item can have multiple low-stock alert records across different locations.
- One location can have low-stock alerts for many items.

### Many-to-many relationship

Users and locations have a many-to-many relationship.

A staff member can be assigned to multiple locations, and a location can have multiple staff members.

This is implemented through the `user_locations` junction table.

---

## 3. Which constraints are enforced by the database, and which by application code — and why did you draw the line there?

### Database-enforced constraints

The database enforces structural and important inventory-integrity rules.

These include:

- Primary keys.
- Foreign keys.
- Unique email addresses.
- Unique category names.
- Unique location names.
- Unique item SKUs.
- Unique `(user_id, location_id)` assignments.
- Unique `(item_id, location_id)` low-stock alerts.
- Non-negative reorder levels.
- Positive stock movement quantities.
- Valid movement/location combinations.
- Valid adjustment information.
- Valid enum values.

Database triggers also enforce important business rules.

The `validate_user_location_access()` trigger function prevents staff from recording movements at locations they are not assigned to. Managers are allowed to access all locations.

The `prevent_negative_stock()` trigger prevents issues, decrease adjustments, and transfers from reducing stock below zero.

The `prevent_stock_movement_changes()` trigger prevents UPDATE and DELETE operations on stock movements.

The `prevent_item_history_changes()` trigger prevents UPDATE and DELETE operations on item history.

The `set_updated_at()` trigger automatically updates the `updated_at` field for items and low-stock alerts.

### Application-enforced rules

The Python application handles rules related to user workflows and interface behaviour, including:

- Which pages are available to managers and staff.
- Which movement options are shown to each role.
- Staff-specific navigation.
- CSV validation and row-level import errors.
- Search, filtering, sorting, and pagination.
- Dashboard calculations and presentation.
- User-facing validation and error messages.

The line was drawn so that critical data-integrity rules are protected by the database itself, while presentation and workflow decisions remain in the application layer.

This prevents important inventory rules from being bypassed simply by calling the database directly.

---

## 4. What did you deliberately denormalise?

The core transactional data was intentionally kept normalized.

The application does not store a manually maintained `current_stock` column on the `items` table. Instead, current stock is calculated from the immutable stock movement ledger through the `current_stock_by_location` view.

The `item_history.old_value` and `item_history.new_value` fields use JSONB. This is a deliberate flexible structure because different item fields can have different value types while still being represented within the same history format.

The `current_stock_by_location` view can also be considered a derived representation rather than duplicated source data. It exists to make inventory calculations easier to query without maintaining a second authoritative stock value.

---

## 5. What would break first if this had 100x the data?

The first areas likely to become bottlenecks would be database queries that process large numbers of stock movements and history records.

### Stock calculations

The `current_stock_by_location` view calculates stock by processing the movement ledger. With a much larger number of movements, this aggregation could become expensive.

Indexes and query optimization would become increasingly important.

### Dashboard

Dashboard statistics and eight-week movement charts could become slower if large amounts of historical movement data have to be scanned for every page load.

Pre-aggregated reporting data or materialized views could eventually be considered.

### Item history

Items with very large histories would require efficient pagination and targeted queries rather than loading all history records at once.

### Search and inventory listing

Search and filtering across a much larger item table would depend heavily on appropriate indexes for fields such as SKU, name, category, and foreign keys.

### CSV import/export

Very large CSV files would require more efficient batch processing and possibly background jobs instead of processing the entire file during a single Streamlit request.

The current schema is appropriate for the scale and requirements of this project. At 100x the data volume, database indexing, query optimization, aggregation strategies, and possibly background processing would become the main areas requiring redesign.
