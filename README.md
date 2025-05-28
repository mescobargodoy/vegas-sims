This repository contains simple python functions to submit VEGAS jobs to condor queue. You need VEGAS installed.
The purpose of this repository is to keep track of the methods used to process simulation files in order
to assess the reconstruction of the depth of first interaction using the Image Template Method.
Only useful in the vhe cluster at UCSC.

Simulation files can be found here `/data_disks/vhe1a/mc/CARE_V6_05Wobble/`.

Now on to submitting VEGAS jobs to condor queue. A simple test to try in a python terminal:

```
from vaStage1 import create_vaStage1_condor_script
from CondorSubmit import submit_vaStage1, submit_vaStage2, submit_vaStage4

output_dir = "/home/vhep/mescob11/VERITAS/VEGAS_sims_commands/test"
vbf = "/data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen20deg_05wob_200MHz_1.vbf"
laser = "/data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/vegas_outputs/laser/simLaser.root" 

vaStage2Ouput = "/home/vhep/mescob11/VERITAS/VEGAS_sims_commands/test/gamma_V6_CARE_v1.6.2_12_ATM61_zen0deg_05wob_200MHz_1.stg2.root"

config = "/home/vhep/mescob11/VERITAS/VEGAS_sims_commands/vastage4_config.txt"
cuts = "/home/vhep/mescob11/VERITAS/VEGAS_sims_commands/vastage4_cuts.txt"

create_vaStage1_condor_script(vbf, output_dir)  # creates a condor script
submit_vaStage1(vbf, output_dir)                # creates and submitsi a condor script
```
Once you are done with VEGAS stage 1 you can proceed to stage2.

```
submit_vaStage2(vbf, laser, output_dir)
```

And once this is done you can proceed to stage 4:

```
submit_vaStage4(vaStage2Ouput, config, cuts, output_dir)
```


To submit multiple jobs you can do something like this:

```
from CondorSubmit import submit_vaStage1, submit_vaStage2, submit_vaStage4

output_dir = "/data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/vegas_outputs/with_gt_factors/stage2"
laser = "/data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/vegas_outputs/laser/simLaser.root" 

files = [
    "/data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen0deg_05wob_200MHz_1.vbf",
    "/data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen20deg_05wob_200MHz_1.vbf",
    "/data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen30deg_05wob_200MHz_1.vbf",
    "/data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen35deg_05wob_200MHz_1.vbf",
    "/data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen40deg_05wob_200MHz_1.vbf",
    "/data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen45deg_05wob_200MHz_1.vbf",
    "/data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen50deg_05wob_200MHz_1.vbf",
    "/data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen55deg_05wob_200MHz_1.vbf",
    "/data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen60deg_05wob_200MHz_1.vbf"
]

for file in files:
    submit_vaStage1(file, output_dir)

```

Once the VEGAS stage 1 is done you can do:

```
for file in files:
    submit_vaStage2(file, laser, output_dir, S_factors="1/0.742,2/0.665,3/0.735,4/0.701")

```

