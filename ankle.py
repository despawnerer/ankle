import warnings
from lxml.html import html5parser
from six import string_types
from functools import wraps


__all__ = ['find', 'find_all', 'find_iter']


def find(skeleton, document):
    """
    Return first element from document that matches given skeleton.
    """
    return next(find_iter(skeleton, document), None)


def find_all(skeleton, document):
    """
    Return all elements from document that match given skeleton.
    """
    return list(find_iter(skeleton, document))


@wraps(find_all)
def match(skeleton, document):
    warnings.warn("match is deprecated, use find_all instead")
    return find_all(skeleton, document)


def find_iter(skeleton, document):
    """
    Return an iterator yielding elements from document
    that match given skeleton.

    Elements from the skeleton are matched with document's by tag name,
    attributes and text inside them.

    Children of elements in skeleton are matched to descendants of
    elements in the document.

    Skeleton may only contain one root element.

    `document` and `skeleton` may be either HTML strings or parsed etrees.
    """
    if isinstance(document, string_types):
        document = html5parser.document_fromstring(document)
    if isinstance(skeleton, string_types):
        skeleton = html5parser.fragment_fromstring(skeleton)

    bones = skeleton.getchildren()
    for element in find_bone_like_descendants(skeleton, document):
        if match_bones(bones, element) is not None:
            yield element


def match_bones(bones, element):
    result = []
    for bone in bones:
        matches = find_bone_like_descendants(bone, element)
        for match in matches:
            if match_bones(bone.getchildren(), match) is not None:
                result.append(match)
                break
        else:
            return None
    return result


def find_bone_like_descendants(bone, parent):
    attrs_path = ''.join(
        '[@{attr}=\'{value}\']'.format(attr=attr, value=value)
        for attr, value in bone.attrib.items()
    )
    path = './/{tag}{attrs}'.format(tag=bone.tag, attrs=attrs_path)
    elements = parent.findall(path)

    text = stripped(bone.text)
    if text:
        elements = [e for e in elements if stripped(e.text) == text]

    return elements


def stripped(text):
    return text and text.strip()
