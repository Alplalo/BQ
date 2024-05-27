# Crear PEM (Potencial electrostatico molecular) a partir del .top y .crd

import numpy as np
from numba import jit


# Leer chignolin.top para obtener nombres de atomos y cargas usando %FLAG ATOM_NAME y %FLAG CHARGE
def read_top(top_file):
    with open(top_file, 'r') as f:
        lines = f.readlines()
    atom_name = []
    charge = []
    for i in range(len(lines)):
        if lines[i].strip() == "%FLAG ATOM_NAME":
            for j in range(i+2, len(lines)):
                if lines[j].strip() == "%FLAG CHARGE":
                    break
                fila_atom_name = lines[j].split()
                for atom in fila_atom_name:
                    atom_name.append(atom)
        if lines[i].strip() == "%FLAG CHARGE":
            for j in range(i+2, len(lines)):
                if lines[j].strip() == "%FLAG ATOMIC_NUMBER":
                    break
                charges = lines[j].strip().split()
                for c in charges:
                    charge.append(float(c))
    return atom_name, charge

# Hay 6 columnas en el archivo crd, las primeras 3 son las coordenadas x,y,z de un atomo y las otras 3 del siguiente atomo.
def read_crd(crd_file):
    with open(crd_file, 'r') as f:
        lines = f.readlines()
    x = []
    y = []
    z = []
    lines = lines[2:]
    for i in range(len(lines)-1):
        if lines[i].strip() == "":
            break
        fila = lines[i].split()
        if len(fila) == 6:
            x.append(float(fila[0]))
            y.append(float(fila[1]))
            z.append(float(fila[2]))
            x.append(float(fila[3]))
            y.append(float(fila[4]))
            z.append(float(fila[5]))
        else:
            x.append(float(fila[0]))
            y.append(float(fila[1]))
            z.append(float(fila[2]))
    return x, y, z


# Crear archivo con nombres de atomos y cargas, 2 columnas
def write_atom_charge(atom_name, charge,x,y,z, output_file):
    factor = 1
    with open(output_file, 'w') as f:
        for i in range(len(atom_name)):
            f.write(atom_name[i] + ' ' + str(x[i]) + ' ' + str(y[i]) + ' ' + str(z[i]) + ' ' + str(charge[i]/factor) + '\n')

# Superficie de Potencial electrostatico molecular los primeros 148 atomos, aplicar una malla en el espacio de los atomos y calcular el potencial electrostatico en cada punto de la malla.
def PEM(atom_name, charge, x, y, z):
    N = 148
    factor = 18.2223
    x = x[:N]
    y = y[:N]
    z = z[:N]
    extra = 5
    distancia_malla = 0.1
    charge = charge[:N]
    xmin = min(x)
    ymin = min(y)
    zmin = min(z)
    xmax = max(x)
    ymax = max(y)
    zmax = max(z)
    # El minimo es el minimo de los 3 minimos
    min_total = min(xmin, ymin, zmin)
    max_total = max(xmax, ymax, zmax)
    min_total -= extra
    max_total += extra
    x_range = np.arange(min_total, max_total, distancia_malla)
    y_range = np.arange(min_total, max_total, distancia_malla)
    z_range = np.arange(min_total, max_total, distancia_malla)
    PEM = np.zeros((len(x_range), len(y_range), len(z_range)))
    for i in range(len(x_range)):
        for j in range(len(y_range)):
            for k in range(len(z_range)):
                for l in range(N):
                    r = np.sqrt((x_range[i]-x[l])**2 + (y_range[j]-y[l])**2 + (z_range[k]-z[l])**2)
                    PEM[i,j,k] += charge[l]*factor/r

    # Buscar los 2 minimos de PEM
    min1 = np.min(PEM)
    min1_index = np.where(PEM == min1)
    PEM[min1_index] = 1000
    # Subir el minimo a 1000 y los de alrededor a 1000
    rango1 = 8
    rango2 = -8
    for i in range(rango2,rango1):
        for j in range(rango2,rango1):
            for k in range(rango2,rango1):
                PEM[min1_index[0][0]+i, min1_index[1][0]+j, min1_index[2][0]+k] = 1000

    min2 = np.min(PEM)
    min2_index = np.where(PEM == min2)
    PEM[min1_index] = min1

    # Coordenadas de los 2 minimos
    x_min1 = x_range[min1_index[0][0]]
    y_min1 = y_range[min1_index[1][0]]
    z_min1 = z_range[min1_index[2][0]]
    x_min2 = x_range[min2_index[0][0]]
    y_min2 = y_range[min2_index[1][0]]
    z_min2 = z_range[min2_index[2][0]]
    print('Minimo 1:', x_min1, y_min1, z_min1)
    print('Minimo 2:', x_min2, y_min2, z_min2)
    return PEM, x_range, y_range, z_range, min1, min2, min1_index, min2_index

# Escribir minimos
def write_min(min1, min2, output_file):
    with open(output_file, 'w') as f:
        f.write('Minimo 1: ' + str(min1) + '\n')
        f.write('Minimo 2: ' + str(min2) + '\n')


atom_name,charge = read_top('chignolin.top')
x, y, z = read_crd('chignolin.crd')
print(len(atom_name), len(charge), len(x), len(y), len(z))
write_atom_charge(atom_name, charge,x,y,z, 'atom_charge.txt')
PEM,x_range,y_range,z_range,min1,min2,min1_index,min2_index = PEM(atom_name, charge, x, y, z)
write_min(min1, min2, 'minimos.txt')



# Dibujar los 2 minimos de PEM alrededor de los 148 primeros atomos

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# x = x[:148]
# y = y[:148]
# z = z[:148]
# ax.scatter(x, y, z, c='r', marker='o')
# ax.scatter(x_range[min1_index[0][0]], y_range[min1_index[1][0]], z_range[min1_index[2][0]], c='b', marker='o')
# ax.scatter(x_range[min2_index[0][0]], y_range[min2_index[1][0]], z_range[min2_index[2][0]], c='g', marker='o')
# plt.show()



