from simulation import Simulation
from visualiser import Visualiser


def main():
    simulation = Simulation()
    visualiser = Visualiser(simulation)
    visualiser.run()

    
if __name__ == "__main__":
    main()
