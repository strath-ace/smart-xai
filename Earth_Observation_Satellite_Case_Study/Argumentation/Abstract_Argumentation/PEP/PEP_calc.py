# PEP calculation 3

from Earth_Observation_Satellite_Case_Study.Argumentation.Abstract_Argumentation.PEP.contraints_considered_add2 import attack_calculation

def PEP_action_a(a, m, i, ma1, ma2, ma3,  count_coord, lines_cp_coord, lines_attack_coord, addrx, a2, m_max, add1, add2):
    mi_a = m
    violation1 = ''
    start_time2 = 0
    mi_a2 = 0
    if (add2 > add1) : # attack add2 with add1
        #print(add1)
        # for the first address
        for n in range(add1,add2):
            #print('n1',n,i,add1,add2)

            start_time2 = lines_cp_coord[i+n-add1].split()[0]
            #start_time2 = int(solver_values[0])
            S_1 = lines_attack_coord[i+n-add1].split()[4]

            if n == add1:
                mi_a = m # new memory for action swap

            else:
                if S_1 == '0':
                    mi_a = mi_a + ma1
                elif S_1 == '1':
                    mi_a = mi_a + ma2
                elif S_1 == '2':
                    mi_a = mi_a + ma3
                else:
                    mi_a = mi_a

            if mi_a > m_max or mi_a <= 0:
                violation1 = 'Exceeded'
                a = '-'
                break



        #mi_a2 = mi_a

        #S_1 = lines_cp_coord[add2].split()[]
        # for the second address
        mi_a2 = attack_calculation(a2,addrx, mi_a, lines_cp_coord, lines_attack_coord)


        for n in range(add2, count_coord - 1):

            if mi_a2 > m_max or mi_a2 <= 0:
                violation1 = 'Exceeded'
                a = '-'
                break

            #print('n2',n,i,add1,add2)
            #print('ack',n,i+n-add2, count_coord - 1,i,add1,S_1 )

            if n >= count_coord - i:
                S_1 = lines_attack_coord[n].split()[4]
                start_time2 = lines_cp_coord[n].split()[0]
            else:
                S_1 = lines_attack_coord[i+n-add2].split()[4]
                start_time2 = lines_cp_coord[i+n-add2].split()[0]

            if n == add2:
                mi_a2 = mi_a2
                # if a2 == '0':
                #     mi_a2 = mi_a + ma1
                # elif a2 == '1':
                #     mi_a2 = mi_a + ma2
                # elif a2 == '2':
                #     mi_a2 = mi_a + ma3
                # else:
                #     mi_a2 = mi_a

            else:
                if S_1 == '0':
                    mi_a2 = mi_a2 + ma1
                elif S_1 == '1':
                    mi_a2 = mi_a2 + ma2
                elif S_1 == '2':
                    mi_a2 = mi_a2 + ma3
                else:
                    mi_a2 = mi_a2


            # check if memory is exceeded
            if mi_a2 > m_max or mi_a2 <= 0:
                violation1 = 'Exceeded'
                a = '-'

                break
            else:
                if n == count_coord - 1:
                    violation1 = 'Not_exceeded'
                else:
                    violation1 = 'Not_exceeded'
                a = '-'
            #print(mi_a2)

    return i, a, violation1, start_time2, mi_a, mi_a2