# Setup Instructions

Enviroment used during development:
* python 3.9
* Windows 10

Theorically this should be runnable on Linux, but this has not been tested.

To setup follow these steps:
* Create a python environment (below is an example with conda)
```
conda create -n environment_name python=3.9
conda activate environment_name
```
* Install all the required pacakges `pip install -r requirements.txt`
* Run the streamlit app `streamlit run app.py`

This should open a browser with the app running. If not, go to the url specificed in the command output of the last command.

Please open an issue for any feature requests and bugs. asfda 