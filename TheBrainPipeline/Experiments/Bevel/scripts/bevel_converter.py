# Nichollette Acosta |Heuristic phantom converter for phantom-1
# 9/4/2017

# Phantom heurisitc converter
# Very simple ~ can be upgraded/modified
# Searches for T1w files and dwi files

import os
subject = os.environ["id"]

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    # create directories

    # anat/
    t1 = create_key('anat/sub-' + subject+ '_T1w')


    # fmap/
    fmap_phase = create_key('fmap/sub-' + subject + '_phasediff')
    fmap_magnitude = create_key('fmap/sub-' + subject + '_magnitude')


    # func/
    rest = create_key('func/sub-' + subject + '_task-rest_bold')
    run01 = create_key('func/sub-' + subject + '_task-prob_run-1_bold')
    run02 = create_key('func/sub-' + subject  + '_task-prob_run-2_bold')
    run03 = create_key('func/sub-' + subject + '_task-prob_run-3_bold')
    run04 = create_key('func/sub-'+ subject + '_task-prob_run-4_bold')



    info = {t1: [],  fmap_phase: [], rest: [], run01: [], run02: [], run03: [], run04: [], fmap_magnitude: []}
    for s in seqinfo:
        print(s)
        if (s.dim3 == 192) and ('anat' in s.protocol_name):
            info[t1].append(s.series_id)  ## append if multiple series meet criteria
        if (s.dim3 == 72) and ('fmap' in s.protocol_name):
            info[fmap_magnitude].append(s.series_id)  ## append if multiple series meet criteria
        if (s.dim3 == 36) and ('fmap' in s.protocol_name):
            info[fmap_phase].append(s.series_id)  # append if multiple series meet criteria
        if  ('run01' in s.protocol_name):
            info[run01].append(s.series_id)  # append if multiple series meet criteria
        if ('run02' in s.protocol_name):
            info[run02].append(s.series_id)
	if (s.dim4 == 150) and ('resting' in s.protocol_name):
            info[rest].append(s.series_id)  # append if multiple series meet criteria
        if ('run03' in s.protocol_name):
            info[run03].append(s.series_id)  # append if multiple series meet criteria
        if ('run04' in s.protocol_name):
            info[run04].append(s.series_id)
	##if (s.dim4 == 170) and ('bold' in s.protocol_name):
            #info[pictures].append(s.series_id)  # append if multiple series meet criteria

    return info
