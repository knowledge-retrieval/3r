# coding=utf-8


def unicode_only_string(obj):
    # str の encode として utf-8 以外は想定していない
    return unicode(obj, "utf-8") if (isinstance(obj, str)) else obj
