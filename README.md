# Python to Stata workflow utilities

installation
```bash
pip install -e git+https://github.com/paul-konietschke/stata-utils.git#egg=stata-utils
```

## clean_stata
Python function that solves two knows issues when using pandas.to_stata()
  0. Replaces all potential NA placeholders with uniform pd.nan
  1. Object columns prevent wrting df to Stata: Usually numeric columns that contain pd.NA instead of pd.nan which is not accepted as numerical column by stata writer
    - attempts conversion to numerical pandas column with pd.nan
    - if it fails, reverts to brute force string column conversion which can later be destrung within stata
  2. Ensures int64 type for numerical columns instead of other column types that contain few nas because of internal boolean masking that generates .z_ type of NAs. 
