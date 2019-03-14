# Nichollette Acosta

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
    rest = create_key('func/sub-' + subject + '_task-resting_bold')
    run01 = create_key('func/sub-' + subject + '_task-training_run-1_bold')
    run02 = create_key('func/sub-' + subject  + '_task-training_run-2_bold')
    run03 = create_key('func/sub-' + subject + '_task-training-run-3_bold')
    run04 = create_key('func/sub-'+ subject + '_task-training_run-4_bold')
    run01_rl = create_key('func/sub-'+ subject + '_task-rl_run-1_bold')
    run02_rl = create_key('func/sub-'+ subject + '_task-rl_run-2_bold')



    info = {t1: [],  fmap_phase: [], rest: [], run01: [], run02: [], run03: [], run04: [], fmap_magnitude: [], run01_rl: [], run02_rl: []}
    for s in seqinfo:
        print(s)
        if (s.dim3 == 192) and ('anat' in s.protocol_name):
            info[t1].append(s.series_id)  ## append if multiple series meet criteria
        if (s.dim3 == 72) and ('fmap' in s.protocol_name):
            info[fmap_magnitude].append(s.series_id)  ## append if multiple series meet criteria
        if (s.dim3 == 36) and ('fmap' in s.protocol_name):
            info[fmap_phase].append(s.series_id)  # append if multiple series meet criteria
        if  ('run01' in s.protocol_name) and ('training' in s.protocol_name) and (s.dim4 == 233):
            info[run01].append(s.series_id)  # append if multiple series meet criteria
        if  ('run02' in s.protocol_name) and ('training' in s.protocol_name) and (s.dim4 == 233):
            info[run02].append(s.series_id)
	    if (s.dim4 == 147) and ('resting' in s.protocol_name):
            info[rest].append(s.series_id)  # append if multiple series meet criteria
        if  ('run03' in s.protocol_name) and ('training' in s.protocol_name) and (s.dim4 == 233):
            info[run03].append(s.series_id)  # append if multiple series meet criteria
        if  ('run04' in s.protocol_name) and ('training' in s.protocol_name) and (s.dim4 == 233):
            info[run04].append(s.series_id)
        if  ('rl' in s.protocol_name) and ('run01' in s.protocol_name) and (s.dim4 == 212):
            info[run01_rl].append(s.series_id)
        if  ('rl' in s.protocol_name) and ('run02' in s.protocol_name) and (s.dim4 == 212):
            info[run02_rl].append(s.series_id)


    return info
