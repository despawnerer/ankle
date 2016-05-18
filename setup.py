from setuptools import setup

setup(
    name='ankle',
    version='0.1.0',
    description='Find elements in HTML by matching them with a skeleton',
    url='https://github.com/despawnerer/ankle',
    author='Aleksei Voronov',
    author_email='despawn@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    py_modules=['ankle'],
    install_requires=[
        'lxml>=3',
        'html5lib>=0.9999999',
        'six>=1.0'
    ]
)
