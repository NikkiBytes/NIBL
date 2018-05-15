##### get files
##### parse:
# START, LEVEL ROWS
# ONSETS col1, IMAGES col3, TASTE TYPE col8

#### manipulate:
# ADJUST ONSET TIMES : ( - start_time)

#### write to outfile (.tsv)


import glob
import os
import sys

f = glob.glob('*.log')

subj = {}
handles = []
names = []

subjects = []

for l in f:
    handles.append(open(l))

subject_file = open('subject_conversion.txt', 'r')

for line in subject_file:
    subjects.append(line) #appending the subject to the list

for handle in range(0, len(handles)):
    subject_name = handles[handle].name.split('-')[0]
    subj[subject_name] = []

for handle in range(0, len(handles)):
    subject_name = handles[handle].name.split('-')[0]
    # print(subject_name.split()[0])
    # subj[subject_name] =[]
    # print(subject_name)
    onsets = []
    images = []
    tastes = []
    rinses = []
    count = []
    # parse images/ taste/ time

    for x in handles[handle].readlines():
        line = x.strip().split()

        onsets.append(line)

        if line[1] == "Level" and "image" in line[2]:
            image = line[2]
            cue_onset = line[0]

            if "not" in image:

                val = "2"
            elif "water" in image:
                val = "0"

            else:
                val = "1"
            temp = [cue_onset, image, val]

            images.append(temp)
        elif line[1] == "Level" and "injecting" in line[2]:
            taste_time = line[0]
            taste_type = line[7]
            temp = [taste_time, taste_type]
            tastes.append(temp)

        else:
            pass

    for t in images:
        rinse = float(t[0]) + 8
        rinses.append(rinse)

    if len(onsets) > 1:
        start_time = float(onsets[0][0])

        for index, y in enumerate(images):
            # print("Before........" + str(images[index][0]))
            time = float(y[0]) - start_time
            images[index][0] = time
            # print("After.........." + str(images[index][0]))

        for index, y in enumerate(tastes):
            # print("Before........" + str(tastes[index][0]))
            time = float(y[0]) - start_time
            tastes[index][0] = time
            # print("After.........." + str(tastes[index][0]))

        for index, y in enumerate(rinses):
            # print("Before........" + str(rinses[index]))
            time = float(y) - start_time
            rinses[index] = time
            # print("After.........." + str(rinses[index]))

    for line in subjects:
        if subject_name in line.split()[0]:
            tag = line.split()[1]
            print(tag)
            if not os.path.exists(str(tag)):
                os.makedirs(str(tag))
                subj[subject_name].append(1)
                run = sum(subj[subject_name])
                run = '{0:02d}'.format(run)
                cue_file = "sub-" + str(tag) + "_task-cue_run-" + str(run) + "_events.tsv"
                taste_file = "sub-" + str(tag) + "_task-taste_run-" + str(run) + "_events.tsv"
                rinse_file = "sub-" + str(tag) + "_task-rinse_run-" + str(run) + "_events.tsv"

                print(tag, subject_name)
                with open(os.path.join(str(tag), cue_file), 'w') as f:
                    f.write("Onset" + "\t" + "Duration" + "\t" + "Cue" + "\t" + "stim_file" + "\n")

                    for x in images:
                        onset = str(x[0])
                        image = str(x[1])
                        cue = str(x[2])
                        f.write(onset + "\t" + "1" + "\t" + cue + "\t" + image + "\n")
                with open(os.path.join(str(tag), taste_file), 'w') as f:
                    f.write("Onset" + "\t" + "Duration" + "\t" + "Taste" + "\n")

                    for x in tastes:
                        time = str(x[0])
                        taste = str(x[1])
                        f.write(time + "\t" + "3" + "\t" + taste + "\n")
                with open(os.path.join(str(tag), rinse_file), 'w') as f:
                    f.write("Onset" + "\t" + "Duration" + "\t" + "Rinse" + "\n")

                    for x in rinses:
                        rinse = str(x)

                        f.write(rinse + "\t" + "3" + "\t" + "1" + "\n")
            else:
                subj[subject_name].append(1)
                run = sum(subj[subject_name])
                run = '{0:02d}'.format(run)
                cue_file = "sub-" + str(tag) + "_task-cue_run-" + str(run) + "_events.tsv"
                taste_file = "sub-" + str(tag) + "_task-taste_run-" + str(run) + "_events.tsv"
                rinse_file = "sub-" + str(tag) + "_task-rinse_run-" + str(run) + "_events.tsv"

                print(tag, subject_name)
                with open(os.path.join(str(tag), cue_file), 'w') as f:
                    f.write("Onset" + "\t" + "Duration" + "\t" + "Cue" + "\t" + "stim_file" + "\n")

                    for x in images:
                        onset = str(x[0])
                        image = str(x[1])
                        cue = str(x[2])
                        f.write(onset + "\t" + "1" + "\t" + cue + "\t" + image + "\n")
                with open(os.path.join(str(tag), taste_file), 'w') as f:
                    f.write("Onset" + "\t" + "Duration" + "\t" + "Taste" + "\n")

                    for x in tastes:
                        time = str(x[0])
                        taste = str(x[1])
                        f.write(time + "\t" + "3" + "\t" + taste + "\n")
                with open(os.path.join(str(tag), rinse_file), 'w') as f:
                    f.write("Onset" + "\t" + "Duration" + "\t" + "Rinse" + "\n")

                    for x in rinses:
                        rinse = str(x)

                        f.write(rinse + "\t" + "3" + "\t" + "1" + "\n")
        else:
            pass

