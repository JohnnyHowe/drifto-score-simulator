from simulation import Simulation
from visualiser import Visualiser


def main():
    simulation = Simulation("car_handling_stats.csv")
    visualiser = Visualiser(simulation)
    visualiser.run()

    
if __name__ == "__main__":
    main()
