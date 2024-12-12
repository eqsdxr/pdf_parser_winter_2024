def check_data(data: list) -> None:
    """Function that checks data. It is meant only for using within Parser class"""
    
    if not data or len(data) < 4:
        raise Exception(f'Data is empty or corrupted.\n{data}')