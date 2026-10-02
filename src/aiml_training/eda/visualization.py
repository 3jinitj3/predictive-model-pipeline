import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import StrMethodFormatter, FuncFormatter
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import Literal


def create_figure(style_type:str, context_type:str, palette_type:str, **subplot_kwargs) -> tuple[Figure, Axes]:
    """
    
    """
    sns.set_theme(
        style=style_type,
        context=context_type,
        palette=palette_type
        )
    fig, ax = plt.subplots(**subplot_kwargs)
    return fig, ax


def chart_metadata(ax:Axes, ax_title:str, ax_xlabel:str, ax_ylabel:str, ax_fontsize:int) -> Axes:
    """
    
    """
    ax.set_title(title=ax_title, fontsize=ax_fontsize + 2, fontweight='bold')
    ax.set_xlabel(ax_xlabel, fontsize=ax_fontsize)
    ax.set_ylabel(ax_ylabel, fontisze=ax_fontsize)
    return ax


def style_ticks_grid(ax:Axes, grid_alpha:float, **tick_params_kwargs) -> Axes:
    """
    
    """
    ax.grid(alpha=grid_alpha)
    ax.tick_params(**tick_params_kwargs)
    return ax


def format_yaxis(ax:Axes, axis_type:Literal["%", "$", "K", "M"]) -> Axes:
    """
    
    """
    def formatter(func):
        ax.yaxis.set_major_formatter(FuncFormatter(func))
    match axis_type:
        case "%":
            formatter(lambda x, pos: f"{x:.2f}%")

        case "$":
            formatter(lambda x, pos: f"${x:.2f}")

        case "K":
            formatter(lambda x, pos: f"{x/1000:.0f}K")

        case "M":
            formatter(lambda x, pos: f"{x/1000000:.1f}M")
    return ax


def add_bar_labels(ax:Axes, label_type:Literal["%", "$", "K", "M"], **kwargs) -> Axes:
    """
    
    """
    for container in ax.containers:
        match label_type:
            case "%":
                formatter = lambda v: f"{v:.2f}%"
            case "$":
                formatter = lambda v: f"${v:,.2f}"
            case "K":
                formatter = lambda v: f"{v/1_000:.2f}K"
            case "M":
                formatter = lambda v: f"{v/1_000_000:.2f}M"
            case _:
                raise ValueError(f"Unsupported label type: {label_type}")
        labels = [formatter(value) for value in container.datavalues]
        ax.bar_label(container, labels=labels, padding=3, **kwargs)
    return ax


def clean_save_figure(fig:Figure, folder_name:str, png_name:str, show_plot:bool):
    """
    
    """
    sns.despine()
    fig.tight_layout()
    fig.savefig(os.path.join(folder_name, png_name))
    if show_plot:
        plt.show()


def hist_plot(data:pd.Series|pd.DataFrame, **kwargs) -> Axes:
    """
    
    """
    ax = sns.histplot(
        data=data,
        **kwargs
    )
    return ax


def bar_plot(data=pd.DataFrame, **kwargs) -> Axes:
    """
    
    """
    ax = sns.barplot(
        data=data,
        **kwargs
    )
    return ax


def box_plot(data=pd.DataFrame, **kwargs) -> Axes:
    """
    
    """
    ax = sns.boxenplot(
        data=data,
        **kwargs
    )
    return ax


def line_plot(data=pd.DataFrame, **kwargs) -> Axes:
    """
    
    """
    ax = sns.lineplot(
        data=data,
        **kwargs
    )
    return ax


def heatmap(data=pd.DataFrame, **kwargs) -> Axes:
    """
    
    """
    ax = sns.heatmap(
        data=data,
        **kwargs
    )
    return ax