# DINAMICA MOLECULAR CON AMBER

## Índice

- [LEaP](#leap)
- [Minimización](#minimización)
- [Heating](#heating)
- [Descripción Flags AMBER](#DescripciónFlagsAMBER)

## LEaP

### Descripción

LEaP es una herramienta utilizada para la preparación de sistemas moleculares en dinámica molecular dentro del entorno de AMBER. Permite construir sistemas, anñadir solvente e iones, y generar los archivos necesarios para simulaciones.

### Uso

#### Funciones Principales

- **`source`**: Comando para cargar campos de fuerza o librerías necesarias para definir los parámetros del sistema.   
    - Ejemplo:`source leaprc.protein.ff14SB`

- **Cargar parámetros externos**: Si añades moleculas no estándar o parametrizadas, es necesario cargar sus parámetros.  
    - Ejemplo: `loadAmberParms ligand.frcmod` / `loadoff ligand.lib`

- **crear objeto**:
  - Se puede crear un objeto con una secuencia específica (No muy usado debido a que no defines estructura 3D) `peptide = sequence{NGLY TYR ASP PRO GLU THR MET THR TRP CGLY}`.
  - También se puede crear leyendo un archivo PDB `peptide = loadPdb chinolindo.pdb`.

- **`solvatebox`**: Solvata el sistema en una caja con aguas.  
    - Ejemplo:`solvateBox peptide TIP3PBOX 15.0` (15.0 Amstrongs es la distancia mínima que definimos entre la proteína y el borde de la caja)

- **`charge`**: Calcula la carga actual del sistema.
    - Ejemplo: `charge peptide`

- **`addIons`**: Añade iones al sistema. La opción 0 permite que el programa calcule cuántos iones son necesarios para neutralizar la carga total del sistema.  
    - Ejemplo: `addIons peptide Na+ 0`

- **`check`**: Verifica que el sistema esté bien (átomos que falten, enlaces, ...)

- **`saveamberparm`**: Genera archivos de topología y coordenadas.  
    - Ejemplo: `saveAmberParm peptide system.prmtop system.inpcrd`

- **`savePdb`**: Genera el sistema en formato PDB.
    - Ejemplo: `savePdb peptide system.pdb`

- **`quit`**: Detiene la ejecución del programa.

## Visualización del sistema

Es recomendable visualizar el sistema antes de avanzar con los siguientes pasos para estar seguro de que no se ha producido algun error en la creación del sistema.

Programas para visualizar:  
    - VMD  
    - Pymol  
    - ChimeraX  

## Minimización

### Descripción

Minimizar es el primer paso tras montar el sistema. El objetivo de la minimización es eliminar contactos estéricos desfavorables y reducir los gradientes de fuerzas que pueden provocar inestabilidad o roturas en la simulación.

En sistemas grandes es recomendable hacer la minimización por etapas.

  1. Relajar hidrógenos
  2. Relajar solvente
  3. Relajar todo el sistema

### Uso

Ejemplo etapa final minimización:
```bash
Minimización general
&cntrl
  imin=1,
  maxcyc=10000,
  ncyc=2000,
  cut=10.0,
  ntb=1,
/
```

#### Etapas

```bash
#
# Minimizacion de hidrogenos de la proteina
#
&cntrl
  imin=1, maxcyc=10000, ncyc=2000,
  drms=0.001, ntb=1, ntp=0, cut=10.0,
  ibelly=1,
  bellymask=':1-948&@H=',
&end

```
```bash
#
# Minimizacion de aguas
#
&cntrl
  imin=1, maxcyc=10000, ncyc=2000,
  drms=0.01, ntb=1, ntp=0, cut=10.0,
  ibelly=1,
  bellymask=':1133-39905',
&end
```
```bash
#
# Minimizacion del sistema
#
&cntrl
  imin=1, maxcyc=5000, ncyc=4000,
  drms=0.01, ntb=1, ntp=0, cut=10.0,
&end
```

## Heating

### Descripción

El heating consiste en aumentar gradualmente la temperatura del sistema de 0K hasta la temperatura objetivo, normalmente 300K, evitando cambios bruscos que puedan desestabilizar la simulación.

### Uso

Ejemplo heating:

``` bash 
Heating de 0 a 300K
&cntrl
  imin=0, ntx=1, irest=0,
  nstlim=50000, dt=0.002,

  ntc=2, ntf=2,
  cut=10.0,

  ntb=1,
  ntt=3, gamma_ln=1.0,

  tempi=0.0, temp0=300.0,

  ntpr=500, ntwx=500,
  nmropt=1,
/
&wt type='TEMP0', istep1=0, istep2=50000, value1=0.0, value2=300.0 /
&wt type='END' /

```

- Para definir el incremento de la temperatura en la dinámica:

``` bash
&wt type='TEMP0', istep1=0, istep2=50000, value1=0.0, value2=300.0 /
&wt type='END' /
```
Modifica el valor de temp0 de un valor inicial (value1) a uno final (value2) entre un step inicial (istep1) y uno final (istep2).

## Density

### Descripción

En esta fase, el sistema se simula a presión constante (NTP) para permitir que el volumen de la caja se ajuste y alcance una densidad realista (Densidad del agua). 
Esto se hace porque el sistema puede tener burbujas debido a que en el LEaP se eliminan las aguas muy cercanas y que podrŕin chocar con la proteína.

### Uso

Ejemplo desnsity:

```bash
Equilibración de densidad
&cntrl
  imin=0, ntx=5, irest=1,
  nstlim=50000, dt=0.002,

  ntc=2, ntf=2,
  cut=10.0,

  ntb=2, ntp=1,
  taup=2.0,

  ntt=3, gamma_ln=1.0,
  temp0=300.0,

  ntpr=500, ntwx=500,
/
```

## Producción

### Descripción

La fase de producción es donde corremos ya nuestro sistema equilibrado y con el que posteriormente obtendremos toos los datos relevantes para el análisis.

### Uso

Ejemplo producción:

```bash
Producción MD
&cntrl
  imin=0, ntx=5, irest=1,
  nstlim=5000000, dt=0.002,

  ntc=2, ntf=2,
  cut=10.0,

  ntb=1,

  ntt=3, gamma_ln=1.0,
  temp0=300.0,

  ntpr=5000, ntwx=5000, ntwr=50000,
/
```

## Descripción Flags AMBER

- **`imin`**: = 1 (Activa el modo minimización), = 0 (Activa el modo dinámica).

- **`maxcyc`**: Número total de pasos de minimización.

- **`ncyc`**: Número de pasos usando Steepest Descent. El resto hasta llegar al maxcyc será usando Conjugate Gradient.

- **`cut`**: Cutoff de interacciones entre atomos no enlazados (Amstrongs).

- **`ntx`**: = 1 (inicia desde estructura, sin velocidades).

- **`irest`**: = 0 (no es continuacion de otra dinámica).

- **`ntb`**: = 1 (Volumen constante), = 2 (Presión constante).

- **`ntp`**: = 1 (Control de presión isotrópico, la caja escala igual en todas las direcciones).

- **`nstlim`**: Número de pasos de la dinámica.

- **`dt`**: Paso de integración (ps).

- **`ntc=2` / `ntf=2`**: Constriñe enlaces con H / No calcula fuerzas en esos enlaces (SHAKE).

- **`ntt`**: Control de temperatura (Termostato).
  - = 3 Langevin  

- **`gamma_ln`**: Coeficiente de fricción.

- **`tempi` / `temp0`**: Temperatura inicial / Temperatura del termostato (a la que tendirá el sistema).

- **`taup`**: Tiempo de relajación de la presión.
  



by [Albert Plazas](https://github.com/Alplalo)
