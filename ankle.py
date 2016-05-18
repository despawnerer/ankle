from lxml.html import html5parser
from six import string_types


__all__ = ['match']


def match(skeleton, document):
    """
    Return elements from document that match given skeleton.

    Each element in skeleton is matched by tag name and attributes.
    Children of nodes in skeleton are checked as descendants of
    elements in the document.

    Document and skeleton may be either HTML strings or a parsed etrees.
    """
    if isinstance(document, string_types):
        document = html5parser.document_fromstring(document)
    if isinstance(skeleton, string_types):
        skeleton = html5parser.fragment_fromstring(skeleton)

    bones = skeleton.getchildren()
    matches = []
    for element in find_bone_like_descendants(skeleton, document):
        if match_bones(bones, element) is not None:
            matches.append(element)
    return matches


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
    return parent.findall(path)
