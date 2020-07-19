# standard library
from pathlib import Path


# local files
from utils import swapi_get_wrapper

# install required
import pandas as pd
import requests


"""
Make request to StarWars API, retrieve top 10 
    characters based on most appearances in film, 
    order the 10 by height descending, produce CSV, 
    and POST CSV to httpbin
"""
# make API calls
people_endpoint, people = swapi_get_wrapper("people")
species_endpoint, species = swapi_get_wrapper("species")

# check successful return
if not people or not species:
    raise Exception("StarWars API returned a bad status code")
else:
    # create an attr for appearances
    for person in people:
        person["appearances"] = len(person["films"])

    # sort by appearances desc
    people_by_most_films = sorted(people, key=lambda x: x["appearances"], reverse=True)

    # create a DF, order by height desc
    df_people = pd.DataFrame(people_by_most_films[:10])
    df_people = df_people.astype({"height": int})
    df_people = df_people.explode("species")
    df_people.sort_values(by=["height"], inplace=True, ascending=False)

    # create a dataframe for species
    df_species = pd.DataFrame(species)

    # join the dataframes to replace the species URL with name
    df_people_species = df_people.join(
        df_species.set_index("url"), on="species", rsuffix="_species"
    )

    # make a smaller DF for outputting to CSV
    output_df = pd.DataFrame(
        df_people_species[["name", "name_species", "height", "appearances"]]
    )

    # rename to clean up the output
    output_df.rename(columns={"name_species": "species"}, inplace=True)

    # output the file and upload
    file_location = str(Path.home())

    output_df.to_csv(
        file_location + "/dmf-output.csv",
        sep=",",
        columns=["name", "species", "height", "appearances"],
        index=False,
    )
    httpbin_url = "https://httpbin.org/post"
    csv_file = {"dmf_swapi_csv": open(file_location + "/dmf-output.csv", "rb")}

    csv_post = requests.post(url=httpbin_url, files=csv_file)

    # print httpbin status and output
    print(csv_post)
    print(csv_post.text)
