# Recreate the python virtual environment and reinstall libs on Windows.
# Chris Joakim, Microsoft, January 2022

$dirs = ".\venv\", ".\pyvenv.cfg"
foreach ($d in $dirs) {
    if (Test-Path $d) {
        echo "deleting $d"
        del $d -Force -Recurse
    } 
}

echo 'creating new venv ...'
python -m venv .\venv\

echo 'activating new venv ...'
.\venv\Scripts\Activate.ps1

echo 'upgrading pip ...'
python -m pip install --upgrade pip 

echo 'uinstall pip-tools ...'
pip install --upgrade pip-tools

echo 'displaying python location and version'
which python
python --version

echo 'displaying pip location and version'
which pip
pip --version

echo 'pip-compile requirements.in ...'
pip-compile --output-file .\requirements.txt .\requirements.in

echo 'pip install requirements.txt ...'
pip install -q -r .\requirements.txt

echo 'pip list ...'
pip list

echo 'done'