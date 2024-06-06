import numpy as np
import matplotlib.pyplot as plt
import lhapdf
from concurrent.futures import ProcessPoolExecutor

pdf = lhapdf.mkPDF("cteq61", 0)

# Define range of x values
x_values = np.linspace(0.01, 1.0, 1000)
Q2 = 100.0 
s = 1.96e6  # Based on LHC report in 2021 GeV^2 (for LHC, s = (14 TeV)^2)

# Extract PDFs for u and ubar quarks at given Q^2
ubar_pdf = np.array([pdf.xfxQ2(-2, x, Q2) for x in x_values])  #
u_pdf = np.array([pdf.xfxQ2(2, x, Q2) for x in x_values])

# Strong coupling constant
alpha_s = 0.118

# gluon mass to avoid devide by zero
m_g = 0.00001

# partonic cross-section for u + ubar -> u + ubar in the t-channel
def partonic_cross_section(x1, x2):
    hat_s = x1 * x2 * s
    t_min = -hat_s + 2 * m_g ** 2
    t_max = -m_g ** 2  # Avoid t = 0 for stability
    integral = 0
    num_points = 1000
    #calculate integra
    for t in np.linspace(t_min, t_max, num_points):
        if t != 0:
            d_sigma_dt = (4 * np.pi * alpha_s ** 2) / (hat_s ** 2) * (1 / (t - m_g ** 2) ** 2)
            integral += d_sigma_dt
    integral *= (t_max - t_min) / num_points
    return integral

# calculate pair product
def process_pair(x1, x2, i, j):
    pdf_product = u_pdf[i] * ubar_pdf[j]
    partonic_cs = partonic_cross_section(x1, x2)
    return pdf_product * partonic_cs

# Manage chunk_size 
def process_chunk(chunk, max_workers):
    cross_section = 0.0
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_pair, x1, x2, i, j) for x1, x2, i, j in chunk]
        for future in futures:
            cross_section += future.result()
    return cross_section

# impleteting of cross section calculate
def calculate_cross_section(x_values, max_workers, chunk_size):
    cross_section = 0.0
    x_len = len(x_values)

    # Create chunks of (x1, x2) pairs
    chunks = []
    for i, x1 in enumerate(x_values):
        for j, x2 in enumerate(x_values):
            chunks.append((x1, x2, i, j))
            if len(chunks) >= chunk_size:
                cross_section += process_chunk(chunks, max_workers)
                chunks = []

    if chunks:
        cross_section += process_chunk(chunks, max_workers)
    
    cross_section *= (x_values[1] - x_values[0]) ** 2
    return cross_section

# Limit the number of concurrent processes
max_workers = 3  # set threads
chunk_size = 1000 #limited RAM use

# summiting crassection
cross_section = calculate_cross_section(x_values, max_workers, chunk_size)
print(f"Scattering cross-section: {cross_section:.3e} pb")

# Plot the resulting PDF (optional)
plt.plot(x_values, ubar_pdf * u_pdf, label=r"$\bar{u} \times u$ PDF")
plt.xlabel('x')
plt.ylabel('PDF')
plt.title(r'PDF for $\bar{u} \times u$ in proton-proton scattering (CTEQ61)')
plt.legend()
plt.grid(True)
plt.show()
