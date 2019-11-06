import vxi11, sched, time, random, string
import numpy as numpy
import pandas as pd

# Using Agg instead of Xwindows or run ssh -X 
# (comment out these lines if you are running locally)
# import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt

# Define instrument
instr = vxi11.Instrument("172.19.222.92","gpib0,12")
print(instr.ask("*IDN?"))

# Generate session id and create output file in /data
session_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])
f = open("data/session-"+session_id+".txt", "w")
print("Beginning read session: "+session_id)

# Define scheduler and collect user input for timeframe
s = sched.scheduler(time.time, time.sleep)
secs = float(raw_input("Enter number of seconds: "))
end = time.time() + secs

# Define read function, query instrument
def read_power(sc):
    power = instr.ask("measure:scalar:power:real? 0")
    f.write(power+",")
    f.flush()
    if time.time() < end:
      s.enter(1, 1, read_power, (sc,))

# Schedule execution over user-inputted timeframe
s.enter(1, 1, read_power, (s,))
s.run()

# Read delimited session string from file, convert to 2d array
f = open('data/session-'+session_id+'.txt', 'r')
data = f.read().split(",")
del data[-1]
data = [float(i) for i in data]
frames = [data[i*4:(i+1)*4] for i in range(len(data)//4)]

# Generate plot and save to /figures
df = pd.DataFrame(frames, columns=['c09-13', 'c09-14', 'c09-15', 'c09-16'])
plt.figure()
df.plot()
plt.savefig('figures/'+session_id+'.png') 
