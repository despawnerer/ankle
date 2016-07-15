import ankle
import unittest


class SimpleTestCase(unittest.TestCase):
    def test_works(self):
        document = '''
            <form id="test1" class="form"></form>
            <form id="test2" class="form"></form>
        '''
        skeleton = '<form class="form"></form>'
        ankle.find_all(skeleton, document)


class FindTestCase(unittest.TestCase):
    def test_returns_first_found_element_when_found(self):
        document = '''
            <form id="test1" class="form"></form>
            <form id="test2" class="form"></form>
        '''
        skeleton = '<form class="form"></form>'
        element = ankle.find(skeleton, document)
        self.assertEqual(element.attrib['id'], 'test1')

    def test_returns_none_when_nothing_found(self):
        document = '<form id="test"></form>'
        skeleton = '<div class="other"></div>'
        self.assertIsNone(ankle.find(skeleton, document))


class MatchingTestCase(unittest.TestCase):
    def test_match_by_tag_name(self):
        document = '''
            <form id="test"></form>
        '''
        skeleton = '<form></form>'
        matches = ankle.find_all(skeleton, document)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].attrib['id'], 'test')

    def test_match_by_attribute(self):
        document = '''
            <form id="test1"></form>
            <form id="test2"></form>
        '''
        skeleton = '<form id="test1"></form>'
        matches = ankle.find_all(skeleton, document)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].attrib['id'], 'test1')

    def test_match_by_child(self):
        document = '''
            <form id="test1"><input name="match"></form>
            <form id="test2"><input name="no-match"></form>
        '''
        skeleton = '<form><input name="match"></form>'
        matches = ankle.find_all(skeleton, document)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].attrib['id'], 'test1')

    def test_match_by_descendant(self):
        document = '''
            <form id="test1">
                <div><span><input name="match"></span></div>
                <button>Submit</button>
            </form>
            <form id="test2">
                <input name="whatever">
                <div><button>Go</button></div>
            </form>
        '''
        skeleton = '<form><input name="match"></form>'
        matches = ankle.find_all(skeleton, document)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].attrib['id'], 'test1')

    def test_match_by_multiple_children(self):
        document = '''
            <form id="login">
                <input name="name">
                <input name="password">
            </form>
            <form id="some-other-form">
                <input name="no-match">
                <input name="different-input">
            </form>
        '''
        skeleton = '<form><input name="name"><input name="password"></form>'
        matches = ankle.find_all(skeleton, document)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].attrib['id'], 'login')

    def test_multiple_matches(self):
        document = '''
            <form id="test1"></form>
            <form id="test2"></form>
        '''
        skeleton = '<form></form>'
        matches = ankle.find_all(skeleton, document)
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].attrib['id'], 'test1')
        self.assertEqual(matches[1].attrib['id'], 'test2')

    def test_attribute_order_doesnt_matter(self):
        document = '<form method="POST" action="." id="test1"></form>'
        skeleton = '<form id="test1" action="." method="POST"></form>'
        matches = ankle.find_all(skeleton, document)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].attrib['id'], 'test1')

    def test_match_deep_descendants(self):
        document = '''
            <form id="test1">
                <div class="red">
                    <input name="wonderful">
                </div>
            </form>
            <form id="test2">
                <div class="red">
                    <input name="different">
                </div>
            </form>
        '''
        skeleton = (
            '<form><div class="red"><input name="wonderful"></form></div>'
        )
        matches = ankle.find_all(skeleton, document)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].attrib['id'], 'test1')

    def test_match_text(self):
        document = '''
            <form id="test1">
                <label for="name">
                    Correct label
                </label>
                <input name="name">
            </form>
            <form id="test2">
                <label for="name">
                    Wrong label
                </label>
                <input name="name">
            </form>
        '''
        skeleton = '''
            <form>
                <label for="name">Correct label</label>
                <input name="name">
            </form>
        '''
        matches = ankle.find_all(skeleton, document)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].attrib['id'], 'test1')

    def test_match_by_order(self):
        document = '''
            <form id="test1">
                <label for="name">Label</label>
                <input name="name">
            </form>
            <form id="test2">
                <input name="name">
                <label for="name">Label</label>
            </form>
        '''
        skeleton = '''
            <form>
                <label for="name">Label</label>
                <input name="name">
            </form>
        '''
        matches = ankle.find_all(skeleton, document)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].attrib['id'], 'test1')

    def test_matches_skeleton_with_just_text(self):
        document = '''
            <h1 id="test1">Correct title</h1>
            <h2 id="test2">Different title</h1>
        '''
        skeleton = '''
            <h1>Correct title</h1>
        '''
        matches = ankle.find_all(skeleton, document)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].attrib['id'], 'test1')

    def test_match_text_between_elements(self):
        document = '''
            <form id="test1">
                <label for="name">Label</label>
                Correct text
                <input name="name">
            </form>
            <form id="test2">
                <label for="name">Label</label>
                Incorrect text
                <input name="name">
            </form>
        '''
        skeleton = '''
            <form>
                <label for="name">Label</label>
                Correct text
                <input name="name">
            </form>
        '''
        matches = ankle.find_all(skeleton, document)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].attrib['id'], 'test1')

    def test_match_text_in_the_beginning_of_element(self):
        document = '''
            <form id="test1">
                Correct text
                <label for="name">Label</label>
                <input name="name">
            </form>
            <form id="test2">
                Incorrect text
                <label for="name">Label</label>
                <input name="name">
            </form>
        '''
        skeleton = '''
            <form>
                Correct text
                <label for="name">Label</label>
                <input name="name">
            </form>
        '''
        matches = ankle.find_all(skeleton, document)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].attrib['id'], 'test1')
