# World Happiness app

## Get started

### Locally

Before launching the app, you'll need the following:

* Python from 3.6 to 3.8
* A new environment (`venv` or `conda`)

Install the packages in `requirements.txt` and start the app:

```
pip install -r requirements.txt
streamlit run app.py
```
Visit then `localhost:8501` and start playing with the data.

### Docker

Launch the following command:

```

docker image build -t streamlit:app .
```