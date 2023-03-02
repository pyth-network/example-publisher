import random
from ..providers.pyth_replicator import manual_aggregate


def test_manual_aggregate_works():
    prices = [1, 2, 3, 4, 5, 6, 8, 10, 12, 14]
    random.shuffle(prices)

    agg_price, agg_confidence_interval = manual_aggregate(prices)
    assert agg_price == 6
    assert agg_confidence_interval == 4
