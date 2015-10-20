
def sdv_import(path):
    ps = path.split('.')
    np = '.'.join(ps[:-1])
    md = __import__(np)
    for p in ps[1:]:
        md = getattr(md, p)
    return md
