# Simulated Annealing Allocation Tool (SAAT)

## Install

**Git**
```
git clone https://github.com/samuelweller21/SAAT.git
cd SAAT
```

**Install dependencies**

##### Linux
```
(python -m venv venv
source venv/bin/activate
pip install ipykernel
python -m ipykernel install --user --name="venv" --display-name="SAAT"
pip install -r requirements.txt)
```

##### Windows - run one by one
```
python -m venv venv
venv/Scripts/activate
pip install ipykernel
python -m ipykernel install --user --name="venv" --display-name="SAAT"
pip install -r requirements.txt
```

**Run tests**
```
pytest
```

See [Demo.ipynb](https://github.com/samuelweller21/SAAT/blob/main/Demo.ipynb) for example of use
