from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, ColorBar, LassoSelectTool, DataTable, TableColumn, HoverTool, Button
from bokeh.transform import linear_cmap
from bokeh.palettes import Reds
from bokeh.layouts import column, row
from bokeh.io import curdoc
from umap import UMAP
import pandas as pd

#this script should be used in conjunction with lib_analysis.ipynb to generate a standalone app to explore library sequences
#

#which library to use
library= 'Norm_freq2_corr'

#load the dataframe
ref_123_df = pd.read_csv('./output/umap_df_pep.csv')

# Create a Bokeh ColumnDataSource with the embeddings and frequency values
source = ColumnDataSource(data=dict(
    x=ref_123_df['x'],
    y=ref_123_df['y'],
    Norm_freq=ref_123_df['Norm_freq'],
    Norm_freq1_corr=ref_123_df['Norm_freq1_corr'],
    Norm_freq2_corr=ref_123_df['Norm_freq2_corr'],
    Norm_freq3_corr=ref_123_df['Norm_freq3_corr'],
    Translation=ref_123_df['Translation'],
))

hover = HoverTool(tooltips=[
    ("index", "$index"),
    ("Translation", "@Translation"),
    ("Norm_freq1", "@Norm_freq1_corr"),
    ("Norm_freq2", "@Norm_freq2_corr"),
    ("Norm_freq3", "@Norm_freq3_corr")
])

# Create a linear color map that maps the frequency values to a red 8 point gradient, 
# but only use the top 7 in reverse so that dark red is highest and the lowest is just off white
color_mapper = linear_cmap(field_name=library, palette=Reds[8][6::-1], low=0, high=1)

# Create a scatter plot of the embeddings with the points colored by frequency
plot = figure(tools=['pan,wheel_zoom,box_zoom,reset',hover],title='UMAP Embeddings of Protein Sequences')
plot.scatter(x='x', y='y', source=source, color=color_mapper)
plot.add_tools(LassoSelectTool())

# Add a color bar to show the mapping between frequency and color
color_bar = ColorBar(color_mapper=color_mapper['transform'], width=8, location=(0, 0))
plot.add_layout(color_bar, 'right')

# create a table to display the selected points
columns = [TableColumn(field=col, title=col) for col in ref_123_df.columns[3:8]]
table = DataTable(source=source, columns=columns, width=400, height=400)



# create a button to save the selected points as a CSV file
button = Button(label="Save CSV", button_type="success")

# define a callback function for the button click
def save_csv():
    selected_indices = source.selected.indices
    if selected_indices:
        selected_data = {col: source.data[col][selected_indices] for col in source.column_names}
        selected_df = pd.DataFrame(selected_data)
        selected_df.to_csv("selected_pep_points.csv", index=False)
def changeLabel(button):
    if button.label == 'Save CSV':
        button.label = 'CSV Saved!'
    else:
        button.label = 'Save CSV'

button.on_click(save_csv)
button.on_click(lambda : changeLabel(button))



# define a callback function for the selection change event
def selection_change_callback(attrname, old, new):
    selected_indices = source.selected.indices
    if selected_indices:
        selected_data = {col: source.data[col][selected_indices] for col in source.column_names}
        selected_source.data = selected_data
    else:
        selected_source.data = {col: [] for col in source.column_names}

# create a new data source for the selected points
selected_source = ColumnDataSource({col: [] for col in source.column_names})
selected_table = DataTable(source=selected_source, columns=columns, width=600, height=600)

# add a selection change callback to the data source
source.selected.on_change('indices', selection_change_callback)


# combine the plot, tables, and button into a layout
layout = column(row(plot, selected_table), button)

curdoc().add_root(layout)