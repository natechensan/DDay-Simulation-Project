from Models import *

def main():
    sim = Simulation("omaha")
    sim.warmup()
    sim.run_simulation()

            
if __name__ == '__main__':
    main()
