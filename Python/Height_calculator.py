import numpy as np
import sqlite3
from itertools import product


def get_height(hMin, hMax):
    # connect to the database
    conn = sqlite3.connect('BIM_Craneplanner_DB.db')

    # Queries to get everything that is needed from the database
    cur = conn.cursor()
    cur_id = conn.cursor()
    cur_tw = conn.cursor()
    # Get the IDs and the height
    cur.execute("SELECT height FROM Tower_Elements WHERE height IS NOT NULL")
    cur_id.execute("SELECT id FROM Tower_Elements WHERE height IS NOT NULL")
    cur_tw.execute("SELECT id, TowerElementIndex FROM Tower_Elements WHERE height IS NOT NULL")

    rows = cur.fetchall()
    row_id = cur_id.fetchall()
    row_tw = cur_tw.fetchall()

    arr = []
    arr_id = []
    arr_tw = []

    # put evertyhing that is fetched into arrays and if necessary format them correctly
    for row in rows:
        arr.append(row)
    arr = [i[0] for i in arr]

    for row in row_id:
        arr_id.append(row)
    arr_id = [i[0] for i in arr_id]

    for row in row_tw:
        arr_tw.append(row)

    # combine the array for heights and the one for ids together
    def combine_to_arr(height_array, id_array):

        res = []
        for x in range(0, len(height_array)):
            res = [[i] for i in arr_id]
            for y in range(0, len(res)):
                res[y].append(height_array[y])

        return res

    # convert to numoy array
    arr_1 = np.array(combine_to_arr(arr, arr_id))

    # remove all subarrays which sum is less than the desired height
    def rem(arr):
        res = []
        for x in arr:
            z = sum(x)
            if hMax > z > hMin:
                res.append(x)
        return np.asarray(res)

    # trying to go over id's but they change. Currently not working
    def get_ID(height_array):
        res = []
        for x in range(0, len(arr)):
            res = [[i] for i in arr_id]
            for y in range(0, len(res)):
                res[y].append(id(arr[y]))
        return res

    # getting the IDs to the heights. Not working with to different tower elements of the same height
    def get_ID_new(height_array, id_array):

        res = []
        for x in range(0, len(height_array)):
            res = [[i] for i in arr_id]
            for y in range(0, len(res)):
                res[y].append(height_array[y])

        return res

    for_ids = get_ID_new(arr, arr_id)

    # create permutations
    def all_repeat(arr, num):
        perm = list(arr)
        results = []
        for c in product(perm, repeat=num):
            results.append(c)
            np.asarray(results)
        return results

    # get all permutations till a certain length
    def get_perm(array):
        res = []
        for x in range(1, 4):
            res.append(rem(all_repeat(array, x)))
            resu = np.asarray(res)
        return resu

    # get only the possible combinations
    comb = get_perm(arr)[2]

    # remove all duplicates from the array
    # [1,2,3] is the same as [2,1,3]
    def remove_dups(array):
        res = []
        for x in array:
            res = (np.sort(array))
            res = np.unique(res, axis=0)
        return res

    for_tests = remove_dups(comb)

    # finds the corresponding tower element to the combinations
    def find_tw(array_perm, array_id, array_elements):
        test1 = []
        test = []
        for x in array_perm:
            for y in x:
                for z, yz in zip(array_id, array_elements):
                    if y in z:
                        # print("Y: ", y, "Z: ",z)
                        test.append(yz[1])
            test1.append(test)
            test = []
        return test1

    return print(find_tw(for_tests, for_ids, arr_tw))


#get_height(32, 35)