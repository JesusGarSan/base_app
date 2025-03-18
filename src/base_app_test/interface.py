import streamlit as st

@st.cache_data
def header(elements:list):
    # Assertions and checks
    attributes = ["page_name", "filepath", "icon"]
    for element in elements:
        assert type(element) == dict, "elements list must contain dictionaries"
        for attribute in attributes:
            assert attribute in element, f"Header element dictonary must contain {attribute} as attribute"
    

    n_elements = len(elements)
    col = st.columns(n_elements)

    for i in range(n_elements):
        with col[i]:
            page_name = elements[i]["page_name"]
            filepath  = elements[i]["filepath"]
            icon      = elements[i]["icon"]
            st.page_link(filepath, label=page_name, icon=icon)

    return
