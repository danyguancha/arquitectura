# Importamos el módulo sys para usar la entrada y salida estándar
import sys

# Definimos el tamaño de la memoria en bytes
MEM_SIZE = 32

# Definimos el tamaño de los registros y las instrucciones en bits
REG_SIZE = 16
INS_SIZE = 16

# Definimos el número de registros de propósito general
NUM_REGS = 8

# Definimos las máscaras para extraer los campos de las instrucciones
OP_MASK = 0xF0000000 # Los 4 bits más significativos son el código de operación
RN_MASK = 0x0F000000 # Los siguientes 4 bits son el número del primer registro
RM_MASK = 0x00F00000 # Los siguientes 4 bits son el número del segundo registro
DIR_MASK = 0x0000FFFF # Los 16 bits menos significativos son la dirección de memoria o el valor inmediato

# Definimos los códigos de operación según el conjunto de instrucciones
NOP = 0x0
ADD = 0x1
SUB = 0x2
AND = 0x3
OR = 0x4
XOR = 0x5
NOT = 0x6
MOV = 0x7
LDR = 0x8
STR = 0x9
JMP = 0xA
JZ = 0xB
JN = 0xC
IN = 0xD
OUT = 0xE
HALT = 0xF

# Definimos los componentes del procesador
alu = 0 # La ALU guarda el resultado de la última operación
uc = 0 # La UC guarda el estado del procesador (0 = ejecutando, 1 = detenido)
mbr = 0 # El MBR guarda la instrucción o el dato leído de la memoria
cp = 0 # El CP guarda la dirección de la próxima instrucción a ejecutar
mar = 0 # El MAR guarda la dirección de memoria a acceder
ir = 0 # El IR guarda la instrucción a decodificar y ejecutar
regs = [0] * NUM_REGS # Los registros se inicializan a cero

# Definimos la memoria de sistema y la memoria de datos
# Usamos listas de enteros para representar la memoria
# Cada elemento de la lista es un byte
# Para leer o escribir una instrucción o un dato de 32 bits, se usan 4 bytes consecutivos
mem_sis = [0] * MEM_SIZE # La memoria de sistema se inicializa a cero
mem_dat = [0] * MEM_SIZE # La memoria de datos se inicializa a cero

# Definimos los buses
bus_int = 0 # El bus interno transfiere datos entre el MBR y el IR o los registros
bus_dat = 0 # El bus de datos transfiere datos entre el MBR y la memoria de datos
bus_dir = 0 # El bus de direcciones transfiere direcciones entre el MAR y la memoria de sistema o de datos
bus_con = 0 # El bus de control transfiere señales de control entre la UC y los demás componentes

# Definimos las funciones que realizan las operaciones del conjunto de instrucciones
# Cada función recibe como parámetros los números de los registros o las direcciones de memoria involucrados
# Cada función actualiza el valor de la ALU y de los registros o la memoria según corresponda
# Cada función devuelve un valor booleano que indica si la operación se realizó con éxito o no

def nop():
    # No hace nada
    global alu
    alu = 0 # Resetea el valor de la ALU
    return True # Devuelve verdadero

def add(rn, rm):
    # Suma los contenidos de los registros Rn y Rm y guarda el resultado en Rn
    global alu, regs
    if rn < 0 or rn >= NUM_REGS or rm < 0 or rm >= NUM_REGS:
        # Comprueba si los números de los registros son válidos
        return False # Devuelve falso si no lo son
    alu = regs[rn] + regs[rm] # Suma los contenidos de los registros y guarda el resultado en la ALU
    regs[rn] = alu # Copia el resultado de la ALU al registro Rn
    return True # Devuelve verdadero

def sub(rn, rm):
    # Resta los contenidos de los registros Rn y Rm y guarda el resultado en Rn
    global alu, regs
    if rn < 0 or rn >= NUM_REGS or rm < 0 or rm >= NUM_REGS: # Comprueba si los números de los registros son válidos
        return False # Devuelve falso si no lo son
    alu = regs[rn] - regs[rm] # Resta los contenidos de los registros y guarda el resultado en la ALU
    regs[rn] = alu # Copia el resultado de la ALU al registro Rn
    return True # Devuelve verdadero

