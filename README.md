# Uniwatcher

An Ethereum scraper that sends notifications on new Uniswap tokens.
Token info is retrieved from the [Uniswap Subgraph](https://thegraph.com/explorer/subgraph/uniswap/uniswap-v2), and notifications are sent via [Pushover](https://pushover.net).

## Install

```bash
pip install -r requirements.txt
```

## Configure

Check out the sample YAML configuration file.

## Run

```bash
python -m uniwatcher -p config.yaml
```
