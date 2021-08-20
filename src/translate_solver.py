"""

"""


def translate_solver(var_names_index, var_values, cycles, itineraries, commodities):
    """ """
    import collections as col

    commodities_1 = commodities
    output = dict()
    output_temp = dict()
    var_keys = list(var_values.keys())

    for ivar in set(var_names_index.keys()):

        var_keys_aux = [key for key in var_keys if ivar in key]

        for i in range(0, len(var_keys_aux)):

            position = list()
            k = var_keys_aux[i][len(ivar) : len(var_keys_aux[i])].count("_")

            if k == var_names_index[ivar][0]:

                for p in range(0, k):
                    position.append(
                        [
                            j
                            for j, x in enumerate(
                                var_keys_aux[i][len(ivar) : len(var_keys_aux[i])]
                            )
                            if x == "_"
                        ][p]
                        + 1
                    )

                if k > 1:
                    index = [None] * (len(position))
                    j = 0
                    if var_names_index[ivar][1] == "integer":
                        index[j] = int(
                            var_keys_aux[i][len(ivar) : len(var_keys_aux[i])][
                                (position[j] + 1) : (position[j + 1] - 2)
                            ]
                        )
                    elif var_names_index[ivar][1] == "float":
                        index[j] = float(
                            var_keys_aux[i][len(ivar) : len(var_keys_aux[i])][
                                (position[j] + 1) : (position[j + 1] - 2)
                            ]
                        )
                    elif var_names_index[ivar][1] == "string":
                        index[j] = var_keys_aux[i][len(ivar) : len(var_keys_aux[i])][
                            (position[j] + 2) : (position[j + 1] - 3)
                        ]

                    for j in range(1, len(position) - 1):
                        if var_names_index[ivar][j + 1] == "integer":
                            index[j] = int(
                                var_keys_aux[i][len(ivar) : len(var_keys_aux[i])][
                                    (position[j] + 1) : (position[j + 1] - 3)
                                ]
                            )
                        elif var_names_index[ivar][j + 1] == "float":
                            index[j] = float(
                                var_keys_aux[i][len(ivar) : len(var_keys_aux[i])][
                                    (position[j] + 1) : (position[j + 1] - 3)
                                ]
                            )
                        elif var_names_index[ivar][j + 1] == "string":
                            index[j] = var_keys_aux[i][
                                len(ivar) : len(var_keys_aux[i])
                            ][(position[j] + 1) : (position[j + 1] - 3)]

                    j = len(position) - 1
                    if var_names_index[ivar][j + 1] == "integer":
                        index[j] = int(
                            var_keys_aux[i][len(ivar) : len(var_keys_aux[i])][
                                (position[-1]) : (
                                    len(
                                        var_keys_aux[i][
                                            len(ivar) : len(var_keys_aux[i])
                                        ]
                                    )
                                    - 1
                                )
                            ]
                        )
                    elif var_names_index[ivar][j + 1] == "float":
                        index[j] = float(
                            var_keys_aux[i][len(ivar) : len(var_keys_aux[i])][
                                (position[-1]) : (
                                    len(
                                        var_keys_aux[i][
                                            len(ivar) : len(var_keys_aux[i])
                                        ]
                                    )
                                    - 1
                                )
                            ]
                        )
                    elif var_names_index[ivar][j + 1] == "string":
                        index[j] = var_keys_aux[i][len(ivar) : len(var_keys_aux[i])][
                            (position[-1] + 1) : (
                                len(var_keys_aux[i][len(ivar) : len(var_keys_aux[i])])
                                - 1
                            )
                        ]

                    output_temp[tuple(index)] = (
                        var_names_index[ivar][j + 2] * var_values[var_keys_aux[i]]
                    )
                elif k == 1:
                    if var_names_index[ivar][1] == "integer":
                        index = int(
                            var_keys_aux[i][(len(ivar) + 1) : len(var_keys_aux[i])]
                        )
                        output_temp[index] = var_values[var_keys_aux[i]]
                    elif var_names_index[ivar][1] == "float":
                        index = float(
                            var_keys_aux[i][(len(ivar) + 1) : len(var_keys_aux[i])]
                        )
                        output_temp[index] = var_values[var_keys_aux[i]]
                    elif var_names_index[ivar][1] == "string":
                        index = var_keys_aux[i][(len(ivar) + 1) : len(var_keys_aux[i])]

                    output_temp[index] = (
                        var_names_index[ivar][-1] * var_values[var_keys_aux[i]]
                    )
                elif k == 0:
                    output_temp[var_keys_aux[i]] = (
                        var_names_index[ivar][-1] * var_values[var_keys_aux[i]]
                    )
            else:
                output_temp[var_keys_aux[i]] = "key error"
        output[ivar] = col.OrderedDict(sorted(output_temp.items()))
        output_temp = {}

    clear_data = dict()
    not_binary = dict()

    # Objective function
    key = "v_objective_function"
    clear_data[key] = dict()
    clear_data[key] = [output[key]]

    key = "v_number_vehicles"
    clear_data[key] = dict()
    clear_data[key] = [output[key]]

    # Vehicles
    key = "Vehicles_Cycle"
    clear_data[key] = dict()
    index = list()
    value = list()

    for ikey in sorted(set(output[key])):
        if output[key][ikey] > 0:
            index.append(cycles[int(ikey - 1)].name)
            value.append(output[key][ikey])

    clear_data[key]["cycle"] = index
    clear_data[key]["vehicles"] = value

    # Flow
    # key = 'Flow_Itinerary'
    # clear_data[key] = dict()
    # commodity = list()
    # itinerary = list()
    # value = list()
    #
    # for ikey in sorted(set(output[key])):
    #     if output[key][ikey] > 0:
    #         index.append(itineraries[int(ikey-1)].name)
    #         value.append(output[key][ikey])
    #
    # clear_data[key]['itinerary'] = index
    # clear_data[key]['flow'] = value

    return clear_data
