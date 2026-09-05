# Plan

## 1. How did you break the work into sessions?

The work was divided into feature-based development sessions rather than trying to build the complete application at once.

The main sessions were:

1. **Project setup and database** – Set up the Streamlit project structure, database connection, and core database tables.
2. **Authentication and roles** – Implemented manager and warehouse staff access and role-based navigation.
3. **Items and categories** – Built item creation, editing, archiving, restoring, and category management.
4. **Locations and staff assignments** – Added locations and restricted staff access according to assigned locations.
5. **Stock movements** – Implemented receipts, issues, transfers, and adjustments with the required validations.
6. **Inventory views** – Added stock overview, item search, filtering, sorting, and pagination.
7. **Dashboard and low-stock features** – Built inventory statistics, charts, and low-stock functionality.
8. **Import/export and history** – Added CSV import/export and immutable item history.
9. **Testing and debugging** – Tested the completed features and fixed issues without unnecessarily changing already-working parts of the application.

Each session focused on getting one part working before moving to the next.

---

## 2. What order did you build in, and why that order?

The project was built from the foundation upward.

First, the database structure and application setup were established because all other features depend on them. Authentication and roles were implemented next so that later pages could use the correct permissions.

Item, category, and location management were then built before stock movements because movements require existing items and locations.

After that, stock movements were implemented because they form the basis for calculating current inventory. Once the core inventory operations were working, search, filtering, pagination, dashboard information, import/export, and item history were added.

The final stage focused mainly on testing, debugging, and making sure new changes did not break existing functionality.

This order reduced dependencies between unfinished features and made it easier to test each major part as it was completed.

---

## 3. What did you estimate versus what it actually took?

The initial expectation was that the project could be completed feature by feature without major restructuring once the database and basic application structure were ready.

In practice, some features took longer than expected because implementation often revealed dependencies between existing parts of the application. Debugging and testing also required significant time.

For example, adding server-side filtering and pagination required additional care because existing pages were already using shared service functions. A change to `get_items()` initially caused the Manager Stock Movements page to stop working. The issue was identified and the original function behaviour was restored while a separate function was created for the new functionality.

Therefore, the actual development time was greater than the initial rough estimate, mainly because of integration, debugging, and testing rather than simply writing new features.

---

## 4. What did you cut when you ran short?

When time became limited, the priority was to keep the completed core functionality stable rather than continue adding features that could introduce new bugs.

The low-stock alert functionality was implemented to a substantial extent, but the complete dismissal and reappearance lifecycle was not finished.

Instead of making further structural changes close to completion, the focus was shifted to testing and stabilizing the features that were already working, including authentication, item management, stock movements, location restrictions, search and pagination, dashboard functionality, import/export, and immutable item history.

This allowed the project to retain a stable and demonstrable implementation while leaving the remaining low-stock alert enhancement for future work.