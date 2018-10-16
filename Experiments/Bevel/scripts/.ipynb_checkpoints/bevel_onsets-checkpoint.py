

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
    print("NAME: ", name)
    print("ORIGINAL ID: ", original_id)
    run_id = files[file].name.split('_')[2].split('.')[0]
    dict_key = str(original_id) + "_" + str(run_id)
    runs[dict_key] = []


# fill dictionary with correct info
for file in range(0, len(files)):
    original_id = files[file].name.split('_')[0]
    run_id = files[file].name.split('_')[2].split('.')[0]
    run_id = run_id.replace('0', '-')
    print(run_id)
    dict_key = str(original_id) + "_" + str(run_id)
    task = files[file].name.split('_')[1]
    for x in files[file].readlines():
        x = x.strip()
        x = x.strip('\t')
        new_line = x + "\t" + task
        runs[dict_key].append(new_line)


# def sort list
def sort_info(dict_key):
    runs[dict_key] = sorted(runs[dict_key], key=lambda x: float(x.split()[0]))
# Write to correct files

for key in runs:
    sort_info(key)

for key, value in runs.items():
    new_key = key.split('_')[0]
    run_id = key.split('_')[1]
    run_id = run_id.replace('0','-')
    print(run_id)
    header = "onsets\tduration\tparametric modulator\ttrial_type"
    if new_key in subs:
        # we have the BIDS folder
        # sort values
        print("Has BIDS")
        
        #sub-001_task-prob_run-3_events
        filename = str(subs[new_key])+"_task-prob_"+run_id+"_events.tsv")
        print(filename)
        with open(filename, 'w') as file:
            file.write(header + '\n')
            for line in value:
                file.write(line + '\n')
            file.close()
            
    else:
        print("Needs BIDS")
        filename = str(key)+'.tsv'
        print(filename)
        with open(filename, 'w') as file:
            file.write(header + '\n')
            for line in value:
                file.write(line + '\n')
            file.close()
