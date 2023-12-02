## TBTE Framework is (will be) a set of tools to train and evaluate machine learning based trading bots.

## For examples see **notebook.ipynb**. It's easier to keep them there since there is too many changes this early in the project.

For now, I am still uncertain about the architecture of the project. It will for sure change over time, maybe completely.

BinanceAPI.py is self explanatory, it contains a BinanceClient class handling communication with the servers.

DataManager.py contains a very basic class for saving/loading data. It will be responsible for collection and storage of different types of data. As the project grows I will add a Postgres database, for now it works with .npy files.

TemporalDataUtils.py contains tools to analize and perform basing transformations for time dependant data, finding missing time ranges in data, plotting etc.

Next steps:
- full api support
- decide on the data manager architecture
- make the data manager
- data pipelines for models (the plan is to build some custom sklearn transformers and pipelines)
- build some basic models
- add methods for evaluation, both on historical data and in real time
- build more models :)