def and_(rn, rm):
    # Realiza la operación lógica AND entre los contenidos de los registros Rn y Rm y guarda el resultado en Rn
    global alu, regs
    if rn < 0 or rn >= NUM_REGS or rm < 0 or rm >= NUM_REGS: # Comprueba si los números de los registros son válidos
        return False # Devuelve falso si no lo son
    alu = regs[rn] & regs[rm] # Realiza la operación lógica AND y guarda el resultado en la ALU
    regs[rn] = alu # Copia el resultado de la ALU al registro Rn
    return True # Devuelve verdadero

def or_(rn, rm):
    # Realiza la operación lógica OR entre los contenidos de los registros Rn y Rm y guarda el resultado en Rn
    global alu, regs
    if rn < 0 or rn >= NUM_REGS or rm < 0 or rm >= NUM_REGS: # Comprueba si los números de los registros son válidos
        return False # Devuelve falso si no lo son
    alu = regs[rn] | regs[rm] # Realiza la operación lógica OR y guarda el resultado en la ALU
    regs[rn] = alu # Copia el resultado de la ALU al registro Rn
    return True # Devuelve verdadero

def xor(rn, rm):
    # Realiza la operación lógica XOR entre los contenidos de los registros Rn y Rm y guarda el resultado en Rn
    global alu, regs
    if rn < 0 or rn >= NUM_REGS or rm < 0 or rm >= NUM_REGS: # Comprueba si los números de los registros son válidos
        return False # Devuelve falso si no lo son
    alu = regs[rn] ^ regs[rm] # Realiza la operación lógica XOR y guarda el resultado en la ALU
    regs[rn] = alu # Copia el resultado de la ALU al registro Rn
    return True # Devuelve verdadero

def not_(rn):
    # Realiza la operación lógica NOT sobre el contenido del registro Rn y guarda el resultado en Rn
    global alu, regs
    if rn < 0 or rn >= NUM_REGS: # Comprueba si el número del registro es válido
        return False # Devuelve falso si no lo es
    alu = ~regs[rn] # Realiza la operación lógica NOT y guarda el resultado en la ALU
    regs[rn] = alu # Copia el resultado de la ALU al registro Rn
    return True # Devuelve verdadero

def mov(rn, rm):
    # Copia el contenido del registro Rm al registro Rn
    global alu, regs
    if rn < 0 or rn >= NUM_REGS or rm < 0 or rm >= NUM_REGS: # Comprueba si los números de los registros son válidos
        return False # Devuelve falso si no lo son
    alu = regs[rm] # Copia el contenido del registro Rm a la ALU
    regs[rn] = alu # Copia el contenido de la ALU al registro Rn
    return True # Devuelve verdadero

def ldr(rn, dir):
    # Carga el contenido de la dirección de memoria dir al registro Rn
    global alu, regs, mbr, mar, bus_int, bus_dat, bus_dir
    if rn < 0 or rn >= NUM_REGS or dir < 0 or dir +4 > MEM_SIZE: # Comprueba si el número del registro y la dirección de memoria son válidos
        return False # Devuelve falso si no lo son
    mar = dir # Copia la dirección de memoria al MAR
    bus_dir = mar # Copia el contenido del MAR al bus de direcciones
    mbr = read_mem(bus_dir) # Lee el contenido de la memoria de datos en la dirección indicada por el bus de direcciones y lo guarda en el MBR
    if mbr == None: # Comprueba si hubo un error al leer la memoria
        return False # Devuelve falso si lo hubo
    bus_dat = mbr # Copia el contenido del MBR al bus de datos
    bus_int = bus_dat # Copia el contenido del bus de datos al bus interno
    alu = bus_int # Copia el contenido del bus interno a la ALU
    regs[rn] = alu # Copia el contenido de la ALU al registro Rn
    return True # Devuelve verdadero

def str(rn, dir):
    # Almacena el contenido del registro Rn en la dirección de memoria dir
    global alu, regs, mbr, mar, bus_int, bus_dat, bus_dir
    if rn < 0 or rn >= NUM_REGS or dir < 0 or dir +4 > MEM_SIZE: # Comprueba si el número del registro y la dirección de memoria son válidos
        return False # Devuelve falso si no lo son
    alu = regs[rn] # Copia el contenido del registro Rn a la ALU
    bus_int = alu # Copia el contenido de la ALU al bus interno
    bus_dat = bus_int # Copia el contenido del bus interno al bus de datos
    mbr = bus_dat # Copia el contenido del bus de datos al MBR
    mar = dir # Copia la dirección de memoria al MAR
    bus_dir = mar # Copia el contenido del MAR al bus de direcciones
    if not write_mem(bus_dir, mbr): # Escribe el contenido del MBR en la memoria de datos en la dirección indicada por el bus de direcciones
        return False # Devuelve falso si hubo un error al escribir la memoria
    return True # Devuelve verdadero

