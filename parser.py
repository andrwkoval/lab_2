from collections import defaultdict


def read_data(path):
    """
    (str) -> (list)
    This function reads data and returns it in a list

    path: path of file to read data from
    returns: list of lists typo of [film, year, location]
    """

    with open(path, "r", encoding="latin1", errors="ignore") as f:
        for line in range(14):
            f.readline()

        return [line.strip().split("\t") for line in f]


def diction_create(lst, year):
    """
    (lst, int) -> (dict)
    This function converts list data to dictionary

    lst: list of lists with imbd data
    year: year to show films and locations
    returns: dictionary of data with locations as key
    and name of film and year as value
    """

    dict_all = defaultdict(set)
    for line in lst:
        if "(" + str(year) in line[0]:
            if "(" in line[-1]:
                dict_all[line[-2]].add(line[0])
            else:
                dict_all[line[-1]].add(line[0])

    return dict_all


def main(year, path):
    """
    (int, str) -> dict
    This function creates the final data dictionary

    year: year to find films
    path: path to the file to read data from
    returns: final data dictionary
    """

    data_lst = read_data(path)
    data_dict = diction_create(data_lst, year)
    return data_dict
