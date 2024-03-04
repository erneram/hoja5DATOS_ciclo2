import simpy
import random
import csv

class Programa:

    def __init__(self, name, env, ram, procesador, writer):
        self.name = name
        self.env = env
        self.ram = ram
        self.procesador = procesador
        self.num_instruc = random.randint(1, 10)
        self.memoria = random.randint(1, 10)
        self.t_final = 0
        self.t_inicial = 0
        self.estado = "new"
        self.writer = writer

    def pedir_memoria(self):
        while True:
            if self.estado == "new":
                self.t_inicial = self.env.now
                print(f"Proceso {self.name} pidiendo memoria RAM")
                
                yield self.env.timeout(1)
                if self.memoria <= self.ram.level:
                    yield self.ram.get(self.memoria)
                    print(f"Proceso {self.name} obtuvo {self.memoria} de memoria")
                    self.estado = "ready"
                    break
                else:
                    print(f"Falta de memoria para el proceso {self.name}")
                    yield self.env.timeout(1)

    def devolver_memoria(self):
        yield self.env.timeout(1)
        yield self.ram.put(self.memoria)
        self.estado = "new"
        

    def usar_cpu(self):
        while True:
            if self.estado == "ready":
                with self.procesador.request() as req:
                    print(f"Proceso {self.name} pidiendo CPU")
                    yield req
                    print(f"Proceso {self.name} inicia su uso del CPU")
                    yield self.env.timeout(1)
                    self.num_instruc -= 3

                    if self.num_instruc <= 0:
                        self.end_time = self.env.now
                        print(f"Proceso {self.name} ha completado su proceso")
                        self.estado = "terminated"
                        break

                    io = random.randint(1, 21)
                    if io == 1 or io == 2:
                        print(f"Proceso {self.name} regresa al estado ready")
                        self.estado = "ready"
                        break

    def promedio_tiempo(self):
        self.writer.writerow([-1 *(self.t_final - self.t_inicial)])
        

    def run(self):
        yield self.env.process(self.pedir_memoria())
        yield self.env.process(self.usar_cpu())
        yield self.env.process(self.devolver_memoria())
        self.promedio_tiempo()
        print(f"Proceso {self.name} terminado")


def simular(env, ram, procesador, amount_process, writer, intervalo):
    for i in range(amount_process):
        proceso = Programa(i+1, env, ram, procesador, writer)
        env.process(proceso.run())
        yield env.timeout(random.expovariate(1.0 / intervalo))


# ----------------------25 operaciones----------------------
nombre_archivo = "./Intervalosde5/dataTime/25_procesos.csv"
with open(nombre_archivo, 'w', newline='') as archivo_csv:
    escritor = csv.writer(archivo_csv)
    env = simpy.Environment()
    ram = simpy.Container(env, init=100, capacity=100)
    procesador = simpy.Resource(env, capacity=1)
    amount_process = 25
    intervalo = 5

    print("Iniciando simulación")
    env.process(simular(env, ram, procesador, amount_process, escritor, intervalo))
    env.run()

# ----------------------50 operaciones----------------------
nombre_archivo = "./Intervalosde5/dataTime/50_procesos.csv"
with open(nombre_archivo, 'w', newline='') as archivo_csv:
    escritor = csv.writer(archivo_csv)
    env = simpy.Environment()
    ram = simpy.Container(env, init=100, capacity=100)
    procesador = simpy.Resource(env, capacity=1)
    amount_process = 50
    intervalo = 5

    print("Iniciando simulación")
    env.process(simular(env, ram, procesador, amount_process, escritor, intervalo))
    env.run()

# ----------------------100 operaciones----------------------
nombre_archivo = "./Intervalosde5/dataTime/100_procesos.csv"
with open(nombre_archivo, 'w', newline='') as archivo_csv:
    escritor = csv.writer(archivo_csv)
    env = simpy.Environment()
    ram = simpy.Container(env, init=100, capacity=100)
    procesador = simpy.Resource(env, capacity=1)
    amount_process = 100
    intervalo = 5

    print("Iniciando simulación")
    env.process(simular(env, ram, procesador, amount_process, escritor, intervalo))
    env.run()

# ----------------------150 operaciones----------------------
nombre_archivo = "./Intervalosde5/dataTime/150_procesos.csv"
with open(nombre_archivo, 'w', newline='') as archivo_csv:
    escritor = csv.writer(archivo_csv)
    env = simpy.Environment()
    ram = simpy.Container(env, init=100, capacity=100)
    procesador = simpy.Resource(env, capacity=1)
    amount_process = 150
    intervalo = 5
    
    print("Iniciando simulación")
    env.process(simular(env, ram, procesador, amount_process, escritor, intervalo))
    env.run()

# ----------------------200 operaciones----------------------
nombre_archivo = "./Intervalosde5/dataTime/200_procesos.csv"
with open(nombre_archivo, 'w', newline='') as archivo_csv:
    escritor = csv.writer(archivo_csv)
    env = simpy.Environment()
    ram = simpy.Container(env, init=100, capacity=100)
    procesador = simpy.Resource(env, capacity=1)
    amount_process = 200
    intervalo = 5
    
    print("Iniciando simulación")
    env.process(simular(env, ram, procesador, amount_process, escritor, intervalo))
    env.run()