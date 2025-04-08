

def circle_config_form(data, default:bool=False, radius:float=50, colormap:str='hot', key:str=""):
    display_circles = st.checkbox("Display circle markers", default, key="circle_config_form_display_circles"+key)
    if not display_circles:
        return display_circles, radius, None, None, None
    
    col = st.columns(4)
    radius = col[0].number_input("Radius for the circles (meters)", min_value=0, value=radius, step=100, key="circle_config_form_radius"+key)
    color_column = col[1].selectbox("Column to use for coloring", data.columns,index=None, key="circle_config_form_color_column"+key)
    columns = col[2].multiselect("Colums to use as tips", data.columns, key="circle_config_form_columns"+key)
    tips = columns_to_tips(columns)
    
    colormap_options = plt.colormaps()
    index = colormap_options.index(colormap)
    colormap = col[3].selectbox("Select colormap", colormap_options,index, key="circle_config_form_colormap"+key)

    return display_circles, radius, color_column, tips, colormap
