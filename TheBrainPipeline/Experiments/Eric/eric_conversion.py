# Nichollette Acosta | Heuristic phantom converter for phantom-1
# 9/4/2017#

# Phantom heurisitc converter
# Very simple ~ can be upgraded/modified
# Searches for T1w files and dwi files

import os
subject = os.environ["f"]

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

    milkA = create_key('func/sub-' + subject + '_task-milkshakeA_bold' )
    milkB = create_key('func/sub-' + subject + '_task-milkshakeB_bold')
    milkC = create_key('func/sub-' + subject + '_task-milkshakeC_bold')
    milkD = create_key('func/sub-' + subject + '_task-milkshakeD_bold')
    noGo1 = create_key('func/sub-' + subject + '_task-Go_NoGo1_bold')
    noGo2 = create_key('func/sub-' + subject + '_task-Go_NoGo2_bold')
    imagine = create_key('func/sub-' + subject + '_task-imagine_bold')

    milkA_moco = create_key('func/sub-' + subject + '_ses-4_task-milkshakeA_physio_bold' )
    milkB_moco = create_key('func/sub-' + subject + '_task-milkshakeB_physio_bold')
    milkC_moco = create_key('func/sub-' + subject + '_task-milkshakeC_physio_bold')
    milkD_moco = create_key('func/sub-' + subject + '_task-milkshakeD_physio_bold')
    noGo1_moco = create_key('func/sub-' + subject + '_task-Go_NoGo1_physio_bold')
    noGo2_moco = create_key('func/sub-' + subject + '_task-Go_NoGo2_physio_bold')
    imagine_moco = create_key('func/sub-' + subject + '_task-imagine_physio_bold')

    info = {t1: [],  fmap_phase: [], fmap_magnitude: [], milkA: [], milkB: [], milkC: [], milkD: [], noGo1: [], noGo2: [], imagine: [],
            milkA_moco: [], milkB_moco: [], milkC_moco: [], milkD_moco: [], noGo1_moco: [], noGo2_moco: [], imagine_moco: [] }
    for s in seqinfo:
        print(s)

        if ('t1' in s.protocol_name):
            info[t1].append(s.series_id)  ## append if multiple series meet criteria

        if (s.dim3 == 54) and ('field_map' in s.protocol_name):
            info[fmap_magnitude].append(s.series_id)  ## append if multiple series meet criteria


        if (s.dim3 == 27) and ('field_map' in s.protocol_name):
            info[fmap_phase].append(s.series_id)  # append if multiple series meet criteria


        if ('milkshake_A' in s.protocol_name):
            if (s.dim4 == 445) and (s.is_motion_corrected == False):
                info[milkA].append(s.series_id)  # append if multiple series meet criteria
            if (s.dim4 == 445) and (s.is_motion_corrected == True):
                info[milkA_moco].append(s.series_id)  # append if multiple series meet criteria

        if ('milkshake_B' in s.protocol_name):
            if (s.dim4 == 445) and (s.is_motion_corrected == False):
                info[milkB].append(s.series_id)  # append if multiple series meet criteria
            if (s.dim4 == 445) and (s.is_motion_corrected == True):
                info[milkB_moco].append(s.series_id)  # append if multiple series meet criteria

        if ('milkshake_C' in s.protocol_name):
            if (s.dim4 == 445) and (s.is_motion_corrected == False):
                info[milkC].append(s.series_id)  # append if multiple series meet criteria
            if (s.dim4 == 445) and (s.is_motion_corrected == True):
                info[milkC_moco].append(s.series_id)  # append if multiple series meet criteria

        if ('milkshake_D' in s.protocol_name):
            if (s.dim4 == 445) and (s.is_motion_corrected == False):
                info[milkD].append(s.series_id)  # append if multiple series meet criteria
            if (s.dim4 == 445) and (s.is_motion_corrected == True):
                info[milkD_moco].append(s.series_id)  # append if multiple series meet criteria

        if ('imagine' in s.protocol_name):
            if (s.dim4 == 475) and (s.is_motion_corrected == False):
                info[imagine].append(s.series_id)  # append if multiple series meet criteria
            if (s.dim4 == 475) and (s.is_motion_corrected == True):
                info[imagine_moco].append(s.series_id)  # append if multiple series meet criteria

        if ('NoGo1' in s.protocol_name):
            if (s.dim4 == 195) and (s.is_motion_corrected == False):
                info[noGo1].append(s.series_id)  # append if multiple series meet criteria
            if (s.dim4 == 195) and (s.is_motion_corrected == True):
                info[noGo1_moco].append(s.series_id)  # append if multiple series meet criteria

        if ('NoGo2' in s.protocol_name):
            if (s.dim4 == 195) and (s.is_motion_corrected == False):
                info[noGo2].append(s.series_id)  # append if multiple series meet criteria
            if (s.dim4 == 195) and (s.is_motion_corrected == True):
                info[noGo2_moco].append(s.series_id)  # append if multiple series meet criteria

    return info
