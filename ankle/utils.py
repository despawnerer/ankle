import six


def maybe_strip(text):
    return text and text.strip()


def is_string(value):
    return isinstance(value, six.string_types)
