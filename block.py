#####################IDEA################################
#1.Convert all the raw data into numbers, O(n)
#2.We get a set of time range(we called this busy-time)
#3.We consider the time before 8am and after 10pm as busy-time, O(7)
#4.Union all the busy-time, O(nlog(n)), if I implement non-comparison sorting, it could be O(n)
#5.We get the compliment of the busy-time in the following week(available-time), O(n)
#6.Compare and get the longest time range, O(n)
# Overall, O(nlog(n)), but it is possible to make it O(n)
#########################################################
import datetime as DT

#retrieve from http://www.geekviewpoint.com/python/sorting/radixsort
def radixsort( aList ):
  RADIX = 10
  maxLength = False
  tmp , placement = -1, 1
 
  while not maxLength:
    maxLength = True
    # declare and initialize buckets
    buckets = [list() for _ in range( RADIX )]
 
    # split aList between lists
    for  i in aList:
      tmp = i / placement
      buckets[tmp % RADIX].append( i )
      if maxLength and tmp > 0:
        maxLength = False
 
    # empty lists into aList array
    a = 0
    for b in range( RADIX ):
      buck = buckets[b]
      for i in buck:
        aList[a] = i
        a += 1
 
    # move to next digit
    placement *= RADIX

def to_int(dt_object):
    return int(dt_object.strftime("%Y%m%d%H%M%S"))

#convert the raw data to a pair of two time numbers
def convert(line_info):
    start_time = line_info[0]
    end_time = line_info[1]
    if start_time[0] == ' ':
        start_time = start_time[1:]#remove white space
    if end_time[0] == ' ':
        end_time = end_time[1:]#remove white space
    try:
        st = DT.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        et = DT.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        st_num = to_int(st)
        et_num = to_int(et)
    except:
        traceback.print_exc()
        print('datetime format does not match')
        raise Exception()
    event = (st_num,et_num)
    return event

def union(a):
    b = []
    sorted(a)
    for begin,end in a:
        if b and b[-1][1] >= begin - 1:
            b[-1][1] = max(b[-1][1], end)
        else:
            b.append([begin, end])
    return b

#gives a list of intervals between 22pm and 8am on the next day
def non_meeting_time():
    lst = []
    today = DT.datetime.today()
    for d in range(-1,7):
        day = today + DT.timedelta(days=d)
        ten_pm = day.replace(hour=22,minute=00,second=00)
        next_day = today + DT.timedelta(days=(d+1))
        eight_am = next_day.replace(hour=8,minute=00,second=00)
        eam = to_int(eight_am)
        tpm = to_int(ten_pm)
        lst.append((tpm,eam))
    return lst

#gives the time intervals when every user is free between today 8am
#    and the next week 22pm
def available_in_one_week(busy_time):
    today = DT.datetime.today()
    begining_time = to_int(today.replace(hour=8,minute=00,second=00))
    last_day = today + DT.timedelta(days=6)
    ending_time = to_int(last_day.replace(hour=22,minute=00,second=00))
    available_list = []
    for i in range(len(busy_time)-1):
        busy = busy_time[i]
        if busy[1] < begining_time:continue
        if busy[0] < begining_time and busy[1] > ending_time:break
        if busy[0] > ending_time: break
        else:
            avai_time = (busy[1], busy_time[i+1][0])
            available_list.append(avai_time)
    return available_list

#convert integer of date to string of date 
def to_str(time):
    time_str = str(time)
    time_info = time_str[0:4] + '-' + time_str[4:6] + '-'+ time_str[6:8] +' '
    time_info += time_str[8:10] + ':' + time_str[10:12] + ':' + time_str[12:14]
    return time_info

#gives the longest time interval 
def longest_time(time_list):
    longest = ()
    delta1 = 0
    for time in time_list:
        delta2 = time[1] - time[0]
        if(delta1 < delta2):
            longest = time
            delta1 = longest[1] - longest[0]
    lst_longest = []
    # find the interval has the same length
    for time in time_list:
        delta2 = time[1] - time[0]
        if(delta1 == delta2):
            lst_longest.append(time)
    return lst_longest

def main():    
    #convert the raw data to datetime object
    time_list = []
    with open('calendar.csv', 'r') as csv:
        for line in csv.readlines():
            line_info = line.rstrip().split(",")   
            time_list.append(convert(line_info[1:3]))#ignore user id
    #check if we have invalid time interval
    for time in time_list:
        if time[0] > time[1]:
            print('invalid time interval: from ' + str(time[0]) + ' to '+str(time[1]))
    #consider the time before 8am and after 10pm as busy time
    time_list += non_meeting_time()
    #union all the busy time in one list
    busy_time = union(time_list)
    #get the compliment of busy time in the following week
    available_time = available_in_one_week(busy_time)
    #get the longest time interval
    longest = longest_time(available_time)
    #print the result
    print('Longest time intervals:')
    for l in longest:
        print('from '+ to_str(l[0])+ ' to '+ to_str(l[1]))
    return 0
main()
