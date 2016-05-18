ankle
=====

[![Build Status](https://travis-ci.org/despawnerer/ankle.svg?branch=master)](https://travis-ci.org/despawnerer/ankle)
[![PyPI version](https://badge.fury.io/py/ankle.svg)](https://badge.fury.io/py/ankle)

`ankle` is a tool that finds elements inside HTML documents by comparing them with an HTML skeleton. It is useful in testing to check markup returned by a server or possibly web scraping.

Works on Python 2.7 and Python 3.4+.


Installation
------------

	$ pip install ankle


Usage
-----

```python
ankle.find_all(skeleton, document)
```

Return elements from document that match given skeleton.

Elements from the skeleton are matched with document's by tag name, attributes and text inside them.

Children of elements in skeleton are matched to descendants of the respective elements in the document.

Skeleton may only contain one root element.

`document` and `skeleton` may be either HTML strings or parsed etrees.


```python
ankle.find(skeleton, document)
```

Return the first element that matches given skeleton in the document.


```python
ankle.find_iter(skeleton, document)
```

Return an iterator that yields matching elements from the document. See `find_all` for details.


Caveats
-------

These features are currently not implemented:

- Order of elements isn't checked
- Text between elements isn't checked
- Class attribute is checked by strict equality, but it may be desirable to ignore classes that aren't present in the skeleton


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

ankle.find(skeleton, document)  # will return the <form> element from the document
```
