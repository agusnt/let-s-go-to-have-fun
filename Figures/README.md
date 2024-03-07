# Figures-Python

Scripts to automatically generate figures from an JSON file.

## Scripts

### gen-fig.py

This script generates graphs automatically from a _json_ description.
Examples of the json can be found in the folder `fig_example`.

First parameter is the `json` file, second parameter is the output file

```json
{
    "rows": , # integer; number of rows
    "columns": , # interger; number of columns
    "figsize": , # string; size of the figure (e.g. "10,10")
    "args": , # dictionary; key - dictionary to call maptlotlib.rc function
    "graphs": [  # array; the definition of each figure
        {
            "dx": , # integer; position of the figure (row)
            "dy": , # integer; position of hte figure (column)

            "data": , # string; name of the file with the data,
            "title": , # string; title of the graph,
            
            "type": , # string; type of graph (heatmap, scatter, bar)

            "size_bar": , # float (0 to 1.0); width of the bar (bar)

            "args": {
                # dict; Arguments for the specific graph function (e.g: edgecolor)
            },

            "axis": {
                "x": {
                    "label": , # string, label of axis x,
                    "ticks_label": [], # array of strings; ticks labels
                    "ticks": [], # array of floats; ticks
                    "minor_ticks": [], # array of floats; minor ticks
                    "grid": , # bool; enable grid
                    "subgrid": , # bool; enable subgrid
                    "max": , # float; upper limit of the axis
                    "min": , # float; lower limit of the axis
                    "args_labels": {
                        # dict; Arguments for the specific maptlotlib function (e.g: rotation)
                    },
                    "args_txt_labels": {
                        # dict; Arguments for the specific maptlotlib function (e.g: rotation)
                    }
                },
                "y": {
                ... # same that x
                } 
            },

            "legend" : [{
                "elems": [
                ], # array of strings; labels (value field of data.da) to show in the legend
                "args": {}, # dict; extra arguments for the legend function
            }], # dict; legend configuration, only elements in order will be printed

            "hline": {}, #Horizontal line, a dict as you will pass to axhline function

            "annotate" : {
                "general": [
                    {
                        "str": , # str; annotation value
                        "x": , # float; x position
                        "y": , # float; y position
                        "args" :  # dic; extra arguments for the function
                    }
                ],
                
                
                # ONLY Bar graph
                "name" : { # str; label to apply this annotations
                    # Annoate values when it is outside the graph
                    "round": , #  integer; how many decimals to rund it
                    "x": , #  float; extra x to add to the bar x position
                    "y": , #  float; extra y to add to the bar x position
                    "args" :  # dic; extra arguments for the function
                }
            },
            # ONLY Heatmap
            "cmap": , # string; colors of heatmap (gray)
            # ONLY Bar graph
            "order" : [], # array of str; order for the legend and bar
        }
    ]
}
```

The data file has the following format:

```json
[
    {
        "x": , # X-value
        "y": , # Y-value; array if stacked bar 
        "value": , # Value (used also for the label)
        "color": # Point color; array if stacked bar
        "marker": # Marker or Hatch; array if stacked var
        "legend": # Bool; True if we have to include this value into the legend, optional
    }
]
```
