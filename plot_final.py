# plot_final.py

# Imports
import os
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------------------------------------------------------------
data_dir = "DADOS/"
output_dir = "results/"

selected_csi = []
selected_parametrization = []
selected_B = []

data = []
min_b = 15
max_b = 17
min_csi = 10E-16
max_csi = 10E-7

show_plots = False
# ------------------------------------------------------------------------------------------------------------------
# Create output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


"""
Data format
{"parametrization": "", "B": "", "csi": "", "M": "", "R": "", "log_csi": "", max_M: "", max_R: ""}
"""

# ------------------------------------------------------------------------------------------------------------------
def read_folder_names(data_dir):
    folder_names = [name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]
    return folder_names

# ------------------------------------------------------------------------------------------------------------------
def getModel(folder_name):
    folder_name = folder_name.split("_")
#    print(folder_name[0], folder_name[1].split("B")[1])
    return folder_name[0], folder_name[1].split("B")[1]   # Return parametrization and B

# ------------------------------------------------------------------------------------------------------------------
def read_csi_values(data_dir):
    csi_list = []
    folder_names = [name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]
    return csi_list

# ------------------------------------------------------------------------------------------------------------------
def read_eos_data(data_dir):
    eos_data = []
    folder_names = [name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]
    return eos_data

# ------------------------------------------------------------------------------------------------------------------
def read_tov_data(data_dir):
    tov_data = []
    folder_names = [name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]
    return tov_data

# ------------------------------------------------------------------------------------------------------------------
def getData(model):
    global data
    parametrization, B = getModel(model)
    with open(f"{data_dir}/{model}/mr.dat", "r") as file:
        lines = file.readlines()[1:]
        for line in lines:
            line = line.split("\t")
            csi = line[0]
            max_m = float(line[1])
            max_r = float(line[2].split("\n")[0])   # Remove \n from string 
            data.append({"parametrization": parametrization, "B": B, "csi": csi, "max_m": max_m, "max_r": max_r, "log10csi": np.log10(float(csi))})

# ------------------------------------------------------------------------------------------------------------------
def plot_max_M_log_csi(data):
    plt.clf()
    # Filter data based on B and csi intervals.
    filtered_data = [d for d in data if min_b <= int(d["B"]) <= max_b and min_csi <= float(d["csi"]) <= max_csi]
    # Create a mapping of each unique B to a unique explicit color using only filtered data
    unique_B = sorted(list(set([d["B"] for d in filtered_data])))
    explicit_colors = ['red', 'lime', 'blue', 'violet']
    color_dict = {b: explicit_colors[i % len(explicit_colors)] for i, b in enumerate(unique_B)}
    
    # Plot each data point with appropriate marker and color
    for d in filtered_data:
        if d["parametrization"] == "GM1":
            marker = "o"  # Circle for GM1
        elif d["parametrization"] == "GM3":
            marker = "x"  # Cross for GM3
        else:
            marker = "s"  # Square for others
        plt.scatter(d["log10csi"], d["max_m"], marker=marker, color=color_dict[d["B"]],
                    label=f"{d['parametrization']} - B = $10^{{{d['B']}}} G$")
    
    plt.xlabel("$log_{10}(\\xi)$")
    plt.ylabel("$M_{max}$ $[M_{\\odot}]$")
    
    # Set xticks step of 1 by calculating the min and max of x data
    x_values = [d["log10csi"] for d in filtered_data]
    xmin = int(np.floor(min(x_values)))
    xmax = int(np.ceil(max(x_values)))
    plt.xticks(np.arange(xmin, xmax+1, 1))
    
    # Create custom legend entries for parametrization markers
    import matplotlib.lines as mlines
    param_legend_elements = [
        mlines.Line2D([], [], color='k', marker='o', linestyle='None', markersize=8, label='GM1'),
        mlines.Line2D([], [], color='k', marker='x', linestyle='None', markersize=8, label='GM3')
    ]
    
    # Create custom legend entries for unique B color mapping
    B_legend_elements = [
        mlines.Line2D([], [], color=color_dict[b], marker='s', linestyle='None', markersize=8, label=f'$B = 10^{{{b}}}G$')
        for b in unique_B
    ]
    
    # Move legends outside of the plot using bbox_to_anchor for positioning
    first_legend = plt.legend(handles=param_legend_elements, title="Parametrization", loc="upper left", bbox_to_anchor=(1.05, 1))
    plt.gca().add_artist(first_legend)
    plt.legend(handles=B_legend_elements, title="Color Mapping (B)", loc="upper left", bbox_to_anchor=(1.05, 0.7))
    
    plt.tight_layout()  # Adjust layout to accommodate the legends outside the plot
    plt.savefig(f"{output_dir}/max_M_log_csi.jpg", dpi=600)
    if show_plots: plt.show()

    # Separate plotting for GM1 and GM3
    for param in ['GM1', 'GM3']:
        plt.figure()
        param_data = [d for d in filtered_data if d['parametrization'] == param]
        if not param_data:
            continue
        unique_B_param = sorted(set(d["B"] for d in param_data))
        color_dict_param = {b: explicit_colors[i % len(explicit_colors)] for i, b in enumerate(unique_B_param)}
        marker = "o" if param == "GM1" else "x"
        for d in param_data:
            plt.scatter(d["log10csi"], d["max_m"], marker=marker, color=color_dict_param[d["B"]])
        plt.xlabel("$log_{10}(\\xi)$")
        plt.ylabel("$M_{max}$ $[M_{\\odot}]$")
        x_values = [d["log10csi"] for d in param_data]
        xmin = int(np.floor(min(x_values)))
        xmax = int(np.ceil(max(x_values)))
        plt.xticks(np.arange(xmin, xmax+1, 1))
        
        # Create custom legend entries for unique B color mapping (each B appears only once)
        import matplotlib.lines as mlines
        legend_handles = [
            mlines.Line2D([], [], color=color_dict_param[b], marker=marker, linestyle='None', markersize=8, label=f'$B = 10^{{{b}}}G$')
            for b in unique_B_param
        ]
        plt.legend(handles=legend_handles, loc="upper left", bbox_to_anchor=(1.05, 1))
        plt.title(f"Max Mass vs log(csi) for {param}")
        plt.tight_layout()
        plt.savefig(f"{output_dir}/max_M_log_csi_{param}.jpg", dpi=600)
        if show_plots: plt.show()

