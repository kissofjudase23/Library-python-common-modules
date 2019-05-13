import collections


def flatten(d, *, parent_key='', sep='.'):

    items = list()

    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, parent_key=new_key, sep=sep).items())
        else:
            # dictionary item (new_key, v)
            items.append((new_key, v))

    return dict(items)
