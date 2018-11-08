import glob, os
import psutil 
from multiprocessing import Pool
input_dir = "/home_dir/Experiments/ChocoData/BIDS/ses-4"
fmriprep_dir = "/home_dir/Experiments/ChocoData/fmriprep"
error_dir = "/home_dir/Experiments/ChocoData/error_files"
SUBJECTS = glob.glob(os.path.join(input_dir, "sub-*"))
chunksize = int(len(SUBJECTS)/3)
cores=psutil.cpu_count(logical=False)
threads=10
sess="ses-4"
def run_fmriprep(sub_path):
    sub = sub_path.split("/")[-1]
    output_dir = os.path.join(fmriprep_dir, sub, sess)
    cmd = "fmriprep %s %s \
    participant  \
    --participant-label %s  \
    --fs-license-file freesurfer/license.txt \
    --longitudinal \
    --fs-no-reconall \
    --omp-nthreads %s --n_cpus %s  \
    --bold2t1w-dof 12 \
    --output-space template --template MNI152NLin2009cAsym \
    --debug  \
    -w %s \
    --resource-monitor --write-graph --stop-on-first-crash"%(input_dir, output_dir, sub, threads, cores, output_dir)
    #print(cmd)
    try:
        os.system(cmd)
    except Exception as e:
        with open(error_dir+"/error_fmriprep_ses-4.txt", "a")  as f:
            f.write(">>>----> ", str(e))
            f.close()
if __name__ == '__main__':
    pool = Pool(psutil.cpu_count(logical=False))
    pool.map(run_fmriprep, SUBJECTS, chunksize)
    pool.close()
    pool.join()

