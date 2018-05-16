

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
runs = {}

for l in f:
  files.append(open(l))


with open('/projects/niblab/bids_projects/Raw_Data/Bevel/Bevel.txt', 'r') as file:
    subjects = file.readlines()

# make dictionary of subjects that have gone through BIDS
for sub in subjects:
        sub = sub.strip()
        x = sub.split(' ')[0]
        y = sub.split(' ')[2].split('_')[0]
        subs[y] = x


# make runs dictionary
for file in range(0, len(files)):
    name = files[file].name.strip()
    original_id = files[file].name.split('_')[0]

    run_id = files[file].name.split('_')[2].split('.')[0]
    dict_key = str(original_id) + "_" + str(run_id)
    runs[dict_key] = []



for file in range(0, len(files)):
    original_id = files[file].name.split('_')[0]
    run_id = files[file].name.split('_')[2].split('.')[0]
    dict_key = str(original_id) + "_" + str(run_id)
    task = files[file].name.split('_')[1]

    for x in files[file].readlines():
        x = x.strip()
        new_line = x + "\t" + task
        runs[dict_key].append(new_line)




# Add run0X to the correct folder

    if original_id in subs:
        # we have the BIDS folder
        print("Here")
        filename='etc/'+str(subs[original_id])+'_'+str(name)
        print(filename)
        #NEWFILE = open(filename, 'a')
        for x in files[file].readlines():
            x = x.strip()
            print()

            #NEWFILE.write(x, '\t', task)

        #NEWFILE.close()
    else:
        print("There")
        filename = 'etc/sub-XX_'+str(name)
        #NEWFILE = open(filename, 'a')
        for x in files[file].readlines():
            x = x.strip()
        #NEWFILE.close()

        #    NEWFILE.write(x, '\t', task)


## Need to correct output
