import re
import numpy as np
import pandas as pd


def build_mapper(csv_state_list: pd) -> pd.DataFrame:

    # created a dictonary to hold items
    state_vals = {
        "AL": 0,
        "AK": 0,
        "AZ": 0,
        "AR": 0,
        "CA": 0,
        "CO": 0,
        "CT": 0,
        "DE": 0,
        "FL": 0,
        "GA": 0,
        "HI": 0,
        "ID": 0,
        "IL": 0,
        "IN": 0,
        "IA": 0,
        "KS": 0,
        "KY": 0,
        "LA": 0,
        "ME": 0,
        "MD": 0,
        "MA": 0,
        "MI": 0,
        "MN": 0,
        "MS": 0,
        "MO": 0,
        "MT": 0,
        "NE": 0,
        "NV": 0,
        "NH": 0,
        "NJ": 0,
        "NM": 0,
        "NY": 0,
        "NC": 0,
        "ND": 0,
        "OH": 0,
        "OK": 0,
        "OR": 0,
        "PA": 0,
        "RI": 0,
        "SC": 0,
        "SD": 0,
        "TN": 0,
        "TX": 0,
        "UT": 0,
        "VT": 0,
        "VA": 0,
        "WA": 0,
        "WV": 0,
        "WI": 0,
        "WY": 0,
        "DC": 0,
        "AS": 0,
        "GU": 0,
        "MP": 0,
        "PR": 0,
        "UM": 0,
        "VI": 0,
    }

    # using regex, find all State Code strings
    state_code = re.findall("[A-Z]{2}", str(csv_state_list["State"]))

    # interate through State Code values and update count in "state_vals" dictionary
    for x in state_vals:
        state_vals.update({x: state_code.count(x)})

    # put updated data in a new dictionary and dataframe
    data = {"State": state_vals.keys(), "Val": state_vals.values()}
    csv_results = pd.DataFrame(data)
    # print(csv_results)
    return csv_results
