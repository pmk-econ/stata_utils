import numpy as np
import pandas as pd

# replace any missings with old np.nan for conversion purposes
DEFAULT_MISSING_SENTINELS = {
    "": np.nan,
    " ": np.nan,
    ".": np.nan,
    "NA": np.nan,
    "N/A": np.nan,
    "NaN": np.nan,
    "nan": np.nan,
    "None": np.nan,
    "NULL": np.nan,
}

# main function
def clean_stata(
    df: pd.DataFrame,
    missing_sentinels: dict | None = None,
    in_place: bool = False,
) -> pd.DataFrame:
    """
    Clean a DataFrame so it is safe for Stata export.
    """

    if not in_place:
        df = df.copy()

    sentinels = DEFAULT_MISSING_SENTINELS.copy()
    if missing_sentinels:
        sentinels.update(missing_sentinels)

    # 1) Normalize missing sentinels
    non_num = df.columns[~df.dtypes.apply(pd.api.types.is_numeric_dtype)]
    for col in non_num:
        df[col] = (
            df[col]
                .astype("string")
                .str.strip()
                .replace(sentinels)
        )

    # 2) Convert safely to numeric, many almost non-missings are objects and dont allow stata-writer, convert to numeric or if not possible to string instead
    for col in non_num:
        s = df[col].astype("string")
        num = pd.to_numeric(s, errors="coerce")

        if s.notna().sum() == num.notna().sum():
            df[col] = num.astype("float64")
        else:
            df[col] = s.astype("object")

    # 3) Convert nullable ints to float64, this is very important if you want to avoid weird stata nas such as ".z_" will generate usual "."
    for col in df.columns:
        dtype_str = str(df[col].dtype)
        if pd.api.types.is_integer_dtype(df[col].dtype) and "Int" in dtype_str:
            df[col] = df[col].astype("float64")

    return df
