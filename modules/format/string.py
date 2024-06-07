def fit(content, length, fill='.', left_align=True):
    # Convert to string so numbers can work too
    cache_content = str(content)

    cache_return = cache_content

    for i in range(len(cache_content), length):
        if left_align:
            cache_return += fill
        else:
            cache_return = fill + cache_return
    
    return cache_return
