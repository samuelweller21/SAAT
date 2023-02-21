# Simulated Annealing Allocation Tool (SAAT)

## Install

**Git**
```
git clone xyz
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

##### Windows 
```
python -m venv venv &^
venv/Scripts/activate &^
pip install ipykernel &^
python -m ipykernel install --user --name="venv" --display-name="SAAT" &^
pip install -r requirements.txt
```

**Run tests**
```
pytest
```

See Demo.ipynb for example of use
