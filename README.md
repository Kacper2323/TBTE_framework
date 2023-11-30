## TBTE Framework is (will be) a set of tools to train and evaluate machine learning based trading bots.

For now, I am still uncertain about the architecture of the project. It will for sure change over time, maybe completely. Right now I'm focusing on making it work with Binance API.

ApiWrapper.py is self explanatory, it contains a CallWrapper class handling communication with the servers.

DataManager.py contains a very basic class for saving/loading data. It will be responsible for collection and storage of different types of data. As the project grows I will add Postgres database, for now it works with .npy files.

TemporalDataUtils.py contains tools to analize and perform basing transformations for time dependant data, finding missing time ranges in data, plotting etc.

test notebook will contain some examples of the growth of the project.

Next steps:
- full api support
- decide on the data manager architecture
- make the data manager
- data pipelines for models
- build some basic models
- add methods for evaluation, both on historical data and in real time
- build more models :)