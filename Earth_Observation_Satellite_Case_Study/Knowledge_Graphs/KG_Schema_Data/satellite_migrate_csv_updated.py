# Original  Copyright (C) 2022 Vaticle
# Original modified -  October 2023
#-----------Modification - Copyright (C) 2024 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# This function is used to populate the schema for the satellite scheduling problem
# Example codes may be found https://github.com/typedb/typedb-driver/tree/3.0/python
# Tutorial may be found here - https://typedb.com/docs/drivers/python/#_quickstart
# ===========================================================================================================

import csv
from typedb.driver import TypeDB, SessionType, TransactionType
import time

def satellite_graph(inputs, data_path, database_name):
    """
      gets the job done:
      1. creates a TypeDB instance
      2. creates a session to the targeted database
      3. for each input:
        - a. constructs the full path to the data file
        - b. loads csv to TypeDB
      :param input as list of dictionaties: each dictionary contains details required to parse the data
    """
    with TypeDB.core_driver("localhost:1729") as driver:
        with driver.session(database_name, SessionType.DATA) as session:

            for input in inputs:
                input["file"] = input["file"].replace(data_path, "")  # for testing purposes
                input["file"] = data_path + input["file"]  # 3a
                print("Loading from [" + input["file"] + ".csv] into TypeDB ...")
                migrate_data_into_typedb(input, session)  # 3b


def migrate_data_into_typedb(input, session):
    # Loads the scheduled data into the typedb database in the form of dictionary lists
    # An insert query is executed for each dictionary followed by a commit
    # Each entity is in the form of a full insert statement with all the respected attributes

    items = parse_data_to_dictionaries(input)  # 1
    print(items[2])
    for item in (items): # (items[3457,0],items[3]):  # 2 For altering the data size migrated
        list = [input["template"](item)]

        for i in range(len(list[0])):
            with session.transaction(TransactionType.WRITE) as transaction:  # a
                print("Executing TypeQL Query: \n" + list[0][i])
                transaction.query.insert(list[0][i])  # c
                transaction.commit()  # d

    print("\nInserted " + str(len(items)) +
          " items from [ " + input["file"] + ".csv] into TypeDB.\n")


