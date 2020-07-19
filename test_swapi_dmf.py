import pytest

from utils import swapi_get_wrapper


def test_smoke_test():
    assert 1 == 1


def test_swapi_endpoint_concat():
    url_test, _ = swapi_get_wrapper("dummy-test")
    assert url_test == "https://swapi.dev/api/dummy-test"


def test_swapi_people_endpoint_ok():
    _, output_test = swapi_get_wrapper("people")
    assert isinstance(output_test, list)
    assert "films" in output_test[0]
    assert "height" in output_test[0]


def test_swapi_species_endpoint_ok():
    _, output_test = swapi_get_wrapper("species")
    assert isinstance(output_test, list)
    assert "name" in output_test[0]

