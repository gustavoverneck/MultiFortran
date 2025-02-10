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
plt.savefig(f"{output_dir}/eos.jpg", dpi=600)
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
plt.savefig(f"{output_dir}/log_eos.jpg", dpi=600)
plt.clf()

# ------------------------------------------------------------------------------------------------------------------
# Plotting TOV Data
plt.figure(figsize=(10, 6))
for index, param in enumerate(params_complete):
    m = [x[0] for x in tov_data[index]]
    r = [x[1] for x in tov_data[index]]
    plt.plot(r, m, label=f"{param}")

plt.xlabel("Mass (m)")
plt.ylabel("Radius (r)")
plt.title("TOV Data")
plt.legend()
plt.savefig(f"{output_dir}/tov.jpg", dpi=600)


# Plotando Max(M) x log(csi)
max_m = []
max_r = []
log_csi = []
csi_list = []

for index, p in enumerate(params_complete):
    p = p.replace("d", "E")
    try:
        csi = float(p)
    except ValueError:
        print(f"Não foi possível converter o parâmetro {p} para float. Ignorando-o.")
        continue

    if csi <= 0:
        print(f"O parâmetro {p} converteu para um valor não positivo. Ignorando-o.")
        continue

    m_values = [x[0] for x in tov_data[index]]
    r_values = [x[1] for x in tov_data[index]]
    if not m_values:
        continue

    max_m.append(max(m_values))
    max_r.append(r_values[m_values.index(max(m_values))])
    csi_list.append(csi)
    log_csi.append(np.log10(csi))

# Aumentando a resolução do gráfico utilizando dpi e formatadores de ticks com maior precisão.
plt.figure(figsize=(10, 6), dpi=600)
plt.plot(log_csi, max_m, 'o', markersize=4, label='Max(M) vs log(csi)')
plt.ylim(min(max_m) - 1E-3, max(max_m) + 1E-3)
plt.xlabel("log(csi)", fontsize=12)
plt.ylabel("Max(M)", fontsize=12)
plt.title("Gráfico de Max(M) x log(csi)", fontsize=14)
plt.legend()

ax = plt.gca()
ax.minorticks_on()
import matplotlib.ticker as ticker
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.6f'))
plt.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)

plt.savefig(f"{output_dir}/max_M_log_csi.jpg", dpi=600)
plt.clf()

# Aumentando a resolução do gráfico utilizando dpi e formatadores de ticks com maior precisão.
plt.figure(figsize=(10, 6), dpi=600)
plt.plot(log_csi, max_r, 'o', markersize=4, label='Max(M) vs log(csi)')
plt.ylim(min(max_r) - 1E-2, max(max_r) + 1E-2)
plt.xlabel("log(csi)", fontsize=12)
plt.ylabel("Max(r)", fontsize=12)
plt.title("Gráfico de Max(r) x log(csi)", fontsize=14)
plt.legend()

ax = plt.gca()
ax.minorticks_on()
import matplotlib.ticker as ticker
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.6f'))
plt.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)

plt.savefig(f"{output_dir}/max_R_log_csi.jpg", dpi=600)
plt.clf()


# output data in file
with open("output/mr.dat", "w") as f:
    f.write("csi\tm_max\tr_max\n")
    for line in range(len(max_m)):
        f.write(f"{csi_list[line]}\t{max_m[line]}\t{max_r[line]}\n")