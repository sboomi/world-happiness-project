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

Then start a container named `wh_app` listening on `8501`.

```
docker container run -p 8501:8501 -d --name wh_app streamlit:app
```

Open `http://localhost:8501/` and play with the data.