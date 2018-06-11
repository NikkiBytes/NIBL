

# I. first get the subject, trial type, and the run num
# II. match bevel num with sub num
# III. open file and parse out column 1 and 2
# IV. open sub file and add info
# V. Repeat || Exit

# Tasks: [bitter, sweet, neutral (neu), image (img)]

import glob


f = glob.glob('*.txt')

files = []
subs = {}

for l in f:
  files.append(open(l))


with open('/projects/niblab/bids_projects/Raw_Data/Bevel/Bevel.txt', 'r') as file:
    subjects = file.readlines()

# make dictionary
for sub in subjects:
        sub = sub.strip()
        x = sub.split(' ')[0]
        y = sub.split(' ')[2].split('_')[0]
        subs[y] = x


# go through each onset file
for file in range(0, len(files)):
    y = files[file].name.strip()
    original_id = files[file].name.split('_')[0]
    task = files[file].name.split('_')[1]
    #run_id = files[file].name.split('_')[2].split('.')[0]
    #runs[run_id] = [original_id, task, run_id]



    if original_id in subs:
        # we have the BIDS folder
        print("Here")
        filename='etc/'+str(subs[original_id])+'_'+str(y)
        print(filename)
        NEWFILE = open(filename, 'w')
        for x in files[file].readlines():
            x = x.strip()

            NEWFILE.write(x, '\t', task)


    else:
        print("There")
        filename = 'etc/sub-XX_'+str(y)
        NEWFILE = open(filename, 'w')
        for x in files[file].readlines():
            x = x.strip()

            NEWFILE.write(x, '\t', task)


## Need to correct output
