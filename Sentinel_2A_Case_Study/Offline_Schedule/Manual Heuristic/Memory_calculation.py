import pandas as pd
import datetime as dt

def Heuristic_memory_calculation(patha,day):

    file1 = open(patha+'/manual_memory_states_seconds'+str(day)+'.txt', "w")
    file2 = open(patha+'/manual_memory_states'+str(day)+'.txt', "w")

    if day ==1:
        path = patha+'/Manual_Results'+str(day)+'.txt'

    elif day >1:
        path = patha + '/Manual_Results' + str(day) + '.txt'
        path2 = patha + '/Manual_Results' + str(day-1) + '.txt'

        f_coord = open(path2, "r")
        line_count_coord = 0
        for line in f_coord:
            if line != "\n":
                line_count_coord += 1
        f_coord.close()

        f_coord = open(path, "r")
        node_count_coord = line_count_coord
        content_coord = f_coord.read()
        lines_coord = content_coord.split('\n')
    else:
        print('ERROR')

    f_coord = open(path, "r")
    line_count_coord = 0
    for line in f_coord:
        if line != "\n":
            line_count_coord += 1
    f_coord.close()

    f_coord = open(path, "r")
    node_count_coord = line_count_coord
    content_coord = f_coord.read()
    lines_coord = content_coord.split('\n')


    time_interval=5
    onboard_mem = 0.8*24 * 10 ** 5
    # memory required per image
    image_mem = 2688
    downlink_data_rate = -280 * time_interval
    # 5000Kbit/s to process images
    process_im_mem = 50 * time_interval

    Demands_mem = []
    start_ints = []
    Actives = []
    tasks_list = []
    weights2 = []
    final_total=[]
    Actives_List =[]
    h_list=[]
    end=[]
    duration=[]
    jobs=[]

    total_pics=[]
    total_process=[]
    total_down=[]
    total_idle=[]
    process_count=[]
    pictures_count=[]
    download_count=[]

    tot_pic = 0
    tot_proc = 0
    tot_down=0
    tot_idle = 0
    #count the number of instances process has occurred
    count_proc=0
    count_pic=0
    count_down=0

    z=0
    for task in range(0, node_count_coord):

        line_details = lines_coord[task].split()
        final_end = int(line_details[2])
        final_start = int(line_details[1])
        final_jobs = line_details[4]
        final_duration = int(line_details[3])

        h = 0

        while h <= (int(final_end / 1000) - int(final_start / 1000)) and (int(final_end / 1000) - int(final_start / 1000))>time_interval:
            # for i in range(int(final_start[task]/1000),int(final_end[task]/1000)):
            start = int(final_start / 1000) + h

            tasks = final_jobs
            if z < 1000:
                z += 1
                tot_down = tot_down
            else:
                z = 0
                tot_down = 0

            if '1' in tasks_list:

                if final_jobs == '1' and Demands_mem[len(Demands_mem)-1]<(onboard_mem ) and (tot_pic <= (onboard_mem )/image_mem) and (((image_mem*tot_pic)+(process_im_mem*tot_proc)) < onboard_mem):
                    weight2 = 2
                    #pic_chosen = random.randint(0, 1)
                    pic_chosen =1
                    tot_pic +=1
                    count_pic+=1

                    Demands = image_mem * pic_chosen
                elif final_jobs == '2' and Demands_mem[len(Demands_mem)-1]<(onboard_mem ) and tot_proc<(tot_pic*image_mem/process_im_mem):
                    weight2 = 2
                    tot_proc+=1
                    count_proc+=1

                    Demands = process_im_mem #* time_interval
                elif final_jobs == '3':
                    weight2 = 0
                    Demands = 0

                elif final_jobs == '4' and tot_proc>image_mem/process_im_mem :# and  (tot_proc > (-downlink_data_rate/process_im_mem)):
                    weight2 = 2
                    tot_down+=1
                    count_down +=1
                    tot_proc = tot_proc + (downlink_data_rate/process_im_mem)
                    tot_pic = tot_pic+(downlink_data_rate/image_mem)
                    Demands = (tot_proc*process_im_mem)+(tot_pic*image_mem) #* time_interval
                    Demands = -(final_total[len(final_total)-1]-Demands)

                else:
                    weight2 = 0
                    Demands = 0

            else:
                if final_jobs == '1'and (tot_pic <= (onboard_mem )/image_mem)  :
                    weight2 = 2
                    tot_pic+=1
                    count_pic +=1
                    #pic_chosen = random.randint(0, 1)
                    pic_chosen =1
                    Demands = image_mem * pic_chosen
                else:
                    weight2 = 0
                    Demands = 0



            total = Demands

            if h == 0 and len(final_total) ==0 and total==0:
                total = Demands
                Actives = False

            elif h == 0 and len(final_total) ==0 and total>0:
                total = Demands
                Actives = True

            elif h == 0 and len(final_total) ==0 and total<0:
                total = 0
                Actives = False

            elif h== 0 and final_total[h - 1] > 0 and Demands != 0:
                total = final_total[h - 1] + Demands

                if total > 0 and total <= onboard_mem:
                    total = Demands + final_total[h - 1]
                    Actives = True
                else:
                    total = final_total[h - 1]
                    Actives = False

            elif  h>0 and final_total[len(final_total)-1] > 0 and Demands !=0 :
                total = final_total[len(final_total)-1]  + Demands

                if total > 0 and total <= onboard_mem:
                    total = Demands + final_total[len(final_total)-1]
                    Actives = True
                else:
                    total = final_total[len(final_total)-1]
                    Actives = False

            elif (h==0 or h>0) and final_total[len(final_total)-1] == 0 and Demands !=0 :
                total = final_total[len(final_total)-1]  + Demands

                if total > 0 and total <= onboard_mem:
                    total = Demands + final_total[len(final_total)-1]
                    Actives = True
                else:
                    total = final_total[len(final_total)-1]
                    Actives = False

            elif Demands ==0:
                total = Demands + final_total[len(final_total)-1]
                Actives =False

            if final_jobs=='2' and Actives == False and tot_proc >1:
                tot_proc -=1
                count_proc-=1

            if final_jobs=='1' and Actives == False and tot_pic> total_pics[len(total_pics)-1]:
                tot_pic -=1
                count_pic -=1

            if Actives == False:
                tot_idle += 1

            final_total.append(total)
            #print(z)


                # print(i)
            #final_total.append(total)
            Demands_mem.append(Demands)
            start_ints.append(start)
            end.append(start+time_interval)
            duration.append(time_interval)
            tasks_list.append(tasks)
            weights2.append(weight2)
            Actives_List.append(Actives)
            jobs.append(final_jobs)
            h_list.append(h)
            #total pics left in memory
            total_pics.append(tot_pic)
            #total_pics_taken
            pictures_count.append(count_pic)
            #total images left in memory
            total_process.append(tot_proc)
            #total downlink
            total_down.append(tot_down)
            #counts the total downlink
            download_count.append(count_down)
            total_idle.append(tot_idle)
            #counting the total number of images processed
            process_count.append(count_proc)
            h += time_interval

    print_list=[]
    print_list2=[]
    for i in range (0, len(tasks_list)):


        print([str(dt.timedelta(seconds=(start_ints[i]))), tasks_list[i], Demands_mem[i], h_list[i],final_total[i],Actives_List[i],total_pics[i],total_process[i]/ (image_mem / process_im_mem),
               total_down[i]/  (image_mem / -downlink_data_rate),total_idle[i],pictures_count[i],process_count[i]/  (image_mem / process_im_mem),download_count[i]/ (image_mem / -downlink_data_rate)])

        print_list.append([str(dt.timedelta(seconds=(start_ints[i]))),str(dt.timedelta(seconds=(end[i]))), tasks_list[i], Demands_mem[i], h_list[i],final_total[i],Actives_List[i],total_pics[i],
                           total_process[i]/ (image_mem / process_im_mem),
               total_down[i]/ (image_mem / -downlink_data_rate),total_idle[i],pictures_count[i],process_count[i]/ (image_mem / process_im_mem),download_count[i]/ (image_mem / -downlink_data_rate)])

        print_list2.append([start_ints[i],end[i], tasks_list[i], Demands_mem[i], h_list[i],final_total[i],Actives_List[i],total_pics[i],total_process[i]/  (image_mem / process_im_mem),
               total_down[i]/  (image_mem / -downlink_data_rate),total_idle[i],pictures_count[i],process_count[i]/  (image_mem / process_im_mem),download_count[i]/  (image_mem / -downlink_data_rate)])


    df1 = pd.DataFrame(print_list2)
    file1.writelines(df1.to_string(header=False, index=False))
    file1.close()


    df2 = pd.DataFrame(print_list)
    file2.writelines(df2.to_string(header=False, index=False))
    file2.close()

