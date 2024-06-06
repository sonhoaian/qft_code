#this func is to fit the curl to get the desity distribution

import numpy as np
import lhapdf
from scipy.interpolate import CubicSpline
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


pdf = lhapdf.mkPDF("cteq61", 0)


x_values = np.linspace(0.0e-10, 1, 1000)


Q2 = 10


u_pdf_values = np.array([pdf.xfxQ2(2, x, Q2) for x in x_values])


x_values = x_values[np.isfinite(u_pdf_values)]
u_pdf_values = u_pdf_values[np.isfinite(u_pdf_values)]



interp_u_pdf = CubicSpline(x_values, u_pdf_values)


x_interp = np.linspace(0.0e-10, 1, 1000)


u_pdf_interp = interp_u_pdf(x_interp)


def polynomial_func(x, *coefficients):
    return sum(coefficients[i] * x**i for i in range(len(coefficients)))


def fit_polynomial(degree):
    popt, _ = curve_fit(polynomial_func, x_interp, u_pdf_interp, maxfev=100000, p0=np.ones(degree + 1))
    return popt


degree = 13 # Change the degree as needed
coefficients = fit_polynomial(degree)
print(f"Coefficients of the fitted polynomial (Degree {degree}):")
for i, coef in enumerate(coefficients):
    print(f"coefficient_{i} =", coef)


plt.figure(figsize=(10, 6))
plt.plot(x_values, u_pdf_values , label='PDF')
plt.plot(x_interp, u_pdf_interp, label='Interpolated PDF')
plt.plot(x_interp, polynomial_func(x_interp, *fit_polynomial(degree)), label=f'Fitted Polynomial (Degree {degree})', linestyle='--')
plt.xlabel('x')
plt.ylabel('PDF')
plt.title('Interpolated Parton Distribution Function (PDF) for u quark with Fitted Polynomial')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.legend()
plt.grid(True)
plt.show()


