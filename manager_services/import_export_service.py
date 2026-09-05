import io
import csv

from utils.database import supabase


# ==========================================================
# ITEM IMPORT
# ==========================================================

def import_items_csv(file, performed_by):

    content = file.getvalue().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content))

    required_columns = {
        "SKU",
        "Name",
        "Description",
        "Unit of Measure",
        "Reorder Level",
        "Category"
    }

    if not reader.fieldnames:
        return [], ["CSV file is empty or has no headers."]

    missing_columns = required_columns - set(reader.fieldnames)

    if missing_columns:
        return [], [
            "Missing columns: "
            + ", ".join(sorted(missing_columns))
        ]

    # ------------------------------------------------------
    # Get categories
    # ------------------------------------------------------

    categories_response = (
        supabase
        .table("categories")
        .select("id, name")
        .eq("is_active", True)
        .execute()
    )

    category_map = {
        category["name"].strip().lower(): category["id"]
        for category in categories_response.data or []
    }

    # ------------------------------------------------------
    # Existing SKUs
    # ------------------------------------------------------

    existing_response = (
        supabase
        .table("items")
        .select("sku")
        .execute()
    )

    existing_skus = {
        row["sku"].strip().lower()
        for row in existing_response.data or []
    }

    imported = []
    errors = []

    for row_number, row in enumerate(reader, start=2):

        try:

            sku = (row.get("SKU") or "").strip()
            name = (row.get("Name") or "").strip()
            description = (
                row.get("Description") or ""
            ).strip()
            unit = (
                row.get("Unit of Measure") or ""
            ).strip()
            reorder_value = (
                row.get("Reorder Level") or ""
            ).strip()
            category_name = (
                row.get("Category") or ""
            ).strip()

            # --------------------------------------------------
            # Validation
            # --------------------------------------------------

            if not sku:
                raise ValueError("SKU is required.")

            if not name:
                raise ValueError("Name is required.")

            if not unit:
                raise ValueError(
                    "Unit of Measure is required."
                )

            if not reorder_value:
                raise ValueError(
                    "Reorder Level is required."
                )

            try:
                reorder_level = float(reorder_value)
            except ValueError:
                raise ValueError(
                    "Reorder Level must be numeric."
                )

            if reorder_level < 0:
                raise ValueError(
                    "Reorder Level cannot be negative."
                )

            category_id = category_map.get(
                category_name.lower()
            )

            if not category_id:
                raise ValueError(
                    f"Category '{category_name}' "
                    "does not exist or is inactive."
                )

            if sku.lower() in existing_skus:
                raise ValueError(
                    f"SKU '{sku}' already exists."
                )

            # --------------------------------------------------
            # Insert
            # --------------------------------------------------

            response = (
                supabase
                .table("items")
                .insert({
                    "sku": sku,
                    "name": name,
                    "description": description or None,
                    "unit_of_measure": unit,
                    "reorder_level": reorder_level,
                    "category_id": category_id
                })
                .execute()
            )

            if not response.data:
                raise ValueError(
                    "Item could not be inserted."
                )

            created_item = response.data[0]

            supabase.table("item_history").insert({
                "item_id": created_item["id"],
                "event_type": "created",
                "performed_by": performed_by
            }).execute()

            existing_skus.add(sku.lower())

            imported.append({
                "row": row_number,
                "sku": sku,
                "name": name
            })

        except Exception as e:

            errors.append({
                "row": row_number,
                "error": str(e)
            })

    return imported, errors


# ==========================================================
# RECEIPT IMPORT
# ==========================================================

def import_receipts_csv(file, user_id):

    content = file.getvalue().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content))

    required_columns = {
        "SKU",
        "Quantity",
        "Location"
    }

    if not reader.fieldnames:
        return [], ["CSV file is empty or has no headers."]

    missing_columns = required_columns - set(reader.fieldnames)

    if missing_columns:
        return [], [
            "Missing columns: "
            + ", ".join(sorted(missing_columns))
        ]

    # ------------------------------------------------------
    # Items
    # ------------------------------------------------------

    items_response = (
        supabase
        .table("items")
        .select("id, sku")
        .eq("is_archived", False)
        .execute()
    )

    item_map = {
        item["sku"].strip().lower(): item["id"]
        for item in items_response.data or []
    }

    # ------------------------------------------------------
    # Locations
    # ------------------------------------------------------

    locations_response = (
        supabase
        .table("locations")
        .select("id, name")
        .eq("is_active", True)
        .execute()
    )

    location_map = {
        location["name"].strip().lower(): location["id"]
        for location in locations_response.data or []
    }

    imported = []
    errors = []

    for row_number, row in enumerate(reader, start=2):

        try:

            sku = (row.get("SKU") or "").strip()
            quantity_value = (
                row.get("Quantity") or ""
            ).strip()
            location_name = (
                row.get("Location") or ""
            ).strip()

            if not sku:
                raise ValueError("SKU is required.")

            item_id = item_map.get(
                sku.lower()
            )

            if not item_id:
                raise ValueError(
                    f"SKU '{sku}' does not exist."
                )

            try:
                quantity = float(quantity_value)
            except ValueError:
                raise ValueError(
                    "Quantity must be numeric."
                )

            if quantity <= 0:
                raise ValueError(
                    "Quantity must be greater than 0."
                )

            location_id = location_map.get(
                location_name.lower()
            )

            if not location_id:
                raise ValueError(
                    f"Location '{location_name}' "
                    "does not exist or is inactive."
                )

            # --------------------------------------------------
            # Create receipt movement
            # --------------------------------------------------

            response = (
                supabase
                .table("stock_movements")
                .insert({
                    "item_id": item_id,
                    "movement_type": "receipt",
                    "quantity": quantity,
                    "location_id": location_id,
                    "recorded_by": user_id
                })
                .execute()
            )

            if not response.data:
                raise ValueError(
                    "Receipt could not be created."
                )

            imported.append({
                "row": row_number,
                "sku": sku,
                "quantity": quantity,
                "location": location_name
            })

        except Exception as e:

            errors.append({
                "row": row_number,
                "error": str(e)
            })

    return imported, errors


# ==========================================================
# STOCK EXPORT
# ==========================================================

def export_current_stock():

    stock_response = (
        supabase
        .table("current_stock_by_location")
        .select(
            "item_id, location_id, quantity_on_hand"
        )
        .execute()
    )

    if not stock_response.data:
        return ""

    item_ids = list({
        row["item_id"]
        for row in stock_response.data
    })

    location_ids = list({
        row["location_id"]
        for row in stock_response.data
    })

    # ------------------------------------------------------
    # Items
    # ------------------------------------------------------

    items_response = (
        supabase
        .table("items")
        .select("id, sku, name")
        .in_("id", item_ids)
        .execute()
    )

    item_map = {
        item["id"]: item
        for item in items_response.data or []
    }

    # ------------------------------------------------------
    # Locations
    # ------------------------------------------------------

    locations_response = (
        supabase
        .table("locations")
        .select("id, name")
        .in_("id", location_ids)
        .execute()
    )

    location_map = {
        location["id"]: location["name"]
        for location in locations_response.data or []
    }

    # ------------------------------------------------------
    # Build CSV
    # ------------------------------------------------------

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "SKU",
        "Item",
        "Location",
        "Quantity"
    ])

    for row in stock_response.data:

        item = item_map.get(row["item_id"])

        if not item:
            continue

        writer.writerow([
            item["sku"],
            item["name"],
            location_map.get(
                row["location_id"],
                "Unknown"
            ),
            float(
                row["quantity_on_hand"] or 0
            )
        ])

    return output.getvalue()