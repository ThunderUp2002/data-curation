# data-curation

The data contained in this repository was collected using the following API: https://github.com/henrygd/ncaa-api.

The data (contained in all_stats.csv) consists of team stats from the 2024 season (up through November 13) in football, women's volleyball, and women's soccer for all colleges that have a team for at least one of those sports. Each sport has a given metric to provide a rough measure of success:
* *Football*: Average point differential (points per game - opponents' points per game)
* *Volleyball*: Average hitting percentage differential (hitting percentage - opponents' hitting percentage)
* *Soccer*: Average goal differential (goals per game - opponents' goals per game)

Here is an example instance with a subset of the features:

| Ranking | +/- GPG | +/- Hitting % | +/- PPG | Average z-Score |
| ------- | ------- | ------------- | ------- | --------------- |
| BYU     | 0.4     | 0.072         | 13.92   | 0.84            |

Here is a summary of the data:

| Sport        | Sample Size | Metric Value Mean | Metric Value SD |
| ------------ | ----------- | ----------------- | --------------- |
| Football     | 133         | 3.03              | 11.36           |
| W Volleyball | 333         | 0.004             | 0.06            |
| W Soccer     | 339         | 0.03              | 0.95            |
| **Total**    | **356**     |                   |                 |

*Notes*: The metric value corresponds to the given sport (as discussed above). Additionally, the row containing the totals is based on the final dataset (after combining sports so each row contains one team), thus the sample size of 356.

All code used to collect and analyze the data can be found in data_curation.ipynb.