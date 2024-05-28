# DINAMICA MOLECULAR CON AMBER

## Índice

- [DINAMICA MOLECULAR CON AMBER](#dinamica-molecular-con-amber)
  - [Índice](#índice)
  - [LEaP](#leap)
    - [Descripción](#descripción)
    - [Uso](#uso)
      - [Funciones Principales](#funciones-principales)
    - [Modificaciones](#modificaciones)
    - [Visualización en VMD](#visualización-en-vmd)
  - [Minimización](#minimización)
    - [Descripción](#descripción-1)
    - [Uso](#uso-1)
      - [Funciones Principales](#funciones-principales-1)
  - [Heating](#heating)
    - [Descripción](#descripción-2)
    - [Uso](#uso-2)
      - [Funciones Principales](#funciones-principales-2)

## LEaP

### Descripción

LEaP es una herramienta utilizada para la preparación de sistemas moleculares en dinámica molecular, especialmente en el contexto de simulaciones con el software Amber. Este README proporciona una guía básica sobre las principales funciones y modificaciones que se pueden realizar con LEaP, así como los pasos para la visualización y minimización de sistemas moleculares.

### Uso

#### Funciones Principales

- **source**: Se utiliza para cargar paquetes o librerías en el programa.

- **crear objeto**: Se puede crear un objeto con una secuencia específica utilizando la sintaxis `peptide = sequence{NGLY TYR ASP PRO GLU THR MET THR TRP CGLY}`. También es posible crearlo leyendo un archivo PDB mediante `peptide = loadPdb chignolin.pdb`.

- **solvatebox**: Se utiliza para solvatar un objeto con un tipo de caja, manteniendo una distancia mínima. Si el agua está a una cierta distancia del péptido, se elimina. En este caso se utiliza la siguiente sintaxis: `solvatebox (objeto: peptide, solvente: TIP3PBOX, distancia mínima del péptido al límite de la caja: 15.0, distancia para eliminar aguas: 1.8)`.

- **additions**: Añade iones para neutralizar la carga neta de la caja. La opción 0 permite que el programa calcule cuántos iones son necesarios para la neutralización y los añade automáticamente.

- **check**: Realiza un chequeo de la proteína para verificar que todo esté correcto. Para proteínas grandes, este proceso puede tardar considerablemente.

- **saveamberparm**: Genera archivos de topología y coordenadas en formato .top y .crd respectivamente.

- **savepdb**: Permite guardar la estructura en formato PDB.

- **quit**: Detiene la ejecución del programa en ese punto.

### Modificaciones

- Se ha modificado el aminoácido 7 (GLY) por MET.

> [!WARNING]
> Actualmente intentando generar una imagen del potencial electrostático molecular (PEM).

### Visualización en VMD

- El archivo top se lee en formato Amber7 Parm, seguido de la carga de coordenadas (CRD) utilizando el formato Amber7 Restart.

## Minimización

### Descripción

Durante la creación de la caja, es común que queden espacios vacíos alrededor de la proteína debido a la eliminación del agua que esté muy cerca de esta. Para abordar este problema y garantizar que la estructura molecular esté bien equilibrada, se lleva a cabo un proceso de minimización del sistema. Esta minimización implica pasar de un ensamble NVT a NPT, lo que implica ajustar el volumen de la caja para eliminar estos espacios vacíos.

### Uso

#### Funciones Principales

- **imin**: Se establece en 0 para realizar una dinámica molecular y en 1 para iniciar el proceso de minimización.

- **irest**: Se establece en 0 si es el primer cálculo de velocidades, en caso contrario, se modifica para mantener la misma dinámica.

- **ntx**: Similar a irest, pero aplicado a las coordenadas.

- **cut**: Define el rango de corte para crear la lista de Verlet de los vecinos de cada átomo.

- **maxcyc**: Define el número máximo de iteraciones en el proceso de minimización. En este caso, se utiliza el método de gradiente descendente (SD).

- **ntpr**: Determina cada cuántos pasos se imprime la información de la minimización.

- **ntb**: Define las condiciones periódicas. Se utiliza 0 para no PBC, 1 para Vcte y 2 para Pcte.

Se realizan dos minimizaciones en cadena utilizando el ejecutable `en_pmemd20_iqtc07`. Este ejecutable a su vez invoca el programa `run_pmemd20`, proporcionando el archivo de entrada, la topología, las coordenadas y una última columna con la extensión de las coordenadas.

## Heating

### Descripción

El proceso de calentamiento (heating) implica llevar a cabo una dinámica molecular corta donde se aplica un termostato para gradualmente elevar la temperatura del sistema a un valor específico, típicamente 300K. Este paso es crucial para simular el entorno del cuerpo humano y establecer las condiciones iniciales de la dinámica molecular.

### Uso

#### Funciones Principales

- **ntc**: Se establece en 2 para aplicar restricciones a los enlaces con hidrógeno, y en 0 para no aplicar restricciones.

- **ntf**: Similar a ntc.

- **dt**: Incremento de tiempo en la dinámica.

- **nstlim**: Número total de pasos de la dinámica.

- **ntp**: Control de presión: se establece en 0 para no escalar la presión, 1 para isotrópica y 2 para anisotrópica.

- **temp0**: Temperatura objetivo del sistema.

- **ntt**, **gamma_ln**, **ig**: Control de temperatura utilizando el termostato de Langevin.

- **ntwv**: Determina la frecuencia con la que se escriben las coordenadas.

- **iwrap**: Indica si las coordenadas escritas se "envuelven" en una caja primaria.


by [Albert Plazas](https://github.com/Alplalo)