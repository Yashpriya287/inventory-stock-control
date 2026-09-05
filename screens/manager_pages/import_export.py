import streamlit as st

from manager_services.import_export_service import (
    import_items_csv,
    import_receipts_csv,
    export_current_stock
)


def import_export_page():

    st.title("Import / Export")
    st.caption(
        "Import inventory data and export stock information."
    )

    st.divider()

    # ==================================================
    # IMPORT
    # ==================================================

    st.subheader("📥 Import")

    item_col, empty, receipt_col = st.columns(
        [1, 0.12, 1]
    )

    # --------------------------------------------------
    # IMPORT ITEMS
    # --------------------------------------------------

    with item_col:

        st.markdown("### Import Items")

        item_file = st.file_uploader(
            "Upload Items CSV",
            type=["csv"],
            key="items_csv"
        )

        if item_file:

            if st.button(
                "Import Items",
                key="import_items_button",
                type="primary",
                use_container_width=True
            ):

                try:

                    imported, errors = import_items_csv(
                        item_file
                    )

                    if imported:
                        st.success(
                            f"{len(imported)} item(s) "
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
                        f"Error importing items: {e}"
                    )

    # --------------------------------------------------
    # IMPORT RECEIPTS
    # --------------------------------------------------

    with receipt_col:

        st.markdown("### Import Receipts")

        receipt_file = st.file_uploader(
            "Upload Receipts CSV",
            type=["csv"],
            key="receipts_csv"
        )

        if receipt_file:

            if st.button(
                "Import Receipts",
                key="import_receipts_button",
                type="primary",
                use_container_width=True
            ):

                current_user = st.session_state.get(
                    "user"
                )

                if not current_user:

                    st.error(
                        "You must be logged in as a manager."
                    )

                else:

                    try:

                        imported, errors = (
                            import_receipts_csv(
                                receipt_file,
                                current_user["id"]
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

    # ==================================================
    # EXPORT
    # ==================================================

    st.divider()

    st.subheader("📤 Export")

    st.markdown(
        "### Current Stock by Location"
    )

    download_col, _ = st.columns(
        [1.5, 3]
    )

    with download_col:

        try:

            csv_data = export_current_stock()

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