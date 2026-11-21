def err(det: str):
    """Returns a dict with 'status' = 'err' and 'detail' = `det`."""
    return {
        'status': 'err',
        'detail': det
    }

def log_err(e: Exception):
    """Returns a dict with a generic error message to expose to clients, while printing `e`."""
    print(e)
    return err('Couldn\'t get or save data')

def not_found():
    """Returns a dict with 'status' = 'not-found'."""
    return { 'status': 'not-found' }
