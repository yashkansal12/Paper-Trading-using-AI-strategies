from market_data.services import get_market_indices

def market_data(request):
    try:
        return {
            "market": get_market_indices()
        }
    except Exception as e:
        print("Context Processor Error:", e)
        return {
            "market": {}
        }





# from market_data.services import get_market_indices


# def market_data(request):
#     return {"market": get_market_indices()}
