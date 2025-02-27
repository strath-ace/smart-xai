# ------------------Copyright (C) 2024 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# Connects to TypeDB and pushes the generated code from the LLM to execute and retrieve the results
# ===========================================================================================================

from __future__ import annotations
from typedb.driver import TypeDB, SessionType, TransactionType, TypeDBDriverException
import re
# from dataframe import df
# from  __builtin__ import any as b_any
import pandas as pd
import re


def data_extract(r_data1, r_data2):
    if 'Entity' in str(r_data1):
        r_data3 = str(r_data1.get_type())
        r_data4 = r_data3[:0] + r_data3[r_data3.find('[label: '):]
        r_data4 = r_data4.replace('[label: ', '')
        r_data4 = r_data4[:len(r_data4) - 1]
        # print(r_data4, "entity: " + str(r_data2))
        data_result = r_data4


    elif 'Relation' in str(r_data1):
        # print('True')
        # print(r_data1.get_type())
        r_data3 = str(r_data1.get_type())
        r_data4 = r_data3[:0] + r_data3[r_data3.find('[label: '):]
        r_data4 = r_data4.replace('[label: ', '')
        r_data4 = r_data4[:len(r_data4) - 1]
        # print(r_data4, "relation: " + str(r_data2))
        data_result = r_data4

    elif 'Attribute' in str(r_data1):

        r_data2 = r_data1.get_value()  # attribute.get_value()
        r_data3 = str(r_data1.get_type())  # attribute.get_type()
        r_data4 = r_data3[:0] + r_data3[r_data3.find('[label: '):]
        r_data4 = r_data4.replace('[label: ', '')
        r_data4 = r_data4[:len(r_data4) - 1]
        # print(r_data4, "data: " + str(r_data2))
        data_result = r_data2

    return data_result, r_data4


def TypeDB_executor(request):
    text = request

    # Remove all text before the 'match' character
    request = text[text.rfind("match"):]

    # Remove all text after the 'get' character to only extract the data with the query
    request = request[:request.rfind("get")]

    # Remove all text before the 'get' character to separate the get statement from the input
    data = text[text.rfind("get"):]

    # Remove all text after the last ';' character
    data = data[:data.rfind(";") + 1]
    print('data: ', data)

    data2 = (data.replace(";", "").replace('$', '').replace('get', '').replace(' ', ''))
    # print(data2)
    data2 = data2.split(',')

    print(data2)
    # remove sort from the get list
    limit_number = 0
    if 'limit' in data:
        # data = str(data)
        print(limit_number)
        limit_number =  re.findall(r'\d+', data)
        print(limit_number)
        limit_number = int(limit_number[0])
    if any('sort' in x for x in data2) or any('limit' in x for x in data2)  :
        data2 = data2[:-1]
    else:
        data2 = data2
    print(data2)
    heading_list = []
    data_list = []
    another_heading_list = []
    heading = []
    try:
        with TypeDB.core_driver("localhost:1729") as driver:
            with driver.session("sched_final", SessionType.DATA) as session:

                ## Read the data using a READ only transaction
                with session.transaction(TransactionType.READ) as read_transaction:
                    if "count" in data:
                        result = read_transaction.query.get_aggregate(request + data)
                        result = result.resolve().as_value().as_long()
                        heading = ["Total"]
                        data_list.append([result])

                    else:
                        answer_iterator = read_transaction.query.get(request + data)
                        nested = []
                        i = 0
                        for answer in answer_iterator:
                            # print('rerun')
                            # data_list.append(nested)

                            # print(answer.get("n").as_attribute().get_value())
                            # if i <= 5:
                                for sub_data in data2:
                                    r_data2 = 0

                                    r_data1 = answer.get(str(sub_data))
                                    # print(r_data1.get_type())
                                    # print(r_data1)
                                    data_result, r_data4 = data_extract(r_data1, r_data2)
                                    # Create a nested list for googlesheet generation, each nested list is a new row, in googlesheet
                                    # nested.append(str(data_result))
                                    # print('loop')

                                    # Used to record a new list after every 6 reps
                                    if r_data4 not in heading_list:
                                        print('heading_doesnt_exist')
                                        heading_list.append(r_data4)
                                        nested.append(str(data_result))

                                    # If a new heading is present due to different action name, create a new heading, to add as a new row (a new table)
                                    if r_data4 not in heading and heading != []:
                                        heading_list.append(r_data4)
                                        print(r_data4, heading)
                                        another_heading_list = heading_list
                                        nested.append(str(data_result))
                                print('nested', heading_list, nested)
                                i = i + 1
                                print('loop', i)
                                # if i == 6:
                                # print('loop exceeded', i)
                                if another_heading_list == []:
                                    heading = heading_list
                                    data_list.append(nested)
                                else:
                                    data_list.append(another_heading_list)
                                    data_list.append(nested)
                                # nested_new = nested

                                nested = []
                                heading_list = []
                                another_heading_list = []
                                i = 0

        print('exited')
        if limit_number < 6 and limit_number > 0:
            print(i)
            heading = heading_list
            data_list.append(nested)
        data_list.insert(0, heading)
        print(data_list)

        return data_list

    except TypeDBDriverException as e:
        # Retrieve and print error feedback
        print('123456789')
        print(f"TypeDB Error: {e}")
        return e

