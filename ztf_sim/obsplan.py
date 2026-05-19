"""Helpers for writing obsplan text files."""

import pandas as pd


EXPOSURE_TIME = 60.0
TIME_BETWEEN = 100.0
NUM_EXPOSURES = 1
PRIORITY_CODE = 0


def clean_angle(angle):
    """Convert a string or numeric angle to a float, or return None."""
    if isinstance(angle, str):
        angle = angle.strip()
        if angle == "" or angle.lower() == "nan":
            return None
        if "deg" in angle:
            angle = angle.replace("deg", "").strip()
    try:
        return float(angle)
    except (TypeError, ValueError):
        return None


def format_obsplan_line(ra_hours, dec_deg, target):
    """Format one obsplan line in the translate_plan.py convention."""
    return (
        f"{ra_hours:.4f} {dec_deg:.4f} "
        f"Y  {EXPOSURE_TIME:.1f} {TIME_BETWEEN:.1f} "
        f"{NUM_EXPOSURES} {PRIORITY_CODE} # {target}"
    )


def build_obsplan(df, output_file, target_col="target"):
    """Write an obsplan text file from a dataframe with RA/Dec columns."""
    df = df.copy()

    df["ra_deg"] = df["ra"].apply(clean_angle)
    df["dec_deg"] = df["dec"].apply(clean_angle)
    df = df.dropna(subset=["ra_deg", "dec_deg"])
    df["ra_hours"] = df["ra_deg"] / 15.0

    if target_col not in df.columns:
        df[target_col] = "target"

    df = df.rename(columns={target_col: "target"})

    with open(output_file, "w") as f:
        for _, row in df.iterrows():
            f.write(
                format_obsplan_line(row["ra_hours"], row["dec_deg"], row["target"])
                + "\n"
            )

    return output_file