def jmp(dir):
    # Salta a la dirección de memoria dir
    global alu, cp, mar, bus_dir
    if dir < 0 or dir +4 > MEM_SIZE: # Comprueba si la dirección de memoria es válida
        return False # Devuelve falso si no lo es
    alu = dir # Copia la dirección de memoria a la ALU
    bus_dir = alu # Copia el contenido de la ALU al bus de direcciones
    mar = bus_dir # Copia el contenido del bus de direcciones al MAR
    cp = mar # Copia el contenido del MAR al CP
    return True # Devuelve verdadero

def jz(dir):
    # Salta a la dirección de memoria dir si el resultado de la última operación es cero
    global alu, cp, mar, bus_dir
    if dir < 0 or dir +4 > MEM_SIZE: # Comprueba si la dirección de memoria es válida
        return False # Devuelve falso si no lo es
    if alu == 0: # Comprueba si el resultado de la última operación es cero
        bus_dir = dir # Copia la dirección de memoria al bus de direcciones
        mar = bus_dir # Copia el contenido del bus de direcciones al MAR
        cp = mar # Copia el contenido del MAR al CP
    return True # Devuelve verdadero

def jn(dir):
    # Salta a la dirección de memoria dir si el resultado de la última operación es negativo
    global alu, cp, mar, bus_dir
    if dir < 0 or dir +4 > MEM_SIZE: # Comprueba si la dirección de memoria es válida
        return False # Devuelve falso si no lo es
    if alu < 0: # Comprueba si el resultado de la última operación es negativo
        bus_dir = dir # Copia la dirección de memoria al bus de direcciones
        mar = bus_dir # Copia el contenido del bus de direcciones al MAR
        # Copia el contenido del bus de direcciones al MAR
        cp = mar # Copia el contenido del MAR al CP
    return True # Devuelve verdadero

def in_(rn):
    # Lee un dato de entrada y lo guarda en el registro Rn
    global alu, regs, bus_int
    if rn < 0 or rn  >= NUM_REGS: # Comprueba si el número del registro es válido
        return False # Devuelve falso si no lo es
    try:
        alu = int(input()) # Lee un dato de entrada y lo convierte a entero
    except ValueError: # Captura el error si el dato no es válido
        return False # Devuelve falso si lo hay
    bus_int = alu # Copia el contenido de la ALU al bus interno
    regs[rn] = bus_int # Copia el contenido del bus interno al registro Rn
    return True # Devuelve verdadero

def out(rn):
    # Escribe el contenido del registro Rn en la salida
    global alu, regs, bus_int
    if rn < 0 or rn >= NUM_REGS: # Comprueba si el número del registro es válido
        return False # Devuelve falso si no lo es
    alu = regs[rn] # Copia el contenido del registro Rn a la ALU
    bus_int = alu # Copia el contenido de la ALU al bus interno
    print(bus_int) # Escribe el contenido del bus interno en la salida
    return True # Devuelve verdadero

def halt():
    # Detiene la ejecución del programa
    global alu, uc
    alu = 0 # Resetea el valor de la ALU
    uc = 1 # Cambia el estado del procesador a detenido
    return True # Devuelve verdadero

# Definimos una función auxiliar que convierte una lista de bytes a un entero de 32 bits
def bytes_to_int(bytes):
    # Recibe una lista de 4 bytes y devuelve un entero de 32 bits
    # Usa el orden de bytes little-endian, es decir, el byte menos significativo está en el índice 0
    # Usa el formato de complemento a dos para representar los números negativos
    if len(bytes) != 4: # Comprueba si la lista tiene 4 bytes
        return None # Devuelve None si no los tiene
    num = 0 # Inicializa el número a cero
    for i in range(4): # Recorre los 4 bytes de la lista
        num += bytes[i] << (8 * i) # Suma el valor del byte multiplicado por 2 elevado a 8 veces el índice
    if num >= 2**31: # Comprueba si el número es mayor o igual que 2 elevado a 31
        num -= 2**32 # Resta 2 elevado a 32 para obtener el número negativo correspondiente
    return num # Devuelve el número

