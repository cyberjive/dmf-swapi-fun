import requests


def swapi_get_wrapper(endpoint: str) -> list:
    """
    function to handle the SWAPI API return 
        pagination and return all results
    Flattens the output to a return list
    """
    output = []
    swapi_full_url = "https://swapi.dev/api/" + endpoint
    request_output = requests.get(swapi_full_url)
    if request_output.ok:
        request_output_json = request_output.json()
        output.append(request_output_json["results"])
        while request_output_json["next"]:
            swapi_url = request_output_json["next"]
            request_output = requests.get(swapi_url)
            request_output_json = request_output.json()
            output.append(request_output_json["results"])
        output = [item for sublist in output for item in sublist]
    else:
        print("API Returned Not Ok")
        return (swapi_full_url, False)
    return (swapi_full_url, output)

