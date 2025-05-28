import os
import errno
import subprocess

from vaStage1 import create_vaStage1_condor_script
from vaStage2 import create_vaStage2_condor_script
from vaStage4 import create_vaStage4_condor_script

def submit_job(script_path):
    """
    Submit job to queue.

    Parameters
    ----------
    script_path : string
        path to .condor.sub script
    """    
    subprocess.run(["condor_submit", script_path])

def submit_vaStage1(
        vbf,
        output_dir=".",
        T_factors="1/0.742,2/0.665,3/0.735,4/0.701",
        G_factors="1/0.922,2/0.984,3/1.022,4/1.039",
    ):
    """
    Submits a condor script to  queue
    to run VEGAS stage1.

    Parameters
    ----------
    vbf : string
        vbf file to be processed
    vaStage1Output : string
        VEGAS Stage1 output file
        Will take care to rename file with .stage2.root extension
    output_dir : str, optional
        where SLURM will send command-line output/error, by default "."

    """ 
    vaStage1_condor = create_vaStage1_condor_script(vbf, output_dir, T_factors, G_factors)
    
    submit_job(vaStage1_condor)


def submit_vaStage2(
        vbf, 
        laser, 
        output_dir=".",
        S_factors="1/0.684,2/0.654,3/0.751,4/0.728"
        ):
    
    """
    Submits a condor script to queue
    to run VEGAS stage 2.
    
    It is expected that the stage1 output file
    is located in output_dir

    Parameters
    ----------
    vbf : string
        vbf file to be processed
    laser : string
        VEGAS laser file for calibration
    output_dir : str, optional
        where VEGAS/condor will send outputs and command-line output/error
        by default "."

    """    
    if not os.path.exists(vbf):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"{vbf}")      
        
    file_basename = os.path.splitext(os.path.basename(vbf))[0]

    vaStage1Output = os.path.join(output_dir, f"{file_basename}.stg1.root")
    vaStage2Output = os.path.join(output_dir, f"{file_basename}.stg2.root")

    if not os.path.exists(vaStage1Output):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"{vaStage1Output}") 

    subprocess.run(["mv", vaStage1Output, vaStage2Output])

    if not os.path.exists(vaStage2Output):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"{vaStage2Output}") 

    vaStage2_condor = create_vaStage2_condor_script(vbf, laser, output_dir, S_factors)

    submit_job(vaStage2_condor)

def submit_vaStage4(
        vaStage2Output,
        config,
        cuts,  
        output_dir=".", 
        ):
    """
    Submits a condor script to run VEGAS stage 24

    Parameters
    ----------
    vaStage2Output : string
        VEGAS Stage1 output file
        Will take care to rename file with .stage2.root extension
    config : string
        VEGAS stage4 configuration file
    cuts : string
        VEGAS stage4 cuts file
    output_dir : str, optional
        where SLURM will send command-line output/error, by default "."

    """  
    file_basename = os.path.splitext(str(os.path.splitext(os.path.basename(vaStage2Output))[0]))[0]

    vaStage4Output = os.path.join(output_dir, f"{file_basename}.stg4.root")

    subprocess.run(["cp", vaStage2Output, vaStage4Output])

    if not os.path.exists(vaStage2Output):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"{vaStage2Output}") 

    vaStage4_condor = create_vaStage4_condor_script(vaStage2Output, config, cuts, output_dir)

    submit_job(vaStage4_condor)