# Test algorithm
if __name__ == "__main__":
    Response = ('''""match
    $st >= 2020-12-03T18:03:21; # Start time queried
    $st <= 2020-12-03T18:03:26; # End time queried
    $a isa action, has name $n, has a_timestamp $at;
    $ret isa $ret-type;
    {$n contains 'processed'; $x isa processed, has $ret;} or
    {$n contains 'image'; $x isa image, has $ret;} or
    {$n contains 'downlink'; $x isa downlinked, has $ret;};
    $pt($x,$mem) isa contents;
    $g isa ground_station, has access $ac, has $id;
    $env isa environment, has land_visibility $lv, has daylight $d, has latitude $lat,
    has longitude $lon; $sat isa satellite;
    $mem isa memory_unit, has current_capacity $cc, has $id, has max_capacity $max;
    $t($a,$sat) isa schedule;
    $l($mem,$sat) isa installation;
    $sa($g,$env) isa station_access;
    $loc($sat,$env) isa localisation, has start $st, has end $en;
    get $n, $at, $ret, $pt, $ac, $lv, $d, $lat, $lon, $l, $sa, $t, $loc, $id, $mem, $g, $cc, $st, $en;""''')
    word = 'Error'
    found = False
    datalist ='Error'
    while word in str(datalist) or 'error' in str(datalist) or datalist == [[]]:
    # while found != True:

        datalist = TypeDB_executor(Response)

    if word in str(datalist) or 'error' in str(datalist):
        print('false')
        found = False
    else:
        print('true')
        print([datalist])
        found = True
    # else:
    #     Response = ('''match
    # $st = 2020-12-03T00:23:26; # Time queried
    # $a isa action, has name $n, has a_timestamp $at;
    # $ret isa $ret-type;
    # {$n contains 'processed'; $x isa processed, has $ret;} or
    # {$n contains 'image'; $x isa image, has $ret;} or
    # {$n contains 'idle'; $x isa idle, has $ret;} or
    # {$n contains 'downlink'; $x isa downlinked, has $ret;};
    # $pt($x,$mem) isa contents;
    # $g isa ground_station, has access $ac, has $id;
    # $env isa environment, has land_visibility $lv, has daylight $d, has latitude $lat,
    # has longitude $lon; $sat isa satellite;
    # $mem isa memory_unit, has current_capacity $cc, has $id, has max_capacity $max;
    # $t($a,$sat) isa schedule;
    # $l($mem,$sat) isa installation;
    # $sa($g,$env) isa station_access;
    # $loc($sat,$env) isa localisation, has start $st, has end $en;
    # get $n, $at, $ret, $pt, $ac, $lv, $d, $lat, $lon, $l, $sa, $t, $loc, $id, $mem, $g, $cc, $st, $en;''')
    #     datalist = TypeDB_executor(Response)
        # found = True
    # print(datalist)

    #     ('''match
    # $st >= 2020-12-03T00:52:51; # Start time queried
    # $st <= 2020-12-03T00:53:16; # End time queried
    # $a isa action, has name $n, has a_timestamp $at;
    # $ret isa $ret-type;
    # {$n contains 'processed'; $x isa processed, has $ret;} or
    # {$n contains 'image'; $x isa image, has $ret;} or
    # {$n contains 'downlink'; $x isa downlinked, has $ret;};
    # $pt($x,$mem) isa contents;
    # $g isa ground_station, has access $ac, has $id;
    # $env isa environment, has land_visibility $lv, has daylight $d, has latitude $lat,
    # has longitude $lon; $sat isa satellite;
    # $mem isa memory_unit, has current_capacity $cc, has $id, has max_capacity $max;
    # $t($a,$sat) isa schedule;
    # $l($mem,$sat) isa installation;
    # $sa($g,$env) isa station_access;
    # $loc($sat,$env) isa localisation, has start $st, has end $en;
    # get $n, $at, $ret, $pt, $ac, $lv, $d, $lat, $lon, $l, $sa, $t, $loc, $id, $mem, $g, $cc, $st, $en;''')




        # "match "
        #         "    $st >= 2020-12-03T00:44:16;"
        #         "    $st <= 2020-12-03T00:44:26;"
        #         "    $a isa action, has name $n, has a_timestamp $at;"
        #         "    $ret isa $ret-type;"
        #         "    {$n contains 'processed'; $x isa processed, has $ret;} or"
        #         "    {$n contains 'image'; $x isa image, has $ret;} or"
        #         "    {$n contains 'downlink'; $x isa downlinked, has $ret;};"
        #         "    $pt($x,$mem) isa contents;"
        #         "    $g isa ground_station, has access $ac, has $id;"
        #         "    $env isa environment, has land_visibility $lv, has daylight $d, has latitude $lat,"
        #         "    has longitude $lon; $sat isa satellite;"
        #         "    $mem isa memory_unit, has current_capacity $cc, has $id, has max_capacity $max;"
        #         "    $t($a,$sat) isa schedule;"
        #         "    $l($mem,$sat) isa installation;"
        #         "    $sa($g,$env) isa station_access;"
        #         "    $loc($sat,$env) isa localisation, has start $st, has end $en;"
        #         "    get $n, $at, $ret, $pt, $ac, $lv, $d, $lat, $lon, $l,  $sa, $t, $loc, $id, $cc, $max, $st, $en;")

    # Response = open("Type_DB_Code_file.txt", "r")
    # Response = Response.read()

