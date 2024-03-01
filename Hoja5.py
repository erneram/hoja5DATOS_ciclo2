import simpy
import random

class Programa:

    def __init__(self, name, env, ram, procesador):
        self.name = name
        self.env = env
        self.ram = ram
        self.procesador = procesador
        self.num_instruc = random.randint(1, 10)
        self.memoria = random.randint(1, 10)
        self.t_inicio = 0
        self.t_final = 0
        self.prom_tiempo = 0
        self.estado = "new"

    def pedir_memoria(self):
        while True:
            if self.estado == "new":
                self.t_inicio = self.env.now
                print(f"Proceso {self.name} pidiendo memoria RAM")
                yield self.ram.get(self.memoria)
                yield self.env.timeout(1)
                if self.memoria <= self.ram.level:
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
        self.prom_tiempo = self.t_final - self.t_inicio
        

    def run(self):
        yield self.env.process(self.pedir_memoria())
        yield self.env.process(self.usar_cpu())
        yield self.env.process(self.devolver_memoria())
        print(f"Proceso {self.name} terminado")


def simular(env, ram, procesador, amount_process):
    for i in range(amount_process):
        proceso = Programa(i+1, env, ram, procesador)
        env.process(proceso.run())
        yield env.timeout(3) 

# Environment setup
env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)
procesador = simpy.Resource(env, capacity=1)
amount_process = 25

# Simulation
print("Iniciando simulación")
env.process(simular(env, ram, procesador, amount_process))
env.run()