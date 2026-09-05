# BUSY Inventory Management System — Submission

## Project Links

- **GitHub Repository:** https://github.com/Yashpriya287/inventory-stock-control
- **Live Demo:** https://busy-inventory-management.streamlit.app/

---

## Demo Credentials

### Manager

- **Email:** yashpriyadwivedi@gmail.com
- **Password:** 1234

### Staff

- **Email:** 230107057@hbtu.ac.in
- **Password:** 12345

> These credentials are provided only for evaluation of the deployed application.

---

## Tech Stack

- **Frontend / UI:** Streamlit
- **Backend:** Python
- **Database:** PostgreSQL via Supabase
- **Authentication:** Custom role-based authentication
- **Database Logic:** PostgreSQL functions, triggers and views
- **Data Import/Export:** CSV
- **Deployment:** Streamlit Community Cloud
- **Version Control:** Git / GitHub

---

## Self-Assessment Against the 10 Project Goals

| Goal | Status | Assessment |
|---|---|---|
| 1. Accounts & Roles | ✅ Complete | Implemented manager and staff authentication with role-based access control. |
| 2. Item Management | ✅ Complete | Implemented item creation, editing, archiving, categories, SKU, unit of measure, and reorder levels. |
| 3. Stock Movements | ✅ Complete | Implemented receipts, issues, transfers, and adjustments with validation. |
| 4. Append-Only Stock Ledger | ✅ Complete | Stock movements are treated as an append-only ledger, with database-level protection against updates/deletions and negative stock. |
| 5. Location Assignment | ✅ Complete | Staff can be assigned to locations and access is validated for location-based stock operations. |
| 6. Search, Filter & Pagination | ✅ Complete | Implemented item search/filtering and pagination for inventory-related views. |
| 7. Import / Export | ✅ Complete | Implemented CSV import for items and receipts, validation/error reporting, and current-stock CSV export. |
| 8. Dashboard | ✅ Implemented | Implemented inventory dashboard functionality with stock-related summaries and operational information. |
| 9. Immutable Item History | ✅ Complete | Implemented item history tracking with database-level protection against modification or deletion of history records. |
| 10. Low-Stock Alerts | ⚠️ Partially Complete | Implemented low-stock identification, alert visibility, and reorder-level comparison. The complete dismissal and reappearance lifecycle and consistent cross-location aggregation can be improved further. |

---

## Time Spent

Approximately **14 hours** were spent on the project, including database design, backend/service implementation, UI development, integration, debugging, testing, documentation, and deployment.

## Closing Questions

### What was the most challenging part of the project?

The most challenging part was maintaining consistency between the stock movement ledger, current stock calculations, role-based access, and different manager/staff workflows.

A key challenge was also making changes to shared service functions without breaking existing screens that depended on them. This required careful debugging and reinforced the importance of keeping responsibilities separated between the UI, service layer, and database.

### If you had more time, what would you improve?

With more time, I would complete and refine the low-stock alert workflow, particularly the dismissal and reappearance lifecycle and consistent stock aggregation across locations.

I would also add more automated tests and spend additional time on edge-case testing for imports, transfers, permissions, and other inventory operations, along with further UI/UX improvements.