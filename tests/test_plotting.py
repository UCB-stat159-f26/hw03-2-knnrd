import matplotlib
import pandas as pd

matplotlib.use("Agg")

from tennis_age import plot_age_difference


def test_plot_age_difference_returns_axes():
    data = pd.DataFrame({
        "age_player": [20.0, 21.0],
        "age_diff": [-2.0, 1.5],
        "result": ["won", "lost"],
    })

    ax = plot_age_difference(data)

    assert ax.get_xlabel() == "Player age"
    assert ax.get_ylabel() == "Player age - opponent age"
    assert len(ax.collections) == 2
