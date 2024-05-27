# ############ BIOQUIMICA ##############
# ######## DINAMICA MOLECULAR ##########
# ########### ALBERT PLAZAS ############


# LEaP: Descripción y Uso

## Descripción

LEaP es una herramienta utilizada para la preparación de sistemas moleculares en dinámica molecular, especialmente en el contexto de simulaciones con el software Amber. Este README proporciona una guía básica sobre las principales funciones y modificaciones que se pueden realizar con LEaP, así como los pasos para la visualización y minimización de sistemas moleculares.

## Uso

### Funciones Principales

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

- Se intenta generar una imagen del potencial electrostático molecular (PEM).

## Visualización

- El archivo top se lee en formato Amber7 Parm, seguido de la carga de coordenadas (CRD) utilizando el formato Amber7 Restart.

## Minimización

- Al crear la caja, pueden quedar espacios vacíos alrededor de la proteína debido a la eliminación de agua que esté muy cerca de esta. Para resolverlo, se realiza una minimización del sistema, pasando de un ensamble NVT a NPT y modificando el volumen de la caja.

- **imin**: Se establece en 0 para dinámica molecular y en 1 para minimización.

- **irest**: Se coloca en 0 si es el primer cálculo de velocidades, en caso contrario se debe modificar para mantener la misma dinámica.

- **ntx**: Similar a irest, pero para las coordenadas.

- **cut**: Establece el rango de corte para crear la lista de Verlet de los vecinos de cada átomo.

- **maxcyc**: Define el número de iteraciones en el proceso de minimización. En este caso, se utiliza el método SD.

- **ntpr**: Determina cada cuántos pasos se imprime la información de la minimización.

- **ntb**: Define las condiciones periódicas. Se utiliza 0 para no PBC, 1 para Vcte y 2 para Pcte.

Se realizan dos minimizaciones en cadena utilizando el ejecutable `en_pmemd20_iqtc07`. Finalmente, se ejecuta el programa `run_pmemd20`, proporcionando el archivo de entrada, la topología, las coordenadas y una última columna con la extensión de las coordenadas.