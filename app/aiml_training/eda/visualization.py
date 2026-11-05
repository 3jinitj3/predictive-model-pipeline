import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import Literal


def text_formatter(text:str, sanitize_to:Literal["file", "title"]) -> str:
    """
    Formats text to display titles or filenames.

    Args:
        text: Text to format.
        sanitize_to: Target output. Must be either ``'file'`` or ``'title'``.

    Returns:
        The formatted text. File formatting  produces a lowercase, underscore-separated string, while
        title fomatting produces a title cased, space-separated string.
    """
    if sanitize_to.strip().lower() == 'file':
        return '_'.join(text.strip().split()).lower()
    return text.strip().replace('_', ' ').title()


def create_figure( **subplot_kwargs) -> tuple[Figure, Axes]:
    """
    Create Matplotlib Figure and Axes using standardized plot settings.

    Args:
        **subplot_kwargs: Additional keyword arguments passed to ``matplotlib.pyplot.subplots``.
                        The default figure size is ``(12, 8)`` unless overwritten.
        
    Returns:
        A tuple  containing the created Matplotlib ``Figure`` and ``Axes``.

    Notes:
        Applies the following Seaborn theme defaults:
            - ``style='ticks'``
            - ``context='talk'``
            - ``palette='Set2'``
            
        Applies the following ``fig.subplot_adjust`` defaults:
            - ``top=.90``
            - ``bottom=.25``
    """
    subplot_kwargs.setdefault('figsize', (12, 8))
    sns.set_theme(style='ticks', context='talk', palette='Set2')
    fig, ax = plt.subplots(**subplot_kwargs)
    fig.subplots_adjust(top=.90, bottom=.25)
    return fig, ax


def chart_metadata(ax:Axes, ax_title:str, ax_xlabel:str, ax_ylabel:str) -> Axes:
    """
    Apply standardized chart title and axis label formatting.

    Args:
        ax: Matplotlib ``Axes`` object to modify.
        ax_title: Chart title.
        ax_xlabel: ``xaxis`` label.
        ax_ylabel: ``yaxis`` label.

    Returns:
        Axes: Updated Matplotlib ``Axes`` object.

    Notes:
        Applies the following label setting by default:
        - ``ax.set_title``: ``fontsize=22``
        - ``ax.set_title``: ``'fontweight=``'bold'``
        - ``ax.set_xlabel``: ``fontsize=18``
        - ``ax.set_ylabel``: ``fontsize=18``
    """
    ax.set_title(label=ax_title, fontsize=22, fontweight='bold')
    ax.set_xlabel(ax_xlabel, fontsize=18)
    ax.set_ylabel(ax_ylabel, fontsize=18)
    return ax


def style_ticks_grid(ax:Axes, xlabel_rotation:bool=False, **tick_params_kwargs) -> Axes:
    """
    Apply standardized tick and grid styling.

    Args:
        ax: Matplotlib ``Axes`` object to modify.
        xlabel_rotation: Rotate ``xaxis`` tick labels by 30 degrees when
            ``True``.
        **tick_params_kwargs: Additional keyword arguments passed to
            `ax.tick_params()``.

    Returns:
        Axes: Updated Matplotlib ``Axes``object.

    Notes:
        Applies the following default tick settings unless overwritten:
        - ``labelsize=13``
        - ``direction='out'``
        - ``length=10``   
        - ``width=2``
        - ``pad=5``

        Applies grid formatting using:
        - ``alpha=0.50``
        - ``linestyle='-.'``
    """
    tick_params_kwargs.setdefault('labelsize', 13)
    tick_params_kwargs.setdefault('direction', 'out')
    tick_params_kwargs.setdefault('length', 10)
    tick_params_kwargs.setdefault('width', 2)
    tick_params_kwargs.setdefault('pad', 5)
    ax.grid(alpha=.50, linestyle='-.')
    if xlabel_rotation:
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
    ax.tick_params(**tick_params_kwargs)
    return ax


