# Python to Stata workflow utilities

installation (requires git to be installed)

```bash
pip install git+https://github.com/pmk-econ/stata_utils/
```


## clean_stata

```python 
from stata-utils import clean_stata
```

Python function that solves two known issues when using pandas.to_stata()

0. Replaces all potential NA placeholders with uniform `pd.nan`.

1. Object columns prevent writing DataFrames to Stata (Stata cannot handle `pd.NA` in numeric columns).  
   To fix:
   - Attempts conversion to numeric pandas columns using `pd.nan`.
   - If conversion fails, reverts to brute-force string conversion (which can later be `destring`ed in Stata).

2. Ensures `int64` dtype for numeric columns. This avoids mixed dtypes created by boolean masking, which can introduce Stata `.z_`-type missing values.
