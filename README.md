<div align="center">
  <img src="http://history-lab.org/images/new-paper-stack.png"><br>
</div>
<h3 align="center"><font size = "10">History as Data Science</font></h3>

-----------------

# History Lab API

The [History Lab](http://history-lab.org/) focuses on digitizing historical documents and turning them into a format more amenable to the tools of modern data analysis. As part of this, the History Lab has compiled a database of more than 3 million declassified historical documents. 

Traversing any large database of this sort can be tedious though. `histlabapi` is a Python library that aims to solve this, making it easier for users to access data from the History Lab's database by wrapping around the History Lab's API. 

## Installation
Installation is quite straightforward with pip. This package is only compatible with Python 3.8+ due to its usage of the [`requests`](https://requests.readthedocs.io/en/latest/) dependency and its reliance on [`sphinx`](https://www.sphinx-doc.org/en/master/) to generate its documentation.

```bash
$ pip install histlabapi
```

## Usage

- TODO

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`histlabapi` was created by Derrick Gozal. It is licensed under the terms of the MIT license.

## Credits

`histlabapi` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).