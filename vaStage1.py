import os
import warnings
import textwrap
import subprocess
import errno

def create_vaStage1_condor_script(
        vbf,
        output_dir=".", 
        T_factors="1/0.742,2/0.665,3/0.735,4/0.701",
        G_factors="1/0.922,2/0.984,3/1.022,4/1.039",
        ):
    """
    Generates a condor vaStage1 script.

    Parameters
    ----------
    vbf : string
        vbf file to be processed
    vaStage1Output : string
        VEGAS Stage1 output file
        Will take care to rename file with .stage2.root extension
    output_dir : str, optional
        where SLURM will send command-line output/error, by default "."
    T_factor : str, optional
        vector-like (as in C/C++) specifying throughput correction factor
        defaults to 2023/2024 winter value
    G_factor : str, optional
        vector-like (as in C/C++) specifying gain correction factor
        defaults to 2023/2024 winter value

    Returns
    -------
    string containing path to condor sub script that was just created

    """    
    VEGAS = os.environ.get('VEGAS')

    if not VEGAS:
        raise EnvironmentError("VEGAS environment variable is not set.")

    exe = os.path.join(VEGAS, "bin", "vaStage1")
    
    if not os.path.exists(exe):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"{exe}")

    if not os.path.exists(vbf):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"{vbf}")        

    if not os.path.exists(output_dir):
        warnings.warn(f"Directory '{output_dir}' does not exist. It will be created.", UserWarning)
        os.makedirs(output_dir, exist_ok=True)

    file_basename = os.path.splitext(os.path.basename(vbf))[0]
    
    out = os.path.join(output_dir, f"{file_basename}.stg1.condor.out")
    error = os.path.join(output_dir, f"{file_basename}.stg1.condor.error")
    log = os.path.join(output_dir, f"{file_basename}.stg1.condor.log")

    vaStage1Output = os.path.join(output_dir, f"{file_basename}.stg1.root")

    script_content = textwrap.dedent(f"""\
    Universe     = vanilla
    Executable   = {exe}
    Arguments    = -Stage1_RunMode=data -G_SimulationMode=1 -RHM_ObservingMode=drift -CRH_Algorithm=VASimulationRunHeaderFiller -QSCTD_ScaleThroughput={T_factors} -QSCTD_ScaleGain={G_factors} -AIFC_CameraRotation=1/0.0,2/0.0,3/0.0,4/0.0 {vbf} {vaStage1Output}
    Requirements = 
    Environment  = "VEGAS={VEGAS}"
    GetEnv       = True
    image_size   = 1638400
    want_graceful_removal = True

    Output = {out}
    Error  = {error}
    Log    = {log}

    Queue
    """)

    script_path = os.path.join(output_dir, f"{file_basename}.stg1.condor.sub")
    with open(script_path, "w") as script_file:
        script_file.write(script_content)
        return script_path

