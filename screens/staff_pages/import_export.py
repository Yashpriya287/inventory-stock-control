import streamlit as st

from utils.layout import style_base_layout

from staff_services.staff_import_export_service import (
    import_staff_receipts_csv,
    export_staff_current_stock
)


def staff_import_export_page():

    style_base_layout()

    # ------------------------------------------------------
    # CURRENT USER
    # ------------------------------------------------------

    current_user = st.session_state.get(
        "current_user"
    )

    if not current_user:
        st.warning(
            "Please log in first."
        )
        return

    user_id = current_user["id"]

    # ------------------------------------------------------
    # HEADER
    # ------------------------------------------------------

    st.title("Import / Export")

    st.caption(
        "Import stock receipts and export current stock information."
    )

    st.divider()

    # ======================================================
    # IMPORT / EXPORT
    # ======================================================

    import_col, export_col = st.columns([1, 1], gap="large")


    # ======================================================
    # IMPORT RECEIPTS
    # ======================================================

    with import_col:

        st.subheader("📥 Import Receipt")


        st.caption(
            "Upload a CSV containing stock receipts."
        )

        receipt_file = st.file_uploader(
            "Upload Receipts CSV",
            type=["csv"],
            key="staff_receipts_csv"
        )

        if receipt_file:

            if st.button(
                "Import Receipts",
                key="staff_import_receipts_button",
                type="primary",
                use_container_width=True
            ):

                try:

                    imported, errors = (
                        import_staff_receipts_csv(
                            receipt_file,
                            user_id
                        )
                    )

                    if imported:
                        st.success(
                            f"{len(imported)} receipt(s) "
                            "imported successfully."
                        )

                    if errors:

                        st.error(
                            f"{len(errors)} row(s) "
                            "could not be imported."
                        )

                        for error in errors:
                            st.write(
                                f"❌ Row {error['row']}: "
                                f"{error['error']}"
                            )

                    if not imported and not errors:
                        st.info(
                            "No rows were found in the CSV."
                        )

                except Exception as e:

                    st.error(
                        f"Error importing receipts: {e}"
                    )


    # ======================================================
    # EXPORT CURRENT STOCK
    # ======================================================

    with export_col:

        st.subheader("📤 Export")

        st.markdown(
            "### Current Stock by Location"
        )

        st.caption(
            "Export current on-hand stock for your assigned locations."
        )

        try:

            csv_data = export_staff_current_stock(
                user_id
            )

            st.download_button(
                "Download Stock CSV",
                data=csv_data,
                file_name="current_stock_by_location.csv",
                mime="text/csv",
                use_container_width=True
            )

        except Exception as e:

            st.error(
                f"Error generating stock export: {e}"
            )