import os
import warnings
import textwrap
import errno


def create_vaStage2_condor_script(
        vbf,
        laser,  
        output_dir=".", 
        ):
    """
    Generates a condor script to run VEGAS stage 2.

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
    VEGAS = os.environ.get('VEGAS')

    if not VEGAS:
        raise EnvironmentError("SIMTELDIR environment variable is not set.")

    exe = os.path.join(VEGAS, "bin", "vaStage2")
    
    if not os.path.exists(exe):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"{exe}")

    if not os.path.exists(vbf):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"{vbf}")        

    if not os.path.exists(output_dir):
        warnings.warn(f"Directory '{output_dir}' does not exist. It will be created.", UserWarning)
        os.makedirs(output_dir, exist_ok=True)
    
    file_basename = os.path.splitext(os.path.basename(vbf))[0]

    out = os.path.join(output_dir, f"{file_basename}.stg2.condor.out")
    error = os.path.join(output_dir, f"{file_basename}.stg2.condor.error")
    log = os.path.join(output_dir, f"{file_basename}.stg2.condor.log")

    vaStage2Output = os.path.join(output_dir, f"{file_basename}.stg2.root")

    if not os.path.exists(vaStage2Output):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"{vaStage2Output}")  

    script_content = textwrap.dedent(f"""\
    Universe     = vanilla
    Executable   = {exe}
    Arguments    = -G_SimulationMode=1 {vbf} {vaStage2Output} {laser}
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

    script_path = os.path.join(output_dir, f"{file_basename}.stg2.condor.sub")
    with open(script_path, "w") as script_file:
        script_file.write(script_content)
        return script_path
