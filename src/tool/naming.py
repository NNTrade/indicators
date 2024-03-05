from ..indicator_list import Indicators
from typing import List
import re

def contains_invalid_symbols(s):
    # Define the pattern to match the invalid symbols
    pattern = r'[()\[\]|_]'

    # Check if the string contains any of the invalid symbols
    return bool(re.search(pattern, s))

def get_col_name(indicator:Indicators, parameters:List[str], depends_columns:List[str], field:str|None=None)->str:
    assert contains_invalid_symbols(indicator.value) == False, f"Indicator {indicator.value} contain invalid symbols"
    ret_field = indicator.value
    
    if field is not None:
        assert contains_invalid_symbols(field) == False, f"Field {field} contain invalid symbols"
        ret_field = ret_field+"_"+field
    
    return f'{ret_field}({"|".join(parameters)})[{"|".join(depends_columns)}]'