from scrape import find_date

try:
    print(find_date(input()))
except Exception as ex:
    import traceback
    tb = traceback.TracebackException.from_exception(ex, capture_locals=True)
    print(''.join(tb.format()))
