import os
from SCons.Script import DefaultEnvironment, ARGUMENTS

env = DefaultEnvironment()

PYTHON = os.environ.get("PYTHON", "python")

PrivateRepo="/Users_path/quantum-research-private"
SCRIPT_DEFAULT =f"{PrivateRepo}/src/sliding/cycles_analysis.py"
H_DEFAULT = f"{PrivateRepo}/examples/iH.mtx"
L_DEFAULT = f"{PrivateRepo}/examples/Lx0.mtx"

SCRIPT = ARGUMENTS.get("SCRIPT", SCRIPT_DEFAULT)
H = ARGUMENTS.get("H", H_DEFAULT)
L = ARGUMENTS.get("L", L_DEFAULT)

p = ARGUMENTS.get("p", "0.001")
M = ARGUMENTS.get("M", "5")
seed = ARGUMENTS.get("seed", "0")
max_cycles = ARGUMENTS.get("max_cycles", "100000")
weight_data = ARGUMENTS.get("weight_data", "1.0")
weight_meas = ARGUMENTS.get("weight_meas", "1.0")

#-----------------------------------------------
# save .txt output to res/ directory
#-----------------------------------------------
RES_DIR = os.path.join(os.getcwd(), "res")
os.makedirs(RES_DIR, exist_ok=True)

out_file = ARGUMENTS.get(
    "out", 
    os.path.join(RES_DIR, "t1_result.txt"))


cmd = (
    f'{PYTHON} {SCRIPT} '
    f'--H "{H}" --L "{L}" '
    f'--p {p} --M {M} --seed {seed} '
    f'--max_cycles {max_cycles} '
    f'--weight_data {weight_data} --weight_meas {weight_meas}'
)


env.AlwaysBuild(env.Alias("run", [], cmd))
env.AlwaysBuild(env.Alias("out", [], cmd + f' > "{out_file}"'))
