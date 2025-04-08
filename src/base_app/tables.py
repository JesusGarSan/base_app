import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

def column_selector(data, default_columns:list = None, key="", text={"title": "Columns to show:", "placeholder":"Choose an option"}):
    columns = data.columns.to_list()
    if default_columns is None:
        default_columns = columns
    selected_columns = st.multiselect(text['title'], columns, default_columns, key="column_selector_"+key, placeholder=text['placeholder'])

    return selected_columns

def show_table(data, columns=None, use_container_width=True, **kwargs):
    if columns is None: columns = data.columns.to_list()
    if columns:
        st.dataframe(data[columns], use_container_width = use_container_width, **kwargs)
    else:
        st.write("No se ha seleccionado ninguna columna.")
    return

def show_stats(data, columns=None, use_container_width=True):
    if columns is None: columns = data.columns.to_list()
    with st.expander('Stats'):
        st.dataframe(data[columns].describe(), use_container_width=use_container_width)
    return

def sort_dataframe(df: pd.DataFrame, columns:list = None,
                   text={"title": "Columns to sort by",
                         "direction": "Sort direction:"},
                   sorting_directions=["Ascending", "Descending"],
                   max_selections=5, key="") -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers sort by multiple columns
    and direction.

    Args:
        df (pd.DataFrame): Original dataframe
        text (dict, optional): Dictionary of text elements for the UI.
            Defaults to {"title": "Sort dataframe by", "columns": "Columns to sort by", "direction": "Sort direction for"}.
        ascending_options (list, optional): List of strings for ascending/descending options.
            Defaults to ["Ascending", "Descending"].

    Returns:
        pd.DataFrame: Sorted dataframe
    """
    df = df.copy()
    if columns is None: columns = df.columns
    sort_columns = st.multiselect(text["title"], columns, placeholder=text["placeholder"] if "placeholder" in text else "Choose columns to sort",
                                  max_selections=max_selections, key=f"sort_dataframe_multiselect_{key}")
    n = len(sort_columns)
    if n>0: st.write(text['direction'])
    col = st.columns(max_selections)

    sort_directions = {}
    for i, column in enumerate(sort_columns):
        with col[i]:
            direction = sac.switch(label=f"{column}", on_label=sorting_directions[0], off_label=sorting_directions[1],
                                    position='left', size='md')
        sort_directions[column] = direction

    if sort_columns:
        df = df.sort_values(by=sort_columns, ascending=[sort_directions[col] for col in sort_columns])

    return df

def filter_dataframe(df: pd.DataFrame,
                     text={"title":"Filter dataframe on",
                           "values": "Values for ",
                           "regex": "Substring of regex in "}) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
    )

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect(text["title"], df.columns, placeholder=text["placeholder"] if "placeholder" in text else "Choose columns to sort")
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"{text['values']} {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"{text['values']} {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"{text['values']} {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"{text['regex']} {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

    return df