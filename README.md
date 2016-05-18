ankle
=====

[![Build Status](https://travis-ci.org/despawnerer/ankle.svg?branch=master)](https://travis-ci.org/despawnerer/ankle)
[![PyPI version](https://badge.fury.io/py/ankle.svg)](https://badge.fury.io/py/ankle)

`ankle` is a tool that finds elements inside HTML documents by comparing them with an HTML skeleton. It is most useful for testing markup returned by a server.

Definitely works on Python 2.7 and Python 3.4+.


Installation
------------

	$ pip install ankle


Usage
-----

```python
ankle.match(skeleton, document)
```

Return elements from document that match given skeleton.

Each element in skeleton is matched by tag name and attributes. Children of nodes in skeleton are checked as descendants of elements in the document.

Document and skeleton may be either HTML strings or a parsed etrees.


Caveats
-------

These would be nice to have, but are currently not implemented:

- Order of elements isn't checked
- Text within elements isn't checked


Example
-------

```python
import ankle

document = """
<html>
	<body>
		<h1>My document</h1>
		<p>
			Some text
		</p>
		<form id="subscription-form">
			<div>
				<input name="email" placeholder="Email"/>
			</div>
			<div>
				<button type="submit">Subscribe</button>
			</div>
		</form>
	</body>
</html>
"""

skeleton = """
<form>
	<input name="email">
	<button type="submit"></button>
</form>
"""

ankle.match(skeleton, document)  # will return a list with one element: the form in the document
```