And once VEGAS stage 2 is done you can do:
```
config = "/home/vhep/mescob11/VERITAS/VEGAS_sims_commands/vastage4_config.txt"
cuts = "/home/vhep/mescob11/VERITAS/VEGAS_sims_commands/vastage4_cuts.txt"
output_dir = "/data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/vegas_outputs/with_gt_factors/stage4"

stg2_files = [
    "/data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/vegas_outputs/with_gt_factors/stage2/gamma_V6_CARE_v1.6.2_12_ATM61_zen0deg_05wob_200MHz_1.stg2.root",
    "/data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/vegas_outputs/with_gt_factors/stage2/gamma_V6_CARE_v1.6.2_12_ATM61_zen20deg_05wob_200MHz_1.stg2.root",
    "/data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/vegas_outputs/with_gt_factors/stage2/gamma_V6_CARE_v1.6.2_12_ATM61_zen30deg_05wob_200MHz_1.stg2.root",
    "/data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/vegas_outputs/with_gt_factors/stage2/gamma_V6_CARE_v1.6.2_12_ATM61_zen35deg_05wob_200MHz_1.stg2.root",
    "/data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/vegas_outputs/with_gt_factors/stage2/gamma_V6_CARE_v1.6.2_12_ATM61_zen40deg_05wob_200MHz_1.stg2.root",
    "/data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/vegas_outputs/with_gt_factors/stage2/gamma_V6_CARE_v1.6.2_12_ATM61_zen45deg_05wob_200MHz_1.stg2.root",
    "/data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/vegas_outputs/with_gt_factors/stage2/gamma_V6_CARE_v1.6.2_12_ATM61_zen50deg_05wob_200MHz_1.stg2.root",
    "/data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/vegas_outputs/with_gt_factors/stage2/gamma_V6_CARE_v1.6.2_12_ATM61_zen55deg_05wob_200MHz_1.stg2.root",
    "/data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/vegas_outputs/with_gt_factors/stage2/gamma_V6_CARE_v1.6.2_12_ATM61_zen60deg_05wob_200MHz_1.stg2.root"
]


for vaStage2Output in stg2_files:
    submit_vaStage4(vaStage2Output, config, cuts, output_dir)
```


To extract the depth of first interaction truth you need the VBF libraries compiled. I created an extra file to extract the first interaction depth truth of all events in a VBF file.
`/home/vhep/mescob11/VERITAS/InspectingVBF/examples/PrintAllCorsikaSimulationData.cpp`

Try running the following in the terminal first to get the first interaction depth truth:

```
./PrintAllCorsikaSimulationData /data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen0deg_05wob_200MHz_1.vbf  > /data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/first_interaction_truth_h5/gamma_V6_CARE_v1.6.2_12_ATM61_zen0deg_05wob_200MHz_1.dat

./PrintAllCorsikaSimulationData /data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen20deg_05wob_200MHz_1.vbf  > /data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/first_interaction_truth_h5/gamma_V6_CARE_v1.6.2_12_ATM61_zen20deg_05wob_200MHz_1.dat

./PrintAllCorsikaSimulationData /data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen30deg_05wob_200MHz_1.vbf  > /data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/first_interaction_truth_h5/gamma_V6_CARE_v1.6.2_12_ATM61_zen30deg_05wob_200MHz_1.dat

./PrintAllCorsikaSimulationData /data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen35deg_05wob_200MHz_1.vbf  > /data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/first_interaction_truth_h5/gamma_V6_CARE_v1.6.2_12_ATM61_zen35deg_05wob_200MHz_1.dat

./PrintAllCorsikaSimulationData /data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen40deg_05wob_200MHz_1.vbf  > /data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/first_interaction_truth_h5/gamma_V6_CARE_v1.6.2_12_ATM61_zen40deg_05wob_200MHz_1.dat

./PrintAllCorsikaSimulationData /data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen45deg_05wob_200MHz_1.vbf  > /data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/first_interaction_truth_h5/gamma_V6_CARE_v1.6.2_12_ATM61_zen45deg_05wob_200MHz_1.dat

./PrintAllCorsikaSimulationData /data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen50deg_05wob_200MHz_1.vbf  > /data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/first_interaction_truth_h5/gamma_V6_CARE_v1.6.2_12_ATM61_zen50deg_05wob_200MHz_1.dat

./PrintAllCorsikaSimulationData /data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen55deg_05wob_200MHz_1.vbf  > /data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/first_interaction_truth_h5/gamma_V6_CARE_v1.6.2_12_ATM61_zen55deg_05wob_200MHz_1.dat

./PrintAllCorsikaSimulationData /data_disks/vhe1a/mc/CARE_V6_05Wobble/SHV/ATM61/gamma_V6_CARE_v1.6.2_12_ATM61_zen60deg_05wob_200MHz_1.vbf  > /data_disks/vhe1a/mescob11/VERITAS/FirstInteractionSims/first_interaction_truth_h5/gamma_V6_CARE_v1.6.2_12_ATM61_zen60deg_05wob_200MHz_1.dat

```