import streamlit as st

from utils.layout import style_base_layout
from manager_services.location_service import create_location, get_locations,update_location,update_location_status


def locations_page():
    style_base_layout()

    # SESSION STATE 
    if "show_add_location_form" not in st.session_state:
        st.session_state.show_add_location_form = False

    if "editing_location_id" not in st.session_state:
        st.session_state.editing_location_id = None    


    # ---------- HEADER ----------

    title_col, button_col = st.columns([4, 1])

    with title_col:
        st.title("Locations")
        st.caption("Manage your inventory storage locations.")

    with button_col:
        st.write("")
        st.write("")

        if st.button( "＋ Add Location",use_container_width=True,key="add_location" ):
            st.session_state.show_add_location_form = True

    st.write("")


    # ADD LOCATION FORM 
    if st.session_state.show_add_location_form:

        st.subheader("Add New Location")

        name_col, gap, description_col = st.columns([1, 0.08, 2])

        with name_col:
            location_name = st.text_input("Location Name",placeholder="e.g. Main Warehouse")

        with description_col:
            description = st.text_input("Description",placeholder="Enter location description (optional)")

        st.write("")

        cancel_col, save_col, empty_col = st.columns([1, 1, 3])

        with cancel_col:
            if st.button( "Cancel", use_container_width=True, key="cancel_location" ):
                st.session_state.show_add_location_form = False
                st.rerun()

        with save_col:
            if st.button( "Save Location", use_container_width=True,type="primary", key="save_location" ):

                if not location_name.strip():
                    st.error("Please enter a location name.")

                else:
                    try:
                        create_location(
                            name=location_name.strip(),
                            description=description.strip() )

                        st.session_state.show_add_location_form = False
                        st.success("Location added successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Error adding location: {e}")

        st.divider()


    # ---------- SEARCH ----------

    search_col, empty_col = st.columns([2, 2])

    with search_col:
        search = st.text_input( "Search Locations", placeholder="🔍 Search locations", label_visibility="collapsed", key="search_locations" )


   

    locations = get_locations()

    if search:

        search = search.lower()

        locations = [
            location for location in locations
            if search in location["name"].lower()
            or (
                location["description"]
                and search in location["description"].lower()
            )
        ]
    st.write("")
    st.subheader("Locations")

    headers = st.columns([2, 3, 1.2, 0.7])

    for col, text in zip(
        headers,
        [
            "LOCATION",
            "DESCRIPTION",
            "STATUS",
            "ACTIONS"
        ]
    ):
        col.markdown(f"**{text}**")

    st.divider()


    # ---------- TABLE ROWS ----------

    if not locations:
        st.info("No locations found.")

    for location in locations:

        cols = st.columns([2, 3, 1.2, 0.7])

        cols[0].write(location["name"])

        cols[1].write( location["description"] if location["description"] else "—")

        if location["is_active"]:
            cols[2].success("Active")
        else:
            cols[2].warning("Inactive")

        with cols[3]:

            with st.popover( "•••", use_container_width=False):
                if st.button( "✏️ Edit", key=f"edit_location_{location['id']}" ):
                    st.session_state.editing_location_id = location["id"]
                    st.rerun()

                if location["is_active"]:
                    if st.button( "Deactivate",key=f"deactivate_location_{location['id']}" ):
                        try:
                            update_location_status( location["id"], False)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error updating location: {e}")

                else:
                    if st.button( "Activate",key=f"activate_location_{location['id']}" ):
                        try:
                            update_location_status(location["id"],  True )
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error updating location: {e}")
    # ---------- EDIT LOCATION ----------

    if st.session_state.editing_location_id:

        selected_location = next(
            (
                location for location in locations
                if location["id"] == st.session_state.editing_location_id
            ),
            None
        )

        if selected_location:

            st.subheader("Edit Location")

            st.info(
                f"Editing: {selected_location['name']}"
            )

            location_name = st.text_input(
                "Location Name",
                value=selected_location["name"],
                key=f"edit_name_{selected_location['id']}"
            )

            description = st.text_input(
                "Description",
                value=selected_location["description"] or "",
                key=f"edit_description_{selected_location['id']}"
            )

            cancel_col, save_col, _ = st.columns([1, 1, 3])

            with cancel_col:
                if st.button(
                    "Cancel Edit",
                    key="cancel_edit_location"
                ):
                    st.session_state.editing_location_id = None
                    st.rerun()

            with save_col:
                if st.button(
                    "Save Changes",
                    type="primary",
                    key="save_edit_location"
                ):

                    if not location_name.strip():
                        st.error("Please enter a location name.")

                    else:
                        try:
                            update_location(
                                location_id=selected_location["id"],
                                name=location_name.strip(),
                                description=description.strip()
                            )

                            st.session_state.editing_location_id = None
                            st.success("Location updated successfully!")
                            st.rerun()

                        except Exception as e:
                            st.error(f"Error updating location: {e}")                            

        st.divider()