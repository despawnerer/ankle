from lxml.html import html5parser

from .utils import is_string
from .match import node_matches_bone


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
    if is_string(document):
        document = html5parser.document_fromstring(document)
    if is_string(skeleton):
        skeleton = html5parser.fragment_fromstring(skeleton)

    for element in document.iterdescendants():
        if node_matches_bone(element, skeleton):
            yield element
