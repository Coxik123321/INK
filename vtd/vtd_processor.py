from vtd.mfl_parser import parse_mfl
from vtd.ut_parser import parse_ut

def process_vtd(record):
    if record["method"] == "MFL":
        record["depth_percent"] = parse_mfl(
            record["signal"], record["calibration"]
        )
    elif record["method"] == "UT":
        record["depth_percent"] = parse_ut(
            record["t_nom"], record["t_meas"]
        )
    return record
