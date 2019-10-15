import string
import time

import count_schools
import states

COLS = ['SCHNAM05', 'LCITY05', 'LSTATE05']

STEMMINGS = {'ELEM':'ELEMENTARY', 'SCH':'SCHOOL', 'SCHOOLS':'SCHOOL', 'SCHL':'SCHOOL',
             'SR':'SENIOR', 'JR':'JUNIOR', 'N':'NORTH', 'S':'SOUTH', 'W':'WEST', 'E':'EAST',
             'SCI':'SCIENCE', 'SCIENCES':'SCIENCE', 'MT':'MOUNT', 'ST':'SAINT'}

STOP_WORDS = {'THE', 'AND', 'OF', 'AT'}

def getNormalizedData(path):
    '''
    :param path: String representing the path of the file containing the school info
    :return: Array consisting of dictionaries, each corresponding to a school listed in 'path'.
                Each dictionary contains:
                    - 'original': a human-readable string listing the schools name, city, and state
                    - 'normalized': the union of the normalized sets of the school's name, city, and state (normalized sets
                                    are returned by normalize()
    '''
    original_data = count_schools.getCityData(path)
    arr = []
    for i in original_data:
        new_arr = map(lambda x : i[x], COLS)
        new_dict = {'original':', '.join(new_arr), 'normalized':reduce(lambda x, y : x | y, map(normalize, new_arr))}
        arr.append(new_dict)
    return arr

def normalize(name):
    '''
    :param name: The string to normalize
    :return: A set consisting of unique words in 'name' after the following operations have been done on it:
                1) All punctuation marks have been removed
                2) All words occurring in STEMMINGS have been replaced with their corresponding values
                3) All proper state names have been converted to their abbreviations (i.e. California -> CA)
                4) All words occurring in STOP_WORDS (i.e. 'the', 'and') have been removed

    Example 1: "WINTERSET MIDDLE SCHOOL, WINTERSET, IA" -> set(['IA', 'MIDDLE', 'SCHOOL', 'WINTERSET'])
    Example 2: "TWIN CEDARS JR-SR HIGH SCHOOL, BUSSEY, IA" -> set(['HIGH', 'SCHOOL', 'CEDARS', 'IA', 'BUSSEY', 'SENIOR', 'TWIN', 'JUNIOR'])
    '''
    normalized_set = set()
    new_name = name.upper()
    for j in string.punctuation:
        new_name = new_name.replace(j, ' ')
    new_name = new_name.split()
    for i in new_name:
        if i in STEMMINGS:
            normalized_set.add(STEMMINGS[i])
        elif i in states.STATES_DICT:
            normalized_set.add(states.STATES_DICT[i])
        elif i not in STOP_WORDS:
            normalized_set.add(i)
    return normalized_set

# Here, the data is being read in from the CSV and normalized.
# Once that is all done, the time it took to read in and normalize the data is printed.
start = time.time()
normalized_data = getNormalizedData('school_data.csv')
print "Time taken to normalize data (in seconds):", time.time() - start

def getScore(test_set, ref_set):
    '''
    :param test_set: the normalized set (from normalize()) of the string that is being searched for
    :param ref_set: the normalized set (from normalize()) of the school that this string is being compared against
    :return: A float in [0.0, 1.0] representing the percentage of words in test_set are also in ref_set

    This function basically returns a percentage describing how closely the test_set resembles the ref_set
    '''
    return 1.0*len([i for i in test_set if i in ref_set])/len(ref_set)

def search(in_string):
    '''
    :param in_string: The search string, which will be passed into normalize() to get a normalized set
    :return: A list of tuples, each of which represents the following for a single school in global variable normalized_data:
                - A human-readable string, listing the school's name, city, and state
                - The score (from getScore()) of the normalized set derived from in_string compared to the normalized set for the school
    '''
    global normalized_data
    normalized_in_string = normalize(in_string)
    scores = map(lambda x : (x['original'], getScore(normalized_in_string, x['normalized'])), normalized_data)
    return map(lambda y : y[0], sorted(scores, key = lambda x : x[1], reverse=True))

def searchWithTime(in_string):
    '''
    :param in_string: The search string, which will be passed into normalize() to get a normalized set
    :return: A tuple containing (time to execute search(in_string) in seconds, results of search(in_string))
    '''
    start = time.time()
    results = search(in_string)
    duration = time.time()
    return duration, results

def printSearch(in_string, num_results=3):
    '''
    :param in_string: The search string, which will be passed into normalize() to get a normalized set
    :param num_results: The number of closest matches that should be printed (default 3)
    :return:

    This function calls searchWithTime(in_string) and prints out the top num_results closest matches in global variable
    normalized_data, along with the amount of time each search took
    '''
    start = time.time()
    results = search(in_string)
    time_taken = time.time() - start
    print "Results for '%s' (search took %f seconds)" % (in_string, time_taken)
    for i in enumerate(results[:num_results]):
        print '%d) %s' % (i[0] + 1, i[1])

if __name__ == '__main__':
    test_strings = ['monroe elementary school ia',
                    'monroe school',
                    'elementary school highland park',
                    'jefferson belleville',
                    'riverside school 44',
                    'granada charter school',
                    'foley high alabama',
                    'KUSKOKWIM']
    for i in test_strings:
        printSearch(i)