# Definimos una función auxiliar que convierte un entero de 32 bits a una lista de bytes
def int_to_bytes(num):
    # Recibe un entero de 32 bits y devuelve una lista de 4 bytes
    # Usa el orden de bytes little-endian, es decir, el byte menos significativo está en el índice 0
    # Usa el formato de complemento a dos para representar los números negativos
    if num < 0: # Comprueba si el número es negativo
        num += 2**32 # Suma 2 elevado a 32 para obtener el número positivo correspondiente
    bytes = [] # Inicializa la lista de bytes vacía
    for i in range(4): # Recorre los 4 bytes del número
        bytes.append(num & 0xFF) # Añade el byte menos significativo a la lista
        num >>= 8 # Desplaza el número 8 bits a la derecha
    return bytes # Devuelve la lista de bytes

# Definimos una función auxiliar que lee una instrucción o un dato de 32 bits de la memoria de datos
def read_mem(dir):
    # Recibe una dirección de memoria y devuelve una instrucción o un dato de 32 bits
    # Usa la memoria de datos para leer el contenido
    if dir < 0 or dir +4 > MEM_SIZE: # Comprueba si la dirección de memoria es válida
        return None # Devuelve None si no lo es
    #index = dir //4 # Calcula el índice de la lista de bytes
    bytes = mem_dat[dir:dir + 4] # Obtiene los 4 bytes consecutivos de la memoria de datos

    num = bytes_to_int(bytes) # Convierte los bytes a un entero de 32 bits
  
    return num # Devuelve el entero


# Definimos una función auxiliar que escribe una instrucción o un dato de 32 bits en la memoria de datos
def write_mem(dir, num):
    # Recibe una dirección de memoria y una instrucción o un dato de 32 bits
    # Usa la memoria de datos para escribir el contenido
    if dir < 0 or dir +4 > MEM_SIZE: # Comprueba si la dirección de memoria es válida
        return False # Devuelve falso si no lo es
    bytes = int_to_bytes(num) # Convierte el entero a una lista de bytes
    
    mem_dat[dir:dir+4] = bytes # Asigna los 4 bytes consecutivos a la memoria de datos
    return True # Devuelve verdadero

# Definimos una función que carga un programa en la memoria de sistema
def load_program(program):
    # Recibe una lista de instrucciones o datos de 32 bits y los carga en la memoria de sistema
    # Devuelve la dirección de inicio del programa o None si hay un error
    global mem_sis
    if len(program) * 4 > MEM_SIZE: # Comprueba si el programa cabe en la memoria de sistema
        return None # Devuelve None si no cabe
    dir = 0 # Inicializa la dirección de inicio a cero
    for num in program: # Recorre las instrucciones o datos del programa
        bytes = int_to_bytes(num) # Convierte el entero a una lista de bytes
        mem_sis[dir:dir+4] = bytes # Asigna los 4 bytes consecutivos a la memoria de sistema
        dir += 4 # Incrementa la dirección en 4
    return 0 # Devuelve la dirección de inicio del programa