def format_yaxis(ax:Axes, axis_type:Literal["%", "$", "K", "M"]) -> Axes:
    """
    Formats ``yaxis`` tick labels as percentages, currency, thousands or millions.

    Args:
        ax: Matplotlib axis to format.
        axis_type: Tick label format identifier, ``['%', '$', 'K', 'M']``.

    Returns:
        ``Axes`` object with formatted ``yaxis`` tick labels.
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
    Formats bar labels as percentage, currency, thousands, or millions.

    Args:
        ax: Matplotlib axis to format.
        label_type: Bar label format identifier, ``['%', '$', 'K', 'M']``.

    Returns:
        ``Axes`` object with formatted bar labels.
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


def clean_save_figure(fig:Figure, save:bool=False, folder_name:str|None = None, png_name:str| None = None) -> None:
    """
    Applies final plot formatting, displays the figure, and gives the option to save.

    Args:
        fig: Matplotlib figure object.
        save: If ``True``, saves figure as a PNG file. 
        folder_name: Destination folder to save figure.
        png_name: Output PNG filename.

    Returns:
        None
    """
    sns.despine()
    fig.tight_layout(pad=1)
    if save:
        fig.savefig(os.path.join(folder_name, png_name))
    plt.show()



def hist_plot(data:pd.Series|pd.DataFrame, x:str, title:str, bins:int=30, hue:str|None = None, save:bool=False, **hist_kwargs) -> tuple[Figure, Axes]:
    """
    Displays a histogram plot for a specified distribution.

    Args:
        data: ``pd.Series`` or ``pd.DataFrame``.
        x: Column name of values to plot.
        title: Title of plot.
        bins: Number of bins in the distribution.
        hue: Column name used to group and color histogram elements.
        save: If ``True``, saves the figure using the formatted plot title in the project's ``Charts`` directory.
        **hist_kwargs: Additional arguments to be passed to ``sns.histplot``.

    Returns:
        Tuple: ``tuple`` containing the matplotlib ``Figure`` and ``Axes`` objects.

    Notes:
        Applies ``sns.histplot`` default settings unless overwritten.
            - ``kde=True``
            - ``stat='count'``
            - ``edgecolor='black'``
            - ``linewidth=.50``
            - ``color='slategrey'``
            - ``alpha=.60``

        Additional behavior:
            - Title and axis labels are automatically formatted.
            - ``Figure`` is automatically cleaned before display.
            - If ``save=True``, figures are saved to the project's ``'Charts'`` directory using the formatted plot title.
    """
    hist_kwargs.setdefault('kde', True)
    hist_kwargs.setdefault('stat', 'count')
    hist_kwargs.setdefault('edgecolor', 'black')
    hist_kwargs.setdefault('linewidth', .5)
    hist_kwargs.setdefault('color', 'slategrey')
    hist_kwargs.setdefault('alpha', .60)
    fig, ax = create_figure()
    sns.histplot(data=data, ax=ax, x=x, bins=bins, hue=hue, **hist_kwargs)
    chart_metadata(ax=ax, ax_title=text_formatter(title, 'title'), ax_xlabel=text_formatter(x, 'title'), ax_ylabel='Count')
    clean_save_figure(fig=fig, folder_name='Charts', png_name=f'{text_formatter(title, "file")}.png', save=save)
    return fig, ax


def bar_plot(data:pd.DataFrame, x:str, y:str, title:str, bar_label:Literal["%", "$", "K", "M"]|None = None, x_rotation:bool=False, save:bool=False,  **bar_kwargs) -> tuple[Figure, Axes]:
    """
    Displays a formatted bar plot for a specified ``pd.DataFrame``.

    Args: 
        data: ``pd.DataFrame``.
        x: Column name used for bar categories.
        y: Column name containing bar height values.
        title: Title of plot.
        bar_label: Format bar labels as ``'%'``, ``'$'``, ``'K'``, or ``'M'``.
        x_rotation: Option to rotate longer ``xtick`` labels.
        save: If ``True``, saves the figure using the formatted plot title in the project's ``Charts`` directory.
        **bar_kwargs: Additional arguments to be passed to ``sns.barplot``. 

    Returns:
        tuple: ``tuple`` containing matplotlib ``Figure`` and ``Axes``.

    Notes:
        Applies ``sns.barplot`` default settings unless overwritten.
            - ``hue='x'``
            - ``width=.60``
            - ``dodge=False``

        Additional behaviors:
            - Title and axis labels are automatically formatted.
            - ``Figure`` is automatically cleaned before display.
            - If ``save=True``, figures are saved to the project's ``Charts`` directory using the formatted plot title.
    """
    bar_kwargs.setdefault('hue', x)
    bar_kwargs.setdefault('width', .60)
    bar_kwargs.setdefault('dodge', False)
    fig, ax = create_figure()
    sns.barplot(data=data, ax=ax, x=x, y=y,**bar_kwargs)
    if bar_label:
        add_bar_labels(ax=ax, label_type=bar_label)
    chart_metadata(ax=ax, ax_title=text_formatter(title, 'title'), ax_xlabel=text_formatter(x, 'title'), ax_ylabel=text_formatter(y, 'title'))
    style_ticks_grid(ax=ax, xlabel_rotation=x_rotation)
    clean_save_figure(fig=fig, folder_name='Charts', png_name=f'{text_formatter(title, "file")}.png', save=save)
    return fig, ax


def box_plot(data:pd.DataFrame, x:str, y:str, title:str, x_rotation:bool=False, save:bool=False, **box_kwargs) -> tuple[Figure, Axes]:
    """
    Displays a formatted box plot for a specified ``pd.DataFrame``.

    Args:
        data: ``pd.DataFrame``.
        x: Column name used for box categories.
        y: Column name containign values used to calculate quantiles and outliers.
        title: Title of plot.
        x_rotation: Option to rotate longer ``xtick`` labels.
        save: If ``True``, saves the figure using the formatted plot title in the project's ``Charts`` directory.
        **box_kwargs: Additional arguments to be passed to ``sns.boxplot``.

    Returns:
        tuple: ``tuple`` containing matplotlib ``Figure`` and ``Axes``.

    Notes:
        Applies ``sns.boxplot`` default settings unless overwritten:
            - ``hue='x'``

        Additional behaviors:
            - Title and axis labels are automatically formatted.
            - ``Figure`` is automatically cleaned before display.
            - If ``save=True``, figures are saved to the project's ``Charts`` directory using the formatted plot title.
    """
    box_kwargs.setdefault('hue', x)
    fig, ax = create_figure()
    sns.boxplot(data=data, ax=ax, x=x, y=y, **box_kwargs)
    chart_metadata(ax=ax, ax_title=text_formatter(title, 'title'), ax_xlabel=text_formatter(x, 'title'), ax_ylabel=text_formatter(y, 'title'))
    style_ticks_grid(ax=ax, xlabel_rotation=x_rotation)
    clean_save_figure(fig=fig, folder_name='Charts', png_name=f'{text_formatter(title, "file")}.png', save=save)
    return fig, ax


def line_plot(data:pd.DataFrame, x:str, y:str, hue:str, title:str, x_rotation:bool=False, save:bool=False, **line_kwargs) -> tuple[Figure, Axes]:
    """
    Displays a formatted line plot for a specified ``pd.DataFrame``.

    Args:
        data: ``pd.DataFrame``.
        x: Column name used for line plot categories.
        y: Column name containing values used to measure trend.
        hue: Column names of categories used for color line elements.
        title: Title of plot.
        x_rotation: Option to rotate longer ``xtick`` labels.
        save: If ``True``, saves figure using the formatted plot title in the project's ``Charts`` directory. 
        **line_kwargs: Additional arguments to be passed to ``sns.lineplot``.

    Returns:
        tuple: ``tuple`` containing matplotlib ``Figure`` and ``Axes``.

    Notes:
        Applies ``sns.lineplot`` default settings unless overwritten:
            - ``linewidth=3``
            - ``style='hue'``
            - ``markers=True``
            - ``errorbar=None``

        Additional behaviors:
            - Title and axis labels are automatically formatted.
            - ``Figure`` is automatically cleaned before display.
            - If ``save=True``, figures are saved to the project's ``Charts`` directory using the formatted plot title.
    """
    line_kwargs.setdefault('linewidth', 3)
    line_kwargs.setdefault('style', hue)
    line_kwargs.setdefault('markers', True)
    line_kwargs.setdefault('errorbar', None)
    fig, ax = create_figure()
    sns.lineplot(data=data, ax=ax, x=x, y=y, hue=hue, **line_kwargs)
    chart_metadata(ax=ax, ax_title=text_formatter(title, 'title'), ax_xlabel=text_formatter(x, 'title'), ax_ylabel=text_formatter(y, 'title'))
    ax.legend(title=text_formatter(hue, 'title'), loc='center left', bbox_to_anchor=(1.02, 1), fontsize=10, title_fontsize=12)
    style_ticks_grid(ax=ax, xlabel_rotation=x_rotation)
    clean_save_figure(fig=fig, folder_name='Charts', png_name=f'{text_formatter(title, "file")}.png', save=save)
    # Need to add a way to title the x and y axis context titles and subtitls
    return fig, ax


def heatmap(data:pd.DataFrame, title:str, save:bool=False,  **heat_kwargs) -> tuple[Figure, Axes]:
    """
    Displays a formatted heatmap for a specified ``pd.DataFrame``.

    Args:
        data: ``pd.DataFrame``.
        title: Title of plot.
        save: If ``True``, saves the figure using the formatted plot title in the project's 'Charts' directory.
        **heat_kwargs: Additional arguments to be passed to ``sns.heatmap``.

    Returns:
        tuple: ``tuple`` containing matplotlib ``Figure`` and ``Axes``.

    Notes:
        Applies ``sns.heatmap`` default settings unless overwritten:
            - ``cmap='coolwarm'``
            - ``annot=True``
            - ``fmt='.2f'``
            - ``linewidths=.50``
            - ``linecolor='black'``
            - ``cbar=True``
            - ``center=0``
            - ``square=True``

        Additional behaviors:
            - Figure is automatically cleaned before display.
            - Correclation matrix index and column names are automatically formatted.
            - If ``save=True``, figures are saved to the project's ``Charts`` directory using the formatted plot title.
    """
    heat_kwargs.setdefault('cmap', 'coolwarm')
    heat_kwargs.setdefault('annot', True)
    heat_kwargs.setdefault('fmt', '.2f')
    heat_kwargs.setdefault('linewidths', .5)
    heat_kwargs.setdefault('linecolor', 'black')
    heat_kwargs.setdefault('cbar', True)
    heat_kwargs.setdefault('center', 0)
    heat_kwargs.setdefault('square', True)
    data.columns = [text_formatter(col, 'title') for col in data.columns]
    data.index = [text_formatter(index, 'title') for index in data.index]
    fig, ax = create_figure()
    sns.heatmap(data=data, ax=ax, **heat_kwargs)
    clean_save_figure(fig=fig, folder_name='Charts', png_name=f'{text_formatter(title, "file")}.png', save=save)
    return fig, ax
