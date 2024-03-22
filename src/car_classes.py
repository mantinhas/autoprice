import pickle

class Car:
    def __init__(self, mileage, year, price, name, fuel):
        self.name = name
        self.price = price
        self.mileage = mileage
        self.year = year
        self.fuel = fuel

    def __str__(self):
        return self.name + " (" + str(self.year) + ") " + str(self.mileage) + " Km " + self.fuel + " > " + str(self.price) + "€"

class CarList:
    def __init__(self,name):
        self.list = []
        self.name = name
    
    def append(self,car):
        self.list.append(car)

    def save(self):
        filename = "pickles/"+self.name+".pkl"
        output = open(filename,"wb")
        pickle.dump(self,output)
        output.close()

    def load_carlist(filename):
        infile = open(filename,"rb")
        carlist = pickle.load(infile)
        infile.close()
        return carlist

    def __str__(self):
        return "\n".join([str(car) for car in self.list])
