import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging
import pandas as pd
from pathlib import Path
import os
import re

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


def get_file_path(path: str):
    directory = Path.cwd()
    map_file = f"{directory}/{path}"
    os.replace(map_file, map_file)
    update = os.path.getmtime(map_file)
    last_updated = datetime.fromtimestamp(update)
    new_dt_object = last_updated.replace(microsecond=0)
    logger.info(f"Latest Update @{new_dt_object}")
    logger.info(f"{map_file} updated!")


def plotting_map(map_df: pd.DataFrame):
    # plot the dataframe in a map
    fig = go.Figure(
        data=go.Choropleth(
            locations=map_df["State"],  # Spatial coordinates
            z=map_df["Val"],  # Data to be color-coded
            locationmode="USA-states",  # set of locations match entries in `locations`
            colorscale="Reds",
            colorbar_title="Count",
        )
    )

    fig.update_layout(
        title_text="Dennison Families by State",
        geo_scope="usa",  # limit map scope to USA
    )

    # send the interactive map to a html file
    map_path = "map.html"
    answ = fig.write_html(map_path)
    get_file_path(map_path)
    # fig.show()
    return answ
