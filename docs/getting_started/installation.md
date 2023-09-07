---
icon: octicons/download-16
---

# Installation

## Install QuantBT
### Using Poetry
It is highly recommend you use [poetry](https://python-poetry.org/) to manage your virtual env

```bash
poetry add quantbt
```

### Using pip
If you wish to use pip, you can run the following:

```bash
pip install quantbt
```

----

## Dependencies
### Ta-Lib
[Ta-Lib]() is a very powerful technical analysis library that is written in C, thus providing fantastic performance. Unfortunately, it needs to be installed seperatly on your system.

Here's how
#### On Windows
Please follow the instructions [here](https://github.com/TA-Lib/ta-lib-python#windows)

#### On Mac
```
brew install ta-lib
```

#### On Linux

If you are on arch:
```
yay -S ta-lib
```

For other distros, please read [here](https://github.com/TA-Lib/ta-lib-python#linux)

#### Troubleshooting
Please refer to the [docs](https://github.com/TA-Lib/ta-lib-python#dependencies) for solution of any installation problems.
