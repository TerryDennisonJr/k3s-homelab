import gspread
import logging
import pandas as pd
import os

from typing import Dict, List


from gspread import Worksheet
from google.oauth2.service_account import Credentials


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app_env = os.getenv("APP_ENV", "local")

if app_env == "kubernetes":
    logger.info("Running in K8S environment")

else:
    logger.info("Running in LOCAL environment")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_creds() -> Credentials:

    # creds = Credentials.from_service_account_file(file, scopes=SCOPES)
    creds = Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"], scopes=SCOPES
    )
    return creds


def compare_dfs(df1: pd.DataFrame, df2: pd.DataFrame) -> bool:
    return df1.equals(df2)


class Gsheet:
    def __init__(self, spreadsheet, worksheet):
        self.spreadsheet = spreadsheet
        self.worksheet = worksheet

    def get_spreadsheet(self, spreadsheet: str) -> gspread.Spreadsheet:
        client = get_creds()
        gsheet_client = gspread.authorize(client)
        spreadsheet_name = gsheet_client.open(spreadsheet)

        return spreadsheet_name

    def get_worksheet(self, worksheet: gspread.Worksheet) -> gspread.Worksheet:
        spreadsheet = self.get_spreadsheet(self.spreadsheet)
        worksheet = spreadsheet.worksheet(self.worksheet)

        return worksheet

    # def get_state_count(self) -> pd.DataFrame:
    #     sheet_id = self.get_spreadsheet(self.spreadsheet)
    #     worksheet_name = self.get_worksheet(sheet_id)
    #     sheet_data = worksheet_name.get_all_records()

    #     return sheet_data

    def etl_family_data(self) -> pd.DataFrame:
        subscriptions_sheet_data = self.get_sheet_items()
        family_data = pd.DataFrame(subscriptions_sheet_data)

        stripped_family_data = family_data[["Name", "State"]].copy()
        stripped_family_data = stripped_family_data.sort_values(
            by="State", ascending=True
        )

        updated_family_map_df = pd.DataFrame(stripped_family_data)

        return updated_family_map_df

    def get_sheet_items(self) -> List[Dict[str, int | float | str]]:
        worksheet_name = self.get_worksheet(self.worksheet)
        sheet_data = worksheet_name.get_all_records()

        return sheet_data

    def convert_sheet_to_df(
        self, df: List[Dict[str, int | float | str]]
    ) -> pd.DataFrame:
        df = pd.DataFrame(self.get_sheet_items())
        return df

    def update_sheet(self, df: pd.DataFrame):
        worksheet_name = self.get_worksheet(self.worksheet)
        worksheet_name.update([df.columns.values.tolist()] + df.values.tolist())
