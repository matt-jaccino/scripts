import re
from datetime import datetime, timedelta
from subprocess import check_call
from time import sleep


print('*' * 72)
print("Enter time until shutdown in minutes, '[#h] [#m] [#s]', or '@ [HH:MM]'")
inp = input(" > ").replace(' ', '')

now = datetime.now()

if '@' in inp:
    inp.upper()
    shutdown_time = re.search(
        r"\d{1,2}:\d{1,2}",
        inp.split('@', 1)[-1]
    ).group(0)
    if not inp.endswith('M'):
        shutdown_time += 'PM'
    time_diff = datetime.combine(
        now.date(),
        datetime.strptime(shutdown_time, "%I:%M%p").time()
    ) - now
    # negative if time combines before now
    if time_diff.days < 0:
        shutdown_time = shutdown_time[:-2] + "AM"
        time_diff = datetime.combine(
        (now + timedelta(days=1)).date(),
        datetime.strptime(shutdown_time, "%I:%M%p").time()
    ) - now
    secs = time_diff.seconds + 1

elif re.search(r"[hHmMsS]+", inp):
    hours, mins, secs = 0, 0, 0
    inp = inp.lower()
    if 'h' in inp:
        split = inp.split('h', 1)
        hours = int(split[0])
        inp = split[1]
    if 'm' in inp:
        split =  inp.split('m', 1)
        mins = int(split[0])
        inp = split[1]
    if 's' in inp:
        split = inp.split('s', 1)
        secs = int(split[0])
    secs = (hours * 3600) + (mins * 60) + secs

else:
    # Assume minutes
    secs = int(re.search(r"\d+", inp).group(0)) * 60
    

time_of_shutdown = datetime.strftime(now + timedelta(seconds=secs), "%I:%M:%S %p")

print(f"\nShutting down at {time_of_shutdown=}")

check_call(["shutdown", "-s", "-t", str(secs)], shell=True)#, executable="cmd")

print('*' * 72)
sleep(3)
