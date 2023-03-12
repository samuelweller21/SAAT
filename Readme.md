# Welcome to SAAT

[![pypi](https://shields.io/github/v/release/samuelweller21/saat?include_prerelease)](https://pypi.org/project/saat/#history)
[![Documentation](https://img.shields.io/badge/API-documentation-blue)](https://samuelweller21.github.io/SAAT/)

SAAT (Simulated Annealing Allocation Tool) is a tool intended to optimise the allocation of individuals into groups across teams within an organisation.

## Purpose

Suppose we have some employees who want to learn more about their organisation.  Some know about HR, some finance, some marketing and others logistics.  The CEO decides the best way to do this is to put them into groups and get them to talk to one another.  Each employee has their specialism and diary as below: 

| Employee | Specialism | 1pm | 2pm | 3pm |
| -------- | ---------- | --- | --- | --- |
| Dave | Finance | Busy | - | - |
| Janette | Logistics | - | Busy | Busy |
| John | HR | - | Busy | - |
| ... | ... | | ... |

Ideally, the groups would have a good mix of specialisms, all be about the same size and have as many time slots in which the group can meet.  For large numbers, it's not trivial how to best allocate employees into groups; this is the problem which SAAT approaches.

## Docs

[![Documentation](https://img.shields.io/badge/API-documentation-blue)](https://samuelweller21.github.io/SAAT/)

## Install

**Library**

```py
pip install saat
```

**Jupyter Demos**

```
git clone https://github.com/samuelweller21/SAAT.git
cd SAAT

# Intall [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
poetry shell
poetry install

# Jupyter
python3 -m ipykernel install --user --name="SAAT" --display-name="SAAT"
```

**Run tests**
```
pytest
```

See [Tutorial](https://www.samuelweller21.github.io/SAAT/tutorial/data) section for more information or [Demo](https://github.com/samuelweller21/SAAT/blob/main/Demo.ipynb) for a notebook example.
