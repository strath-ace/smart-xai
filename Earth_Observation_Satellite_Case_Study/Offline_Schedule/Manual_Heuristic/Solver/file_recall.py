# to call last read data in file n-1 or n depending on the day and if file already exists
def file_recall(filename, list_num):
    results_coord = open(filename, "r")
    results_count_coord = 0
    for line in results_coord:
        if line != "\n":
            results_count_coord += 1
    results_coord.close()

    results_coord = open(filename, "r")
    # print(results_count)
    results_count_coord = results_count_coord
    results_coord = results_coord.read()
    results_coord = results_coord.split('\n')
    results_data = results_coord[results_count_coord - 1].split()

    pics_count = int(results_data[6])
    processed_pics_count = int(results_data[8])
    downloaded_instances = int(results_data[10])
    idle_time = int(results_data[14])

    # Carry over last data stored in table
    memory_total = memory = int(results_data[4])
    pics_taken = num_pics = int(float(results_data[5]) * 100)
    processed_images = num_processed = int(float(results_data[7]) * 100)

    memory_keep = [memory]
    processed_keep = [num_processed]
    photos_keep = [num_pics]
    if list_num == 1:
        print(results_count_coord, memory, num_pics, num_processed, memory_keep, processed_keep, photos_keep)
        return results_count_coord, memory, num_pics, num_processed, memory_keep, processed_keep, photos_keep
    else:
        print(results_count_coord, pics_count, processed_pics_count, downloaded_instances, idle_time, memory_total, processed_images, pics_taken)
        return results_count_coord, pics_count, processed_pics_count, downloaded_instances, idle_time, memory_total, processed_images, pics_taken
