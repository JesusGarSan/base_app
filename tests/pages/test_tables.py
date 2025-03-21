import base_app
from base_app import tables

base_app.config.default("Test | Tables")

import numpy as np
import pandas as pd
df = pd.DataFrame(np.random.rand(100, 10), columns=['A','B','C','D','E','F','G','H','I','K'])

df = tables.filter_dataframe(df)
columns = tables.column_selector(df)
tables.show_table(df, columns)  
tables.show_stats(df, columns)