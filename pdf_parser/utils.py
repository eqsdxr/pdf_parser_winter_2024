from collections.abc import Callable
from time import time
from memory_profiler import memory_usage

from pdf_parser.setup_loger import logger

from typing import Any


def check_data(data: list) -> None:
    '''
    Function that checks data. It is meant only 
    for using within Parser class.
    '''
    
    if not data or len(data) < 4 or not isinstance(data, list):
        raise Exception(f'Data is empty or corrupted.\n{data}')


def measure_time(func: Callable) -> None:
    '''Decorator that measures executing time of a function.'''
    def wrapper(*args, **kargs):
        start_time = time()
        result = func(*args, **kargs)
        end_time = time()

        logger.debug(
            f'Function {func.__name__} took '
            f'{end_time - start_time:.6f} seconds to execute.'
            )
        
        return result
    return wrapper


def cast_to_int_float(var: str) -> int | float | str:
    '''
    Tipically table fields can be of either str type 
    or int|float type, so this checking is required.
    '''
    # float
    if '.' in var:
        try:
            var = float(var)
        except Exception as e:
            logger.debug(
                f'''Exception while type casting {var} 
                of type {type(var)} to "float": {e}'''
                )
        return var
    # int
    try:
        var = int(var)
    except Exception as e:
        logger.debug(
            f'Exception while type casting {var} '
            f'of type {type(var)} to "int": {e}'
            )
    return var