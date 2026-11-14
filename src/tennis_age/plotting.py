"""Plot Tennis Abstract career age differences."""

import matplotlib.pyplot as plt


def plot_age_difference(data):
    """Plot player age against player-minus-opponent age difference."""
    fig, ax = plt.subplots(figsize=(12, 7))
    colors = {"won": "#43b5d8", "lost": "#8c3b8f"}
    for result, group in data.groupby("result"):
        ax.scatter(
            group["age_player"],
            group["age_diff"],
            c=colors.get(result, "gray"),
            label=result.title(),
            alpha=0.7,
            s=28,
        )
    ax.axhline(0, color="gray", linewidth=1)
    _style_plot(ax)
    return ax


def _style_plot(ax):
    ax.set_xlabel("Player age")
    ax.set_ylabel("Player age - opponent age")
    ax.set_title("Career Matches by Age Difference", loc="left")
    ax.grid(alpha=0.2)
    ax.legend(frameon=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
