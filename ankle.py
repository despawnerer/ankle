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

    for element in document.iterdescendants():
        if node_matches_bone(element, skeleton):
            yield element


def node_matches_bone(node, bone):
    if is_string(bone) or is_string(node):
        return node == bone
    else:
        return (
            node.tag == bone.tag and
            all(bone.attrib[x] == node.attrib.get(x) for x in bone.attrib) and
            has_all_matching_elements(node, list(iter_child_nodes(bone)))
        )


def has_all_matching_elements(element, bone_list):
    if not bone_list:
        return True

    bones_iter = iter(bone_list)
    nodes_iters = [iter_child_nodes(element)]
    bone = next(bones_iter)
    while nodes_iters:
        try:
            node = next(nodes_iters[-1])
        except StopIteration:
            nodes_iters.pop()
            continue

        if node_matches_bone(node, bone):
            try:
                bone = next(bones_iter)
            except StopIteration:
                return True
        elif not is_string(node):
            nodes_iters.append(iter_child_nodes(node))
    else:
        return False


def iter_child_nodes(element):
    text = stripped(element.text)
    if text:
        yield text

    for child in element:
        yield child
        tail = stripped(child.tail)
        if tail:
            yield tail


def stripped(text):
    return text and text.strip()


def is_string(value):
    return isinstance(value, string_types)
