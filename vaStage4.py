import os
import warnings
import textwrap
import errno


def create_vaStage4_condor_script(
        vaStage2Output,
        config,
        cuts,  
        output_dir=".", 
        ):
    """
    Generates a condor script to run VEGAS stage 2.

    Parameters
    ----------
    vaStage2Output : string
        vaStage2 file to be copied
        and renamed to stg4.root
    vaStage1Output : string
        VEGAS Stage1 output file
        Will take care to rename file with .stage2.root extension
    output_dir : str, optional
        where SLURM will send command-line output/error, by default "."

    """    
    VEGAS = os.environ.get('VEGAS')

    if not VEGAS:
        raise EnvironmentError("SIMTELDIR environment variable is not set.")

    exe = os.path.join(VEGAS, "bin", "vaStage4")
    
    if not os.path.exists(exe):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"{exe}")

    if not os.path.exists(config):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"{config}")        

    if not os.path.exists(cuts):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"{cuts}")        

    if not os.path.exists(output_dir):
        warnings.warn(f"Directory '{output_dir}' does not exist. It will be created.", UserWarning)
        os.makedirs(output_dir, exist_ok=True)
        
    file_basename = os.path.splitext(str(os.path.splitext(os.path.basename(vaStage2Output))[0]))[0]

    out = os.path.join(output_dir, f"{file_basename}.stg4.condor.out")
    error = os.path.join(output_dir, f"{file_basename}.stg4.condor.error")
    log = os.path.join(output_dir, f"{file_basename}.stg4.condor.log")

    vaStage4Output = os.path.join(output_dir, f"{file_basename}.stg4.root")

    if not os.path.exists(vaStage4Output):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"{vaStage4Output}")  

    script_content = textwrap.dedent(f"""\
    Universe     = vanilla
    Executable   = {exe}
    Arguments    = -config={config} -cuts={cuts} {vaStage4Output}
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

    script_path = os.path.join(output_dir, f"{file_basename}.stg4.condor.sub")
    with open(script_path, "w") as script_file:
        script_file.write(script_content)
        return script_path