# Definimos una función que ejecuta el programa cargado en la memoria de sistema
def run_program():
    # Ejecuta el programa cargado en la memoria de sistema
    # Usa un bucle que simula el ciclo de instrucción
    # Devuelve el estado final del procesador y los registros
    global uc, mbr, cp, mar, ir, bus_int, bus_dat, bus_dir, bus_con
    while uc == 0: # Mientras el procesador esté ejecutando
        mar = cp # Copia el CP al MAR
        bus_dir = mar # Copia el MAR al bus de direcciones
        mbr = read_mem(bus_dir) # Lee la instrucción de la memoria de sistema en la dirección indicada por el bus de direcciones y la guarda en el MBR
        if mbr == None: # Comprueba si hubo un error al leer la memoria
            print("Error: dirección de memoria inválida") # Imprime un mensaje de error
            break # Sale del bucle
        
        bus_dat = mbr # Copia el MBR al bus de datos
        bus_int = bus_dat # Copia el bus de datos al bus interno
        ir = bus_int # Copia el bus interno al IR
        cp += 4 # Incrementa el CP en 4
        op = (ir & OP_MASK) >> 28 # Extrae el código de operación de la instrucción
        rn = (ir & RN_MASK) >> 24 # Extrae el número del primer registro de la instrucción
        rm = (ir & RM_MASK) >> 20 # Extrae el número del segundo registro de la instrucción
        dir = ir & DIR_MASK # Extrae la dirección de memoria o el valor inmediato de la instrucción
        if op == NOP: # Si el código de operación es NOP
            if not nop(): # Ejecuta la operación NOP
                print("Error: operación NOP inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        elif op == ADD: # Si el código de operación es ADD
            if not add(rn, rm): # Ejecuta la operación ADD
                print("Error: operación ADD inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        elif op == SUB: # Si el código de operación es SUB
            if not sub(rn, rm): # Ejecuta la operación SUB
                print("Error: operación SUB inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        elif op == AND: # Si el código de operación es AND
            if not and_(rn, rm): # Ejecuta la operación AND
                print("Error: operación AND inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        elif op == OR: # Si el código de operación es OR
            if not or_(rn, rm): # Ejecuta la operación OR
                print("Error: operación OR inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        elif op == XOR: # Si el código de operación es XOR
            if not xor(rn, rm): # Ejecuta la operación XOR
                print("Error: operación XOR inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        elif op == NOT: # Si el código de operación es NOT
            if not not_(rn): # Ejecuta la operación NOT
                print("Error: operación NOT inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        elif op == MOV: # Si el código de operación es MOV
            if not mov(rn, rm): # Ejecuta la operación MOV
                print("Error: operación MOV inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        elif op == LDR: # Si el código de operación es LDR
            if not ldr(rn, dir): # Ejecuta la operación LDR
                print("Error: operación LDR inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        elif op == STR: # Si el código de operación es STR
            if not str(rn, dir): # Ejecuta la operación STR
                print("Error: operación STR inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        elif op == JMP: # Si el código de operación es JMP
            if not jmp(dir): # Ejecuta la operación JMP
                print("Error: operación JMP inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        elif op == JZ: # Si el código de operación es JZ
            if not jz(dir): # Ejecuta la operación JZ
                print("Error: operación JZ inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        elif op == JN: # Si el código de operación es JN
            if not jn(dir): # Ejecuta la operación JN
                print("Error: operación JN inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        elif op == IN: # Si el código de operación es IN
            if not in_(rn): # Ejecuta la operación IN
                print("Error: operación IN inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        elif op == OUT: # Si el código de operación es OUT
            if not out(rn): # Ejecuta la operación OUT
                print("Error: operación OUT inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        elif op == HALT: # Si el código de operación es HALT
            if not halt(): # Ejecuta la operación HALT
                print("Error: operación HALT inválida") # Imprime un mensaje de error si hay un error
                break # Sale del bucle
        else: # Si el código de operación no es válido
            print("Error: código de operación inválido") # Imprime un mensaje de error
            break # Sale del bucle
    print("Estado final del procesador y los registros:") # Imprime el estado final del procesador y los registros
    print("ALU:", alu) # Imprime el valor de la ALU
    print("UC:", uc) # Imprime el valor de la UC
    print("MBR:", mbr) # Imprime el valor del MBR
    print("CP:", cp) # Imprime el valor del CP
    print("MAR:", mar) # Imprime el valor del MAR
    print("IR:", ir) # Imprime el valor del IR
    for i in range(NUM_REGS): # Recorre los registros
        print(f"R{i}:", regs[i])


# Definimos un ejemplo de programa que suma dos números de entrada y escribe el resultado en la salida

program = [
    IN, 0, # Lee el primer número y lo guarda en el registro R0
    IN, 1, # Lee el segundo número y lo guarda en el registro R1
    ADD, 0, 1, # Suma los contenidos de los registros R0 y R1 y guarda el resultado en R0
    OUT, 0, # Escribe el contenido del registro R0 en la salida
    HALT # Detiene la ejecución del programa
]

# Cargamos el programa en la memoria de sistema
start = load_program(program)
if start == None: # Comprueba si hubo un error al cargar el programa
    print("Error: el programa no se pudo cargar en la memoria de sistema") # Imprime un mensaje de error
else: # Si no hubo error
    cp = start # Asigna la dirección de inicio del programa al CP
    run_program() # Ejecuta el programa