# ------------------------------------------------------------------------------------------------------------------
def plot_max_R_log_csi(data):
    plt.clf()
    # Filter data based on B and csi intervals.
    filtered_data = [d for d in data if min_b <= int(d["B"]) <= max_b and min_csi <= float(d["csi"]) <= max_csi]

    # Create a mapping of each unique B to a unique explicit color using only filtered data
    unique_B = sorted(list(set([d["B"] for d in filtered_data])))
    explicit_colors = ['red', 'lime', 'blue', 'violet']
    color_dict = {b: explicit_colors[i % len(explicit_colors)] for i, b in enumerate(unique_B)}
    
    # Plot each data point with appropriate marker and color
    for d in filtered_data:
        if d["parametrization"] == "GM1":
            marker = "o"  # Circle for GM1
        elif d["parametrization"] == "GM3":
            marker = "x"  # Cross for GM3
        else:
            marker = "s"  # Square for others
        plt.scatter(d["log10csi"], d["max_r"], marker=marker, color=color_dict[d["B"]],
                    label=f"{d['parametrization']} - B = $10^{{{d['B']}}} G$")
    
    plt.xlabel("$log_{10}(\\xi)$")
    plt.ylabel("$R_{max}$ $[km]$")
    
    # Set xticks step of 1 by calculating the min and max of x data
    x_values = [d["log10csi"] for d in filtered_data]
    xmin = int(np.floor(min(x_values)))
    xmax = int(np.ceil(max(x_values)))
    plt.xticks(np.arange(xmin, xmax+1, 1))
    
    # Create custom legend entries for parametrization markers
    import matplotlib.lines as mlines
    param_legend_elements = [
        mlines.Line2D([], [], color='k', marker='o', linestyle='None', markersize=8, label='GM1'),
        mlines.Line2D([], [], color='k', marker='x', linestyle='None', markersize=8, label='GM3')
    ]
    
    # Create custom legend entries for unique B color mapping
    B_legend_elements = [
        mlines.Line2D([], [], color=color_dict[b], marker='s', linestyle='None', markersize=8, label=f'$B = 10^{{{b}}}G$')
        for b in unique_B
    ]
    
    # Move legends outside of the plot using bbox_to_anchor for positioning
    first_legend = plt.legend(handles=param_legend_elements, title="Parametrization", loc="upper left", bbox_to_anchor=(1.05, 1))
    plt.gca().add_artist(first_legend)
    plt.legend(handles=B_legend_elements, title="Color Mapping (B)", loc="upper left", bbox_to_anchor=(1.05, 0.7))
    
    plt.tight_layout()  # Adjust layout to accommodate the legends outside the plot
    plt.savefig(f"{output_dir}/max_R_log_csi.jpg", dpi=600)
    if show_plots: plt.show()

    # Separate plotting for GM1 and GM3
    for param in ['GM1', 'GM3']:
        plt.figure()
        param_data = [d for d in filtered_data if d['parametrization'] == param]
        if not param_data:
            continue
        unique_B_param = sorted(set(d["B"] for d in param_data))
        color_dict_param = {b: explicit_colors[i % len(explicit_colors)] for i, b in enumerate(unique_B_param)}
        marker = "o" if param == "GM1" else "x"
        for d in param_data:
            plt.scatter(d["log10csi"], d["max_r"], marker=marker, color=color_dict_param[d["B"]])
        plt.xlabel("$log_{10}(\\xi)$ $[fm]$")
        plt.ylabel("$R_{max}$ $[km]$")
        x_values = [d["log10csi"] for d in param_data]
        xmin = int(np.floor(min(x_values)))
        xmax = int(np.ceil(max(x_values)))
        plt.xticks(np.arange(xmin, xmax+1, 1))
        
        # Create custom legend entries for unique B color mapping (each B appears only once)
        import matplotlib.lines as mlines
        legend_handles = [
            mlines.Line2D([], [], color=color_dict_param[b], marker=marker, linestyle='None', markersize=8, label=f'$B = 10^{{{b}}}G$')
            for b in unique_B_param
        ]
        plt.legend(handles=legend_handles, loc="upper left", bbox_to_anchor=(1.05, 1))
        plt.title(f"Max Radius vs log(csi) for {param}")
        plt.tight_layout()
        plt.savefig(f"{output_dir}/max_R_log_csi_{param}.jpg", dpi=600)
        if show_plots: plt.show()


