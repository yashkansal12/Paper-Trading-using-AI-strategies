from market_data.services import get_market_indices


def market_data(request):
    return {"market": get_market_indices()}