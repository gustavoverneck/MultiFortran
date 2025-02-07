import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------------------------------------------------------------
output_dir = "output"
params = []

with open(f"{output_dir}/params.txt") as f:
    for v in f.readlines():
        params.append(v.strip())

eos_data = []
tov_data = []
params_complete = []

for value in params:
    error_found = False
    temp_eos_data = []
    temp_tov_data = []
    try:
        with open(f"{output_dir}/{value}/eos.dat") as f:
            for l in f.readlines():
                l = l.strip().replace("d", "E")
                l = l.split()
                if len(l) == 3:
                    if l[0] == "-1.,":
                        break
                    temp_eos_data.append([float(l[1]), float(l[2])])  # e, p
                
        with open(f"{output_dir}/{value}/tov.out") as f:
            for l in f.readlines():
                l = l.strip().split()
                if len(l) >= 3:
                    temp_tov_data.append([float(l[1]), float(l[2])])  # m, r

    except Exception as e:
        error_found = True
        print(f"Problema encontrado para {value}. Ignorando-o. Erro: {e}")
    
    if not error_found:
        eos_data.append(temp_eos_data)
        tov_data.append(temp_tov_data)
        params_complete.append(value)

print(f"Total de parâmetros completos: {len(params_complete)}")

# ------------------------------------------------------------------------------------------------------------------
# Plotting EOS Data
plt.figure(figsize=(10, 6))
for index, param in enumerate(params_complete):
    e = [x[0] for x in eos_data[index]]
    p = [x[1] for x in eos_data[index]]
    plt.plot(e, p, label=f"{param}")

plt.xlabel("Energy Density (e)")
plt.ylabel("Pressure (p)")
plt.title("EOS Data")
plt.legend()
plt.savefig(f"{output_dir}/eos.jpg")
plt.clf()

# ------------------------------------------------------------------------------------------------------------------
# Plotting log-EOS Data
plt.figure(figsize=(10, 6))
for index, param in enumerate(params_complete):
    e = [x[0] for x in eos_data[index]]
    p = [x[1] for x in eos_data[index]]
    plt.plot(np.log(e), np.log(p), label=f"{param}")

plt.xlabel("log e")
plt.ylabel("log p")
plt.title("log EOS Data")
plt.legend()
plt.savefig(f"{output_dir}/log_eos.jpg")
plt.clf()

# ------------------------------------------------------------------------------------------------------------------
# Plotting TOV Data
plt.figure(figsize=(10, 6))
for index, param in enumerate(params_complete):
    r = [x[0] for x in tov_data[index]]
    m = [x[1] for x in tov_data[index]]
    plt.plot(m, r, label=f"{param}")

plt.ylabel("Mass (m)")
plt.xlabel("Radius (r)")
plt.title("TOV Data")
plt.legend()
plt.savefig(f"{output_dir}/tov.jpg")
