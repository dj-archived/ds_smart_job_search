---
title: Smart Job Search

---


####  [Index](https://dujm.github.io/ds_smart_job_search)&nbsp;  | &nbsp;    [Cookie Cutter Dash](https://github.com/jackdbd/cookiecutter-dash)



### 1. Prepare my Dash app template

```
# Download cookie Cutter Dash app template
$ pip install cookiecutter
$ cookiecutter https://github.com/jackdbd/cookiecutter-dash


# Add directories
mkdir src
mkdir docs
rm -r utility

# Create an environment named job
$ conda create -n job python=3.7 anaconda

# Activate my environment job
conda activate job

# Install packages in requirements.txt
job$ pip install -r requirements.txt

# Export my environment dependencies to a yml file
conda env export > job.yml

# Pin the dependencies in requirements.txt
pip freeze > requirements.txt

# Rename app.py as app_template.py
# Create my app file app.py based on the app_template.py


# Install some packages
conda install dash dash-core-components dash-html-components dash-renderer -c conda-forge



```

<br>

### 2. Add data in my Dash app

```

```

---  

### References  
 * [Cookie Cutter Dash](https://github.com/jackdbd/cookiecutter-dash)