# ------------------------------------------------------------------------------------------------------------------

def create_table(data):
    import csv
    # Filter data based on B and csi intervals.
    filtered_data = [d for d in data if min_b <= int(d["B"]) <= max_b and min_csi <= float(d["csi"]) <= max_csi]
    
    # Create a list of unique B and csi values
    unique_B = sorted(list(set([d["B"] for d in filtered_data])))
    unique_csi = sorted(list(set([d["csi"] for d in filtered_data])))
    
    # Create a table with max M and R for each csi/B combination
    table = []
    for d in filtered_data:
        table.append([d['parametrization'], d['csi'], d['B'], d['max_m'], d['max_r']])
            
    # Write the table to a CSV file
    with open(f"{output_dir}/max_M_R_table.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["model", "csi", "B", "max_m", "max_r"])
        writer.writerows(table)
# ------------------------------------------------------------------------------------------------------------------
def create_latex_table(data):
    # Filter data based on B and csi intervals.
    filtered_data = [d for d in data if min_b <= int(d["B"]) <= max_b and min_csi <= float(d["csi"]) <= max_csi]
    
    # Create a list of unique B and csi values
    unique_B = sorted(list(set([d["B"] for d in filtered_data])))
    unique_csi = sorted(list(set([d["csi"] for d in filtered_data])))
    
    # Create a LaTeX table
    latex_table = []
    latex_table.append("\\begin{tabular}{|c|c|c|c|}")
    latex_table.append("\\hline")
    latex_table.append("$\\xi$ & $B$ (G) & $M_{\\text{max}}$ ($M_{\\odot}$) & $R_{\\text{max}}$ (km) \\\\")
    latex_table.append("\\hline")
    
    # Group data by csi and B
    for csi in unique_csi:
        # Add csi value only once
        latex_table.append(f"{csi} & & & \\\\")
        for B in unique_B:
            # Find the data point for this csi and B
            point = next((d for d in filtered_data if d["csi"] == csi and d["B"] == B), None)
            if point:
                latex_table.append(f" & $10^{{{B}}}$ & {point['max_m']:.2f} & {point['max_r']:.2f} \\\\")
        latex_table.append("\\hline")
    
    latex_table.append("\\end{tabular}")
    
    # Write the LaTeX table to a .tex file
    with open(f"{output_dir}/optimized_max_M_R_table.tex", "w") as file:
        file.write("\n".join(latex_table))


# ------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    folders = read_folder_names(data_dir)               # Get all folders in the data directory (Parametrization, B)
    for folder in folders:
        getData(folder)                                  # Get data from folder
    plot_max_M_log_csi(data)                            # Plot max(M) x log(csi)
    plot_max_R_log_csi(data)                            # Plot max(R) x log(csi)
    create_table(data)                                  # Create table with max(M) and max(R) for each csi and B
    #create_latex_table(data)                            # Create LaTeX table with max(M) and max(R) for each csi and B
# ------------------------------------------------------------------------------------------------------------------