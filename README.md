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

Return all elements from document that match given skeleton.

Skeleton elements are compared with the document's by tag name,
attributes and text inside or between them.

Children of elements in the skeleton are looked for in the descendants of
matching elements in the document.

Order of elements in the skeleton is signficant.

Skeleton must contain one root element.

`document` and `skeleton` may be either HTML strings or parsed etrees.


```python
ankle.find(skeleton, document)
```

Return the first element that matches given skeleton in the document.


```python
ankle.find_iter(skeleton, document)
```

Return an iterator that yields elements from the document that
match given skeleton.

See `find_all` for details.


Caveats
-------

- Class attribute is checked by strict equality, but it may be desirable to ignore classes that aren't present in the skeleton
- Text inside and between elements is checked strictly, so, for example, if it's broken up by a <span> in the document, but presented without it in the skeleton, it won't be found
- There are no nice assertion failure messages when using in py.test so it's difficult to see what failed to match and why


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
			<h2>Subscribe for more information!</h2>
			<div class="control-row">
				<label for="email">Email</label>
				<input name="email" placeholder="Email"/>
			</div>
			<div class="control-row">
				<label for="tos">
					<input name="tos" type="checkbox" class="checkbox-input">
					<span class="checkbox-text">I agree to TOS</span>
				</label>
			</div>
			<div class="submit-row">
				<button type="submit">Subscribe</button>
			</div>
		</form>
	</body>
</html>
"""

skeleton = """
<form>
	Subscribe for more information!
	<label for="email">Email</label>
	<input name="email">
	<label for="tos">
		<input name="tos" type="checkbox">
		I agree to TOS
	</label>
	<button type="submit"></button>
</form>
"""

ankle.find(skeleton, document)  # will return the <form> element from the document
```
