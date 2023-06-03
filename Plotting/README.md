# Plotting

## Contents

1. [Overview and Structure](#overview-and-structure)
    1. [Figures](#figures)
    1. [Animate](#animate)
    1. [Figure](#figure)
    1. [Plot](#plot)
    1. [Data](#data)
1. [Usage](#usage)
1. [Features](#features)
    1. [Universal Legend](#universal-legend)
    1. [Subplot Adjustment](#subplot-adjustment)

## Overview and Structure

This is a tool designed to make creating figures with multiple subplots easier. The data is prescribed, and the creation of the figures is handled by the package.

### Figures

At the top level there is a Figures object. This contains all the information about the figures to be produced. This includes the data to be plotted, the title of the figures, if the figures are going to be shown or saved, the base path to be saved to if needed, the number of subplots per figure, and any appearance settings of the plots. It organises the creation of Figure objects, as if there is too much data for one figure, it will need to be splot over multiple.

### Animate

This is a subclass of Figures, and allows you to make animations. Creating animations is done through exactly the same process as creating figures, with one difference. The independent variables can't be animated, but the dependent variables will need to be passed in as a list or array where each element gives the values of the variable for each frame.

### Figure

The next level down is the Figure object. This arranges how the subplots will be arranged on the figure and organises the creation of the subplots which are handled by Plot objects. Adding the title and universal legend happens here. An aspect ratio can be specified, and it will try to arrange the plots to that ratio as closely as it can.

### Plot

A Plot object is responsible for each individual subplot. The subplot title, axis labels, plot legends, and the data to be put on the subplot are handled at this level. There are subclasses of Plot for different types of data object, and these classes follow the naming convention of appending "Plot" to the name of the data object they are associated with.

### Data

This class handles the data to be plotted. The most basic is a Lines object which handles quantititive data on a 2D plot. There is also a Bars object which handles bar charts, and a Pie object that handles pie charts. Colormesh and Surface are also subclasses which work with 3 dimensional data. As a rule of thumb, if two matplotlib plotting functions are sufficiently different, their data will be handled by two distinct subclasses of Data. Here are the subclasses of Data.

- Lines. This takes in a collection of Line objects. It also has an optional keyword argument called `plot_type` which controls whether the plot is made using `plot`, `semilogy`, `semilogx`, `loglog`, or `errorbar`. Each Line object corresponds to a single line on a subplot, and has a list of $x$ values and $y$ values. The Line object also has optional attributes that control the appearance of the line and the line label.
- Bars. This is similar to Lines, but it handles Bar objects which are similar to Line objects. The key distinction here is that the $x$ axis has qualitative data, and that prescribing the appearance of the bars is very different from lines. We note that a Bar object handles an entire series of data, and a Bars object handles a bar chart plot, so a single plot with two data series on it will be handled by one Bars object and two Bar objects.
- Pie. Pie charts cannot show multiple data series so this subclass does not have a correspondence to Line or Bar. This takes in all the arguments that the matplotlib pie function takes in, and also any of the arguments from the parent class, Plot.
- Colormesh. This shows a single data series with two dimensional input and one dimensional output. It takes in all arguments that the matplotlib pcolormesh function takes in and uses pcolormesh instead of pcolor.
- Surface. This shows a single data series with a two dimensional input and a one dimensional output. Different from Colormesh, this produces a plot in three spatial dimensions represented as a surface.

### Usage

The first step in creating a figure is specifying the data. Here is an example with plotting a single line on a graph. `lines_obj` is the Data object in this case, and we pass it in to `create_figures`.
    
    # Importing
    import numpy as np
    import hgutils.plotting

    # Creation of Line object
    x_values = np.arange(0, 2*np.pi, 0.1)
    y_values = np.sin(x_values)
    line_obj = plotting.line(x_values, y_values)

    # Creation of Lines object
    lines_obj = plotting.lines(line_obj)

    # Creation of figures
    plotting.create_figures(lines_obj)

If we want to create multiple lines, we can pass in a list of line objects. We can also give our figure some labels.


    # Importing
    import numpy as np
    import hgutils.plotting

    # Creation of Line object
    def get_line_obj(n):
        y_values = np.sin(n*x_values)
        label = f"n = {n}"
        line_obj = plotting.line(x_values, y_values, label=label)
        return line_obj

    x_values = np.arange(0, 2*np.pi, 0.01)
    x_coefficients = [1, 2, 3]
    line_objects = [get_line_obj(n) for n in x_coefficients]

    # Creation of Lines object
    title = "Sin(nx)"
    x_label = "My x axis label"
    y_label = "My y axis label"
    lines_obj = plotting.lines(line_objects, title=title, legend=True,
                            x_label=x_label, y_label=y_label)

    # Creation of figures
    plotting.create_figures(lines_obj)

We could have data split across multiple subplots. By default we have `subplots=None` and all subplots will be put on a figure. If subplots is specified and the subplots do not fit on one figure, they will be distributed across multiple. The number given by the subplots key-word is an upper bound on how many subplots there will be on a given figure, and the number of figures is as small as possible given that constraint.

    # Importing
    import numpy as np
    import hgutils.plotting

    def get_lines_obj(n):
        line_obj = get_line_obj(n)
        title = f"Sin({n}x)"
        x_label = "My x axis label"
        y_label = "My y axis label"
        lines_obj = plotting.lines(line_obj, title=title,
                                x_label=x_label, y_label=y_label)
        return lines_obj

    def get_line_obj(n):
        y_values = np.sin(n*x_values)
        line_obj = plotting.line(x_values, y_values)
        return line_obj

    # Creation of lines objects
    x_values = np.arange(0, 2*np.pi, 0.01)
    x_coefficients = list(range(1, 13))
    lines_objects = [get_lines_obj(n) for n in x_coefficients]

    # Creation of figures
    plotting.create_figures(lines_objects, subplots=6)

You can mix the types of plot within a figure. Here is an example that shows the other types of plot supported.

## Features

### Universal Legend

The universal legend is a tool that can be used if all subplots in a figure have the same legend. An extra blank subplot is created and the space is used to show a legend that corresponds to all plots. This can be activated by passing `universal_legend=True` as a keyword-value pair into the `create_figures` function, and any individual legends will be overruled.

### Subplot Adjustment

If the optional key-word argument, `adjust_subplots=True` is passed in to `create_figures` (or `create_animation`), then the matplotlib subplot adjustment tool will appear when the figures are created. The subplots are usually plotted with using the constrained layout, but in this case that will be turned off and tight layout used instead.