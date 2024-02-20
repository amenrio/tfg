# HOW TO RUN Master Checker

## Developing

### PYTHONPATH 

You need to append the **`src`** folder's path to your `PYTHONPATH`:

In **Maya** it looks like this:

```python
# Add the src folder to yout PYTHONPATH
import sys
sys.path.append("<repo_root_path>/src")

# Import master_checer module
import master_checker as MChecker

# Run it's UI
master_checker_ui = MChecker.MasterCheckerUI()
# Without any parameters, MasterCheckerUI will run at DEFAULT

# To run an specific Department checks, run this:
master_checker_ui = MChecker.MasterCheckerUI(department="<DEPARTMENT>")
# Where DEPARTMENT can be (in UPPERCASE): RIGGING, MODELING, SHADING...

```
