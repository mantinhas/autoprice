from car_classes import CarList
import matplotlib.pyplot as plt

def plot(headless,carlists_filenames):
    carlists = [CarList.load_carlist(filename) for filename in carlists_filenames]

    fig, ax = plt.subplots(2,1,figsize=(9,10))
    for carlist in carlists:
        mileages = [car.mileage for car in carlist.list]
        prices = [car.price for car in carlist.list]
        ax[0].scatter(mileages, prices, label=carlist.name, s=3)
    ax[0].legend()
    ax[0].set_title("Mileage vs Price")
    ax[0].set_xlabel("Mileage (Km)")
    ax[0].set_ylabel("Price (€)")

    for carlist in carlists:
        years = [car.year for car in carlist.list]
        prices = [car.price for car in carlist.list]
        ax[1].scatter(years, prices, label=carlist.name, s=3)
    ax[1].legend()
    ax[1].set_title("Year vs Price")
    ax[1].set_xlabel("Year")
    ax[1].set_ylabel("Price (€)")

    if not headless:
        plt.show()
    else:
        save_path = "plots/"
        for carlist in carlists:
            save_path += carlist.name + "-VS-"
        save_path = save_path[:-4] + ".png"
        plt.savefig(save_path)
