def dict_slice(d, start, end):
    items = list(d.items())
    
    sliced_items = items[start:(end + 1)]
    
    sliced_dict = dict(sliced_items)
    
    return sliced_dict