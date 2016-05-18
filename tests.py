import ankle
import unittest


class MatchTest(unittest.TestCase):
    def test_match_by_tag_name(self):
        document = '''
            <form id="test"></form>
        '''
        skeleton = '<form></form>'
        matches = ankle.match(skeleton, document)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].attrib['id'], 'test')

    def test_match_by_attribute(self):
        document = '''
            <form id="test1"></form>
            <form id="test2"></form>
        '''
        skeleton = '<form id="test1"></form>'
        matches = ankle.match(skeleton, document)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].attrib['id'], 'test1')

    def test_match_by_child(self):
        document = '''
            <form id="test1"><input name="match"></form>
            <form id="test2"><input name="no-match"></form>
        '''
        skeleton = '<form><input name="match"></form>'
        matches = ankle.match(skeleton, document)
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
        matches = ankle.match(skeleton, document)
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
        matches = ankle.match(skeleton, document)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].attrib['id'], 'login')

    def test_multiple_matches(self):
        document = '''
            <form id="test1"></form>
            <form id="test2"></form>
        '''
        skeleton = '<form></form>'
        matches = ankle.match(skeleton, document)
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].attrib['id'], 'test1')
        self.assertEqual(matches[1].attrib['id'], 'test2')
