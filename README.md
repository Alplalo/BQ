# DINÁMICA MOLECULAR CON AMBER

## Índice

- [LEaP](#leap)
- [Minimización](#minimización)
- [Heating](#heating)
- [Producción](#producción)
- [Descripción Flags AMBER](#descripción-flags-amber)

## LEaP

### Descripción

LEaP es una herramienta para la preparación de sistemas moleculares en dinámica molecular dentro del entorno de AMBER. Permite construir sistemas, anñadir solvente e iones, y generar los archivos necesarios para la simulación.

### Uso

```bash
# 1. Cargar campos de fuerza (Proteína y Agua)
source leaprc.protein.ff14SB
source leaprc.water.tip3p

# 2. Cargar parámetros del ligando
loadAmberParams ligando.frcmod
loadoff ligando.lib

# 3. Cargar la estructura del complejo
complejo = loadPdb complejo_inicial.pdb

# 4. Verificar carga inicial y enlaces
check complejo
charge complejo

# 5. Solvatación
solvateBox complejo TIP3PBOX 12.0

# 6. Neutralización
# Añadimos iones para neutralizar
addIons complejo Na+ 0
addIons complejo Cl- 0

# 7. Verificación final y guardado
check complejo
savePdb complejo sistema_final.pdb
saveAmberParm complejo sistema_final.prmtop sistema_final.inpcrd

# 8. Salir
quit
```

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

> Nota rápida:
> - **Minimización**: normalmente con `sander`.
> - **Heating/Equilibración/Producción**: normalmente con `pmemd.cuda`.

### 1) Modo de ejecución (minimización vs dinámica)

- **`imin`**
  - `imin=1`: minimización de energía
  - `imin=0`: dinámica molecular (MD)

- **`maxcyc`** (minimización)
  - Pasos totales de minimización.

- **`ncyc`** (minimización)
  - Pasos con *Steepest Descent*, el resto hasta `maxcyc` con *Conjugate Gradient*.

- **`ntmin`** (minimización, opcional)
  - Selecciona el método de minimización (si no lo pones, AMBER usa el default).

- **`drms`** (minimización)
  - Criterio de convergencia (RMS del gradiente). Si se alcanza antes de `maxcyc`, se para.


### 2) Reinicios: cómo empezar vs cómo continuar

- **`ntx`** + **`irest`**
  - **Nueva simulación (sin velocidades)**:
    - `ntx=1, irest=0`
  - **Continuación desde restart (con velocidades)**:
    - `ntx=5, irest=1`

> Regla práctica:
> - Si sales de *minimización* → *heating*: `ntx=1, irest=0` (porque vienes de coordenadas sin velocidades).
> - Si sales de *heating/density/producción* → siguiente etapa: `ntx=5, irest=1`.


### 3) Tiempo, integración y constraints

- **`nstlim`**
  - Número de pasos de MD.

- **`dt`**
  - Paso de integración (ps).
  - Típico con SHAKE en H: `dt=0.002` (2 fs).

- **`ntc`** / **`ntf`**
  - Controlan constraints (SHAKE) y cálculo de fuerzas en enlaces a H.
  - Caso típico:
    - `ntc=2, ntf=2` → constraints en enlaces con H y no se calculan fuerzas en esos enlaces.

- **`tol`** (opcional)
  - Tolerancia de SHAKE.


### 4) No enlazadas y PME (explícito)

- **`cut`**
  - Cutoff (Å) para interacciones no enlazadas de corto alcance.
  - Valores típicos: `8.0` o `10.0` Å.

> En explícito con AMBER, PME suele estar activo/gestionado para electrostática de largo alcance
> (dependiendo del engine/condiciones); `cut` sigue siendo relevante para la parte directa/VDW.


### 5) Condiciones periódicas / volumen / presión (NVT vs NPT)

- **`ntb`**
  - `ntb=1`: volumen constante (NVT; PBC activas)
  - `ntb=2`: permite cambio de volumen (necesario para NPT)

- **`ntp`** (solo si `ntb=2`)
  - `ntp=0`: sin control de presión (no NPT)
  - `ntp=1`: presión isotrópica (la caja escala igual en todas las direcciones)

- **`pres0`** (NPT, opcional)
  - Presión objetivo (por defecto 1 atm).
  - Ejemplo: `pres0=1.0`

- **`taup`** (NPT)
  - Tiempo de acoplamiento de la presión (ps). Normalmente: `taup=1.0` a `2.0`.


### 6) Control de temperatura (termostato)

- **`ntt`**
  - `ntt=3`: Langevin (mas usado en `pmemd.cuda`)

- **`gamma_ln`** (solo si `ntt=3`)
  - Coeficiente de fricción (1/ps). Normalmente: `gamma_ln=1.0`.

- **`tempi`** / **`temp0`**
  - `tempi`: temperatura inicial (K)
  - `temp0`: temperatura objetivo del termostato (K)


### 7) Outputs

- **`ntpr`**
  - Cada cuántos pasos imprime energías al output.

- **`ntwx`**
  - Cada cuántos pasos escribe la trayectoria (mdcrd / NetCDF).

- **`ntwr`**
  - Cada cuántos pasos escribe el archivo de restart (`.rst` / `.ncrst`).

- **`ioutfm`** (opcional)
  - Controla el formato de trayectoria (ASCII vs NetCDF).
  - Normalmente se usa NetCDF.


### 8) “Calidad de vida”: PBC wrap y centro de masa

- **`iwrap`** (opcional)
  - Envuelve (wrap) coordenadas a la caja periódica al escribir coordenadas/trajectoria.
  - Útil para visualización (evita moléculas “partidas” por PBC).

- **`nscm`** (opcional)
  - Elimina el movimiento del centro de masa cada N pasos.
  - Útil para evitar drift del sistema (típico: `nscm=1000` o similar).


### 9) Restraints y control por etapas

- **`ntr`** (opcional)
  - Activa restraints armónicos.

- **`restraint_wt`** / **`restraintmask`** (si `ntr=1`)
  - `restraint_wt`: fuerza del restraint (kcal/mol·Å²)
  - `restraintmask`: selección de átomos, ej. `':1-XXX & !@H='` para aplicar restraint.

- **`nmropt`** + `&wt` (heating por rampa)
  - `nmropt=1` activa el control de NMR-style changes.
  - Con `&wt type='TEMP0'` puedes hacer la rampa 0→300K suave.


  



by [Albert Plazas](https://github.com/Alplalo)
