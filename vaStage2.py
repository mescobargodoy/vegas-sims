import os
import warnings
import textwrap
import errno


def create_vaStage2_condor_script(
        vbf,
        laser,  
        output_dir=".", 
        S_factors="1/0.684,2/0.654,3/0.751,4/0.728"
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
    S_factors : str, optional
        vector-like (as in C/C++) specifying charge correction factor (GT factors)
        defaults to 2023/2024 winter value

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
    Arguments    = -G_SimulationMode=1 -G_NumEventsToAnalyse=100000 -BCI_BadChannelList=/veritas_data/mc/badPixels/V6_BadChannel.txt -S2A_ScaleCharge={S_factors} {vbf} {vaStage2Output} {laser}
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
