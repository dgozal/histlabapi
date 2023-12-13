<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=1TSmni70LaZFjUYUUCtJ9Sc6LbHbxa0g7"><br>
</div>
<h3 align="center"><font size = "20">History as Data Science</font></h3>

-----------------

# History Lab API

The [History Lab](http://history-lab.org/) focuses on digitizing historical documents and turning them into a format more amenable to the tools of modern data analysis. As part of this, the History Lab has compiled a database of more than 3 million declassified historical documents. 

Traversing any large database of this sort can be tedious though. `histlabapi` is a Python library that aims to solve this, making it easier for users to access data from the History Lab's database by wrapping around the History Lab's API. 

## Installation
Installation is quite straightforward with pip. This package is only compatible with Python 3.9+ due to its usage of the [`requests`](https://requests.readthedocs.io/en/latest/) dependency and its reliance on [`sphinx`](https://www.sphinx-doc.org/en/master/) to generate its documentation.

```bash
$ pip install histlabapi
```

## Usage

Before getting to extracting documents left and right, its important to get some bearing on how the History Lab stores and structures its various documents. As such, I've compiled a quick guide where one can look up the various collections and fields that you can access through this API [here](https://histlabapi.readthedocs.io/en/latest/database.html)!

Once that's settled, one can use this package's various functions to extract information in all kinds of ways:
- An [overview](https://histlabapi.readthedocs.io/en/latest/usage.html#list-collections) of all the collections currently available in the API
- [Listing](https://histlabapi.readthedocs.io/en/latest/usage.html#entity-overview) all the entities of a certain type that appear across all collections
- Searching and extracting documents by [text](https://histlabapi.readthedocs.io/en/latest/usage.html#search-by-text), [entity](https://histlabapi.readthedocs.io/en/latest/usage.html#search-by-entity), [date](https://histlabapi.readthedocs.io/en/latest/usage.html#search-by-date) or [document ID](https://histlabapi.readthedocs.io/en/latest/usage.html#search-by-document-id)


## Documentation

Full documentation can be accessed at [Read the Docs](https://histlabapi.readthedocs.io)


## Support

Feel free to contact me at dg3279@columbia.edu if you have any questions and/or want to contribute!


## License

`histlabapi` was created by Derrick Gozal. It is licensed under the terms of the MIT license.


## Credits

`histlabapi` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
Also much thanks to Professor Raymond Hicks and the rest of the History Lab team for all the support in building up this package.