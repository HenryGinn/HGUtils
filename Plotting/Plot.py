import os
import math

import matplotlib.pyplot as plt
import numpy as np

import Defaults as defaults
from Plotting.PlotShape import PlotShape
from Plotting.PlotUtils.SaveFigure import save_figure

class Plot():

    """
    An instance of Plot will be a single figure.
    This figure can have multiple subplots, and corresponding to
    each subplot is a Lines object. A Lines object has a collection
    of Line objects associated with it.
    """

    def __init__(self, plots_obj, lines_objects, plot_index):
        self.plots_obj = plots_obj
        self.plot_index = plot_index
        self.initialise_lines_objects(lines_objects)
        self.set_grid_size()

    def initialise_lines_objects(self, lines_objects):
        self.lines_objects = lines_objects
        self.count = len(self.lines_objects)
        if self.plots_obj.universal_legend:
            self.count += 1

    def set_grid_size(self):
        plot_shape_obj = PlotShape(self.count, self.plots_obj.aspect_ratio)
        self.rows, self.columns = plot_shape_obj.dimensions

    def create_figure(self):
        self.initialise_figure()
        self.populate_figure()
        self.output_figure()
        plt.close()

    def initialise_figure(self):
        self.fig, self.axes = plt.subplots(nrows=self.rows,
                                           ncols=self.columns,
                                           constrained_layout=True)
        self.flatten_axes()
    
    def flatten_axes(self):
        if isinstance(self.axes, np.ndarray):
            self.axes = self.axes.flatten()
        else:
            self.axes = [self.axes]

    def populate_figure(self):
        self.plot_axes()
        self.remove_extra_axes()
        self.add_plot_peripherals()
    
    def plot_axes(self):
        for ax, lines_obj in zip(self.axes, self.lines_objects):
            self.plot_lines(ax, lines_obj)
            self.set_subplot_labels(ax, lines_obj)

    def plot_lines(self, ax, lines_obj):
        plot_function_data = self.get_plot_function_data(ax, lines_obj)
        for line_obj in lines_obj.line_objects:
            self.plot_line_obj(ax, line_obj, plot_function_data)

    def get_plot_function_data(self, ax, lines_obj):
        plot_functions = {"plot": (self.plot_quantitative, ax.plot),
                          "semilogy": (self.plot_quantitative, ax.semilogy),
                          "semilogx": (self.plot_quantitative, ax.semilogx),
                          "loglog": (self.plot_quantitative, ax.loglog),
                          "scatter": (self.plot_quantitative, ax.scatter),
                          "bar": (self.plot_bar, ax.bar),
                          "pie": (self.plot_pie, ax.pie)}
        plot_function = plot_functions[lines_obj.plot_type]
        return plot_function

    def plot_line_obj(self, ax, line_obj, plot_function_data):
        data_type_function, plot_function = plot_function_data
        data_type_function(ax, line_obj, plot_function)
        
    def plot_quantitative(self, ax, line_obj, plot_function):
        plot_function(line_obj.x_values, line_obj.y_values,
                      color=line_obj.colour,
                      marker=line_obj.marker,
                      linestyle=line_obj.linestyle,
                      linewidth=line_obj.linewidth,
                      label=line_obj.label)
        
    def plot_bar(self, ax, line_obj, plot_function):
        plot_function(line_obj.x_values, line_obj.y_values)
        
    def plot_pie(self, ax, line_obj, plot_function):
        plot_function(line_obj.y_values)

    def set_subplot_labels(self, ax, lines_obj):
        self.set_title(ax, lines_obj)
        self.set_x_axis_label(ax, lines_obj)
        self.set_y_axis_label(ax, lines_obj)

    def set_title(self, ax, lines_obj):
        if lines_obj.title is not None:
            ax.set_title(lines_obj.title)

    def set_x_axis_label(self, ax, lines_obj):
        if lines_obj.x_label is not None:
            ax.set_xlabel(lines_obj.x_label)

    def set_y_axis_label(self, ax, lines_obj):
        if lines_obj.y_label is not None:
            ax.set_ylabel(lines_obj.y_label)

    def remove_extra_axes(self):
        extra_axes = len(self.axes) - self.count
        for ax, _ in zip(self.axes[::-1], range(extra_axes)):
            ax.remove()

    def add_plot_peripherals(self):
        self.set_suptitle()
        self.set_legend()

    def set_suptitle(self):
        if self.plots_obj.title is not None:
            self.fig.suptitle(f"{self.plots_obj.title}")

    def set_legend(self):
        if self.plots_obj.universal_legend:
            self.do_universal_legend()
        else:
            self.do_non_universal_legends()

    def do_universal_legend(self):
        ax = self.axes[-1]
        for line_obj in self.lines_objects[0].line_objects:
            ax.plot(1, 1, label=line_obj.label, color=line_obj.colour)
        ax.legend(loc="center", borderpad=2, labelspacing=1)
        ax.axis("off")

    def do_non_universal_legends(self):
        for ax, lines_obj in zip(self.axes, self.lines_objects):
            if lines_obj.legend:
                ax.legend(loc=lines_obj.legend_loc)

    def output_figure(self):
        if self.plots_obj.output == "Show":
            plt.show()
        elif self.plots_obj.output == "Save":
            save_figure(self)

defaults.load(Plot)
