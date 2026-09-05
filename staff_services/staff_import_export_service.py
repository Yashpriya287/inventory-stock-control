import io
import csv

from utils.database import supabase
from staff_services.staff_movement_services import get_staff_locations


# ==========================================================
# IMPORT RECEIPTS
# ==========================================================

def import_staff_receipts_csv(file, user_id):

    content = file.getvalue().decode("utf-8-sig")

    reader = csv.DictReader(
        io.StringIO(content)
    )

    required_columns = {
        "SKU",
        "Quantity",
        "Location"
    }

    if not reader.fieldnames:
        raise ValueError(
            "CSV file is empty or has no header."
        )

    missing_columns = (
        required_columns
        - set(reader.fieldnames)
    )

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    # ------------------------------------------------------
    # STAFF ASSIGNED LOCATIONS
    # ------------------------------------------------------

    assigned_locations = get_staff_locations(user_id)

    location_map = {
        location["name"].strip().lower(): location["id"]
        for location in assigned_locations
    }

    if not location_map:
        raise ValueError(
            "You are not assigned to any location."
        )

    # ------------------------------------------------------
    # ACTIVE ITEMS
    # ------------------------------------------------------

    items_response = (
        supabase
        .table("items")
        .select("id, sku, is_archived")
        .eq("is_archived", False)
        .execute()
    )

    item_map = {
        item["sku"].strip().lower(): item["id"]
        for item in items_response.data
    }

    imported = []
    errors = []

    # ------------------------------------------------------
    # PROCESS EACH ROW
    # ------------------------------------------------------

    for row_number, row in enumerate(
        reader,
        start=2
    ):

        try:

            sku = (
                row.get("SKU") or ""
            ).strip()

            quantity_text = (
                row.get("Quantity") or ""
            ).strip()

            location_name = (
                row.get("Location") or ""
            ).strip()

            # ------------------------------
            # REQUIRED VALUES
            # ------------------------------

            if not sku:
                raise ValueError(
                    "SKU is required."
                )

            if not quantity_text:
                raise ValueError(
                    "Quantity is required."
                )

            if not location_name:
                raise ValueError(
                    "Location is required."
                )

            # ------------------------------
            # CHECK ITEM
            # ------------------------------

            item_id = item_map.get(
                sku.lower()
            )

            if not item_id:
                raise ValueError(
                    f"Active item with SKU '{sku}' "
                    "was not found."
                )

            # ------------------------------
            # CHECK QUANTITY
            # ------------------------------

            try:
                quantity = float(
                    quantity_text
                )
            except ValueError:
                raise ValueError(
                    "Quantity must be a number."
                )

            if quantity <= 0:
                raise ValueError(
                    "Quantity must be greater than zero."
                )

            # ------------------------------
            # CHECK LOCATION
            # ------------------------------

            location_id = location_map.get(
                location_name.lower()
            )

            if not location_id:
                raise ValueError(
                    f"You are not assigned to location "
                    f"'{location_name}'."
                )

            # ------------------------------
            # INSERT RECEIPT
            # ------------------------------

            data = {
                "item_id": item_id,
                "movement_type": "receipt",
                "quantity": quantity,
                "location_id": location_id,
                "recorded_by": user_id
            }

            response = (
                supabase
                .table("stock_movements")
                .insert(data)
                .execute()
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
# EXPORT CURRENT STOCK
# ==========================================================

def export_staff_current_stock(user_id):

    # ------------------------------------------------------
    # GET STAFF LOCATIONS
    # ------------------------------------------------------

    assigned_locations = get_staff_locations(
        user_id
    )

    location_ids = [
        location["id"]
        for location in assigned_locations
    ]

    if not location_ids:
        return (
            "SKU,Item,Location,Quantity\n"
        )

    location_map = {
        location["id"]: location["name"]
        for location in assigned_locations
    }

    # ------------------------------------------------------
    # GET CURRENT STOCK
    # ------------------------------------------------------

    stock_response = (
        supabase
        .table("current_stock_by_location")
        .select(
            "item_id, location_id, quantity_on_hand"
        )
        .in_(
            "location_id",
            location_ids
        )
        .execute()
    )

    # ------------------------------------------------------
    # GET ITEMS
    # ------------------------------------------------------

    item_ids = list({
        row["item_id"]
        for row in stock_response.data
    })

    item_map = {}

    if item_ids:

        items_response = (
            supabase
            .table("items")
            .select("id, sku, name")
            .in_("id", item_ids)
            .execute()
        )

        item_map = {
            item["id"]: item
            for item in items_response.data
        }

    # ------------------------------------------------------
    # CREATE CSV
    # ------------------------------------------------------

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "SKU",
        "Item",
        "Location",
        "Quantity"
    ])

    for stock in stock_response.data:

        item = item_map.get(
            stock["item_id"]
        )

        location_name = location_map.get(
            stock["location_id"]
        )

        if not item or not location_name:
            continue

        writer.writerow([
            item["sku"],
            item["name"],
            location_name,
            float(
                stock["quantity_on_hand"] or 0
            )
        ])

    return output.getvalue()