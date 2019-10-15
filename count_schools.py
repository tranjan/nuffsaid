import csv

def getCityData(path):
    '''
    :param path: String representing the path of the file containing the school info
    :return: Array of dictionaries, mapping the column names to their respective values, for each school
    '''
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_num = 0
        data = []
        for row in csv_reader:
            if line_num == 0:
                headers = row
            else:
                data.append({i[0]: i[1] for i in zip(headers, row)})
            line_num += 1
    return data

def getCountsByKey(data, key):
    '''
    :param data: Array of dictionaries mapping column names to values (the return value of getCityData())
    :param key: Column name by which dictionaries must be grouped and counted (i.e. LSTATE05, LCITY05)
    :return: Dictionary mapping unique values of 'key' to number of dictionaries in 'data' for which 'key'
                maps to each unique value

    This function assumes that each dictionary in 'data' contains the key 'key'
    '''
    d = {}
    for i in data:
        if i[key] not in d:
            d[i[key]] = 0
        d[i[key]] += 1
    return d

def part1(data):
    '''
    :param data: Array of dictionaries mapping column names to values (the return value of getCityData())
    :return:

    This function answers all questions in Part 1 for the provided array 'data'
    '''
    key_dict = {'state':'LSTATE05', 'metro-centric locale':'MLOCALE', 'city':'LCITY05'}
    print "Part 1"
    print "Total schools:", len(data)
    for key in ['state', 'metro-centric locale']:
        print "Schools by %s:" % key
        counts_by_key = getCountsByKey(data, key_dict[key])
        for i in counts_by_key:
            print '- %s:' % i, counts_by_key[i]
    city_dict = getCountsByKey(data, key_dict['city'])
    most_schools = None
    for i in city_dict:
        if most_schools is None or city_dict[i] > most_schools:
            most_schools = city_dict[i]
    print "Cities that have the most schools:"
    for i in [c for c in city_dict if city_dict[c] == most_schools]:
        print "- %s: %d" % (i, city_dict[i])
    print "Unique cities with at least 1 school:", len(city_dict)


if __name__ == '__main__':
    part1(getCityData('school_data.csv'))