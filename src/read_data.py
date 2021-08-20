"""

"""

import pandas as pd
import json


def read_data(vehicles_path, points_path, demand_path):
    """
    Function to read all the data

    Arguments
    ---------
    vehicles_path : string
        Path to the vehicle data file
    points_path : string
        Path to the points data file
    demand_path : string
        Path to the demand data file

    Returns
    -------
        A tuple with the list of dictionaries for each data item.
    """

    with open(points_path) as f:
        points = json.load(f)

    vehicles = pd.read_csv(vehicles_path, sep="\t")
    # points = pd.read_csv(points_path, sep="\t")
    demand = pd.read_csv(demand_path, sep="\t")

    return vehicles, points, demand


def process_demand(demand_data):
    """
    Function to process the demand

    Arguments
    ---------
    demand_data : dataframe
        Dataframe with the demand data.

    Returns
    -------
        A tuple with three dictionaries, one with demand dictionaries, another with times and another with distances.
    """
    demand = demand_data[["originCode", "destinationCode", "parcels"]]
    demand = demand[(demand.parcels > 0)]
    demand_dict = (
        demand.groupby("originCode")
        .apply(lambda x: dict(zip(x["destinationCode"], x["parcels"])))
        .to_dict()
    )
    demand_dict_aux = (
        demand.groupby("destinationCode")
        .apply(lambda x: dict(zip(x["originCode"], x["parcels"])))
        .to_dict()
    )

    demand_parcels_for = dict()
    demand_parcels_from = dict()

    for i in demand_dict:
        laux = list()

        for j in demand_dict[i]:
            if demand_dict[i][j] > 0:
                laux.append(j)

        demand_parcels_for[i] = laux

    for i in demand_dict_aux:
        laux = list()

        for j in demand_dict_aux[i]:
            if demand_dict_aux[i][j] > 0:
                laux.append(j)

        demand_parcels_from[i] = laux

    demand_origin = demand_data.groupby("originCode", as_index=False).agg(
        {"parcels": "sum"}
    )

    demand_origin_dict = dict(zip(demand_origin.originCode, demand_origin.parcels))

    demand_destination = demand_data.groupby("destinationCode", as_index=False).agg(
        {"parcels": "sum"}
    )

    demand_destination_dict = dict(
        zip(demand_destination.destinationCode, demand_destination.parcels)
    )

    demand_dicts = dict()
    demand_dicts["dataframeFull"] = demand
    demand_dicts["baseDict"] = demand_dict
    demand_dicts["originDict"] = demand_origin_dict
    demand_dicts["destinationDict"] = demand_destination_dict
    demand_dicts["forDict"] = demand_parcels_for
    demand_dicts["fromDict"] = demand_parcels_from

    times = demand_data[["originCode", "destinationCode", "Hours"]]
    times_dict = (
        times.groupby("originCode")
        .apply(lambda x: dict(zip(x["destinationCode"], x["Hours"])))
        .to_dict()
    )

    distance = demand_data[["originCode", "destinationCode", "Kilometers"]]
    distance_dict = (
        distance.groupby("originCode")
        .apply(lambda x: dict(zip(x["destinationCode"], x["Kilometers"])))
        .to_dict()
    )

    return demand_dicts, times_dict, distance_dict


def process_points(points_data):
    """
    Function to process the points data

    Arguments
    ---------
    points_data : dataframe
        A data frame containing the data read from the points.

    Returns
    -------
        A dictionary with the data.
    """
    points_names = points_data[["code", "point"]]
    points_names_dict = dict(zip(points_names.code, points_names.point))

    return points_names_dict


def read_all_data():
    """
    Not implemented function.
    """
    return 0
