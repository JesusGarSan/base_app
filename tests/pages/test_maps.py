from base_app import maps
import streamlit as st
import pandas as pd



col = st.columns(2)
with col[0]:
    location, zoom_start, tiles = maps.map_config_form()
map = maps.create_map(location, zoom_start, tiles)


data = None
data = {
    'town': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Zaragoza', 'Málaga', 'Bilbao'],
    'latitude': [40.4168, 41.3851, 39.4691, 37.3891, 41.6561, 36.7213, 43.2630],
    'longitude': [-3.7038, 2.1734, -0.3774, -5.9845, -0.8773, -4.4217, -2.9350],
    'population': [3300000, 1600000, 791000, 688000, 666000, 578000, 346000],
    'coastal': [False, True, True, False, False, True, True],
    'region': ['Centro', 'Cataluña', 'Comunidad Valenciana', 'Andalucía', 'Aragón', 'Andalucía', 'País Vasco']
}
data = pd.DataFrame(data)

if data is not None:
    with col[0]:
        display_circles, radius, color_column, tips, colormap = maps.circle_config_form(data)

    if display_circles:
        fg, colormap = maps.get_circles(data,radius,tips,color_column,colormap)
    else: fg = None

    with col[1]:
        if colormap is not None:
            colormap = maps.create_colorbar(colormap, data[color_column], color_column, 6)
            colormap.add_to(map)
        maps.show_map(map, feature_group_to_add=fg, use_container_width=True)

