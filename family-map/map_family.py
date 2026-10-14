import re

from lib.build_map import build_mapper
from lib.plot_map import plotting_map

import logging

from lib.gsheets import compare_dfs, Gsheet

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


GSHEET_NAME = "Subscriptions"
FAMILY_LIST_WORKSHEET_NAME = "Items"
STATE_COUNT_WORKSHEET_NAME = "state_count"

family_map = Gsheet(GSHEET_NAME, FAMILY_LIST_WORKSHEET_NAME)
state_count = Gsheet(GSHEET_NAME, STATE_COUNT_WORKSHEET_NAME)


def main():
    family_map.get_spreadsheet(GSHEET_NAME)
    family_map.get_worksheet(FAMILY_LIST_WORKSHEET_NAME)
    mapped_df = family_map.etl_family_data()

    updated_map_count = build_mapper(mapped_df)

    state_count.get_spreadsheet(GSHEET_NAME)

    og_state_count = state_count.get_sheet_items()
    old_df = state_count.convert_sheet_to_df(og_state_count)

    old_count_sum = old_df.iloc[:, 1].sum()
    new_count_sum = updated_map_count.iloc[:, 1].sum()

    if compare_dfs(old_df, updated_map_count):
        logger.info(
            f"SUM Counts equal; OLD_COUNT:{old_count_sum} = NEW_COUNT:{new_count_sum} No updates needed"
        )
    else:
        logger.warning(
            f"SUM Counts not equal; OLD_COUNT:{old_count_sum} != NEW_COUNT:{new_count_sum} updating {FAMILY_LIST_WORKSHEET_NAME} sheet!"
        )
        state_count.update_sheet(updated_map_count)
        logger.info(f"New SUM Count:{new_count_sum}")
        plotting_map(updated_map_count)


if __name__ == "__main__":
    main()