# This calls all the satellite data from the csv by each row to load into typedb
def satellite_template(Satellite_data):
    year = '2020-'
    month = '12-'
    day = '03T'
    print(Satellite_data["start_time"])
    st = time.strftime("%H:%M:%S", time.gmtime(int(Satellite_data["start_time"])))
    et = time.strftime("%H:%M:%S", time.gmtime(int(Satellite_data["end_time"])))
    print(st, et)
    # st = timedelta(seconds=int(Satellite_data["start_time"]))
    # et = timedelta(seconds=int(Satellite_data["end_time"]))
    start_time = year+month+day+str(st)
    end_time = year+month+day+str(et)
    # print(start_time, end_time)

    im_size = 2688
    pr_size = 250
    dl_size = 560
    #  # ---------------environment-------------------------------
    graql_insert_query = 'insert $env isa environment' + ''
    graql_insert_query += ', has latitude "' + Satellite_data["latitude"] + '"'
    graql_insert_query += ', has longitude "' + Satellite_data["longitude"] + '"'

    if Satellite_data["land_access"] == '0':
        land_vis = 'false'
    else:
        land_vis = 'true'
    graql_insert_query += ', has land_visibility ' + land_vis + ''

    if Satellite_data["day_access"] == '0':
        day_vis = 'false'
    else:
        day_vis = 'true'
    graql_insert_query += ', has daylight ' + day_vis + '; \n'

    # ---------------action -------------------------------
    graql_insert_query1 = 'insert $a isa action'
    # graql_insert_query1 += ', has action "' + Satellite_data["extracted_action"] + '"'
    if Satellite_data["extracted_action"] == '0' and Satellite_data["action_possible"] == "YES":
        # print('work1')
        action_scheduled = '"image"'
        mem_req = im_size

    elif Satellite_data["extracted_action"] == '1' and Satellite_data["action_possible"] == "YES":
        # print('work2')
        action_scheduled = '"processed"'
        mem_req = pr_size

        # graql_insert_query1 += ', has action-scheduled "Processing" '
        # graql_insert_query1 += ', has number-of-executions ' + str(Satellite_data["total_processed_images"]) + '; \n'
    elif Satellite_data["extracted_action"] == '2' and Satellite_data["action_possible"] == "YES":
        action_scheduled = '"downlinked"'
        mem_req = dl_size
    else:
        print(Satellite_data["extracted_action"], Satellite_data["action_possible"], 'didnt work')
        action_scheduled = '"Idle"'
        mem_req = 0

    graql_insert_query1 += ', has name ' + action_scheduled
    graql_insert_query1 += ', has a_timestamp ' + start_time + ''
    graql_insert_query1 += ', has memory_requirement ' + str(mem_req) + '; \n'

    # ---------------ground station -------------------------------
    graql_insert_query2 = 'insert $gs isa ground_station'
    graql_insert_query2 += ', has id ' + str(Satellite_data["n"])
    graql_insert_query2 += ', has latitude "' + Satellite_data["latitude"] + '"'
    graql_insert_query2 += ', has longitude "' + Satellite_data["longitude"] + '"'
    if Satellite_data["station_access"] == '0':
        station_access = 'false'
    else:
        station_access = 'true'
    graql_insert_query2 += ', has access ' + station_access + ';\n'

    # ---------------memory unit-------------------------------
    graql_insert_query3 = 'insert $m isa memory_unit, has current_capacity ' + str(Satellite_data["memory_used"]) + ''
    graql_insert_query3 += ', has id ' + str(Satellite_data["n"]) + ''
    graql_insert_query3 += ', has max_capacity ' + str(Satellite_data["maximum_memory"]) + '; \n'

    # ---------------image-------------------------------
    graql_insert_query4 = 'insert $im isa image '
    graql_insert_query4 += ', has im_in_memory ' + str(Satellite_data["pics_in_memory"]) + ''
    graql_insert_query4 += ', has im_total_taken ' + str(Satellite_data["total_pics_count"]) + ''

    # added
    graql_insert_query4 += ', has pr_in_memory ' + str(Satellite_data["processed_images_in_memory"]) + ''
    graql_insert_query4 += ', has total_processed ' + str(Satellite_data["total_processed_images"]) + ''
    graql_insert_query4 += ', has total_sent ' + str(Satellite_data["total_downlinked_images"]) + ''
    # if Satellite_data["extracted_action"] == '0' and Satellite_data["action_possible"] == "YES":
    #     graql_insert_query4 += ', has im_timestamp ' + start_time + ''
    graql_insert_query4 += ', has im_size ' + str(im_size) + ';\n'

    # ---------------processed-------------------------------
    graql_insert_query5 = 'insert $p isa processed '
    graql_insert_query5 += ', has pr_in_memory ' + str(Satellite_data["processed_images_in_memory"]) + ''
    graql_insert_query5 += ', has total_processed ' + str(Satellite_data["total_processed_images"]) + ''

    # added below
    graql_insert_query5 += ', has im_in_memory ' + str(Satellite_data["pics_in_memory"]) + ''
    graql_insert_query5 += ', has im_total_taken ' + str(Satellite_data["total_pics_count"]) + ''
    graql_insert_query5 += ', has total_sent ' + str(Satellite_data["total_downlinked_images"]) + ''
    # if Satellite_data["extracted_action"] == '1' and Satellite_data["action_possible"] == "YES":
    #     graql_insert_query5 += ', has pr_timestamp ' + start_time + ''
    graql_insert_query5 += ', has pr_size ' + str(pr_size) + ';\n'

    # ---------------downlinked-------------------------------
    graql_insert_query6 = 'insert $d isa downlinked '
    graql_insert_query6 += ', has total_sent ' + str(Satellite_data["total_downlinked_images"]) + ''

    #added below
    graql_insert_query6 += ', has im_in_memory ' + str(Satellite_data["pics_in_memory"]) + ''
    graql_insert_query6 += ', has im_total_taken ' + str(Satellite_data["total_pics_count"]) + ''
    graql_insert_query6 += ', has pr_in_memory ' + str(Satellite_data["processed_images_in_memory"]) + ''
    graql_insert_query6 += ', has total_processed ' + str(Satellite_data["total_processed_images"]) + ''
    # if Satellite_data["extracted_action"] == '2' and Satellite_data["action_possible"] == "YES":
    #     graql_insert_query6 += ', has dl_timestamp ' + start_time + ''
    graql_insert_query6 += ', has dl_size ' + str(dl_size) + ';\n'

    # ---------------idle-------------------------------
    graql_insert_query7 = 'insert $idl isa idle '

    #added below
    graql_insert_query7 += ', has im_in_memory ' + str(Satellite_data["pics_in_memory"]) + ''
    graql_insert_query7 += ', has im_total_taken ' + str(Satellite_data["total_pics_count"]) + ''
    graql_insert_query7 += ', has pr_in_memory ' + str(Satellite_data["processed_images_in_memory"]) + ''
    graql_insert_query7 += ', has total_processed ' + str(Satellite_data["total_processed_images"]) + ''
    graql_insert_query7 += ', has total_sent ' + str(Satellite_data["total_downlinked_images"]) + ''
    # if  Satellite_data["action_possible"] == "NO":
    #     graql_insert_query6 += ', has idl_timestamp ' + start_time + ''
    graql_insert_query7 += ', has total_idle ' + str(Satellite_data["total_idle_instances"]) + ';\n'

    # ---------------satellite-------------------------------
    graql_insert_query8 = 'insert $sat isa satellite '
    graql_insert_query8 += ', has id ' + str(Satellite_data["n"]) + ';\n'


    # print(graql_insert_query)
    # ---------------groups/relations----------------------------------------------------------------------
    # ---------------contents-------------------------------
    graql_insert_query9 = 'match $m isa memory_unit, has current_capacity ' + str(Satellite_data["memory_used"]) + ';'
    graql_insert_query9 += '$im isa image, has im_in_memory ' + str(Satellite_data["pics_in_memory"]) + ';'
    graql_insert_query9 += '$p isa processed, has pr_in_memory ' + str(Satellite_data["processed_images_in_memory"]) + ';'
    graql_insert_query9 += '$d isa downlinked, has total_sent ' + str(Satellite_data["total_downlinked_images"]) + ';'
    graql_insert_query9 += '$idl isa idle, has total_idle ' + str(Satellite_data["total_idle_instances"]) + ';'
    if action_scheduled == '"image"':
        graql_insert_query9 += 'insert $con(contained:$im, container:$m) isa contents; \n'
    elif action_scheduled == '"processed"':
        print('proc')
        graql_insert_query9 += 'insert $con(contained:$p, container:$m) isa contents; \n'
    elif action_scheduled == '"downlinked"':
        graql_insert_query9 += 'insert $con(contained:$d, container:$m) isa contents; \n'
    else:
        graql_insert_query9 += 'insert $con(contained:$idl, container:$m) isa contents; \n'
    # graql_insert_query9 += 'insert $con(contained:$p, contained:$im, contained:$d, contained:$idl, container:$m) isa contents; \n'

    # ---------------station access-------------------------------
    graql_insert_query10 = 'match $gs isa ground_station, has id ' + str(Satellite_data["n"]) + ';'
    graql_insert_query10 += '$env isa environment, has land_visibility ' + land_vis + ';'
    graql_insert_query10 += 'insert $sa(station:$gs, environment:$env) isa station_access; \n'

    # ---------------localisation-------------------------------
    graql_insert_query11 = 'match $env isa environment, has latitude "' + Satellite_data["latitude"] + '";' #has longitude "' + Satellite_data["longitude"] + '";'
    graql_insert_query11 += '$sat isa satellite, has id ' + str(Satellite_data["n"]) + ';'
    graql_insert_query11 += 'insert $l(environment:$env, satellite:$sat) isa localisation, has start ' + start_time +', has end ' + end_time + '; \n'

    # ---------------installation-------------------------------
    graql_insert_query12 = 'match $sat isa satellite, has id ' + str(Satellite_data["n"]) + ';'
    graql_insert_query12 += '$m isa memory_unit, has current_capacity ' + str(Satellite_data["memory_used"]) + ';'
    graql_insert_query12 += 'insert $ins(satellite:$sat, installed:$m) isa installation; \n'

    # ---------------schedule-------------------------------
    # graql_insert_query13 = 'match $a isa action, has name ' + action_scheduled + ';'
    graql_insert_query13 = 'match $a isa action, has a_timestamp ' + start_time + ';'
    graql_insert_query13 += '$sat isa satellite, has id ' + str(Satellite_data["n"]) + ';'
    # graql_insert_query13 += '$im isa image, has im_in_memory ' + str(Satellite_data["pics_in_memory"]) + ';'
    # graql_insert_query13 += '$p isa processed, has pr_in_memory ' + str(Satellite_data["processed_images_in_memory"]) + ';'
    # graql_insert_query13 += '$d isa downlinked, has total_sent ' + str(Satellite_data["total_downlinked_images"]) + ';'
    # graql_insert_query13 += '$id isa idle, has total_idle ' + str(Satellite_data["total_idle_instances"]) + ';'
    graql_insert_query13 += 'insert $sch(satellite:$sat,scheduled_action:$a) isa schedule, has start ' + start_time + ', has end ' + end_time + '; \n'

    return (graql_insert_query, graql_insert_query1, graql_insert_query2, graql_insert_query3, graql_insert_query4,
            graql_insert_query5, graql_insert_query6, graql_insert_query7, graql_insert_query8, graql_insert_query9,
            graql_insert_query10, graql_insert_query11, graql_insert_query12, graql_insert_query13)
    #

def parse_data_to_dictionaries(input):
    """
      1. reads the file through a stream,
      2. adds the dictionary to the list of items
      :param input.file as string: the path to the data file, minus the format
      :returns items as list of dictionaries: each item representing a data item from the file at input.file
    """
    items = []
    with open(input["file"] + ".csv") as data:  # 1
        for row in csv.DictReader(data, skipinitialspace=True):
            item = {key: value for key, value in row.items()}
            items.append(item)  # 2
    return items


Inputs = [
    {
        "file": "Test",
        "template": satellite_template
    }
]

if __name__ == "__main__":
    satellite_graph(inputs=Inputs, data_path="../Results/Day3/", database_name ="sched_final")