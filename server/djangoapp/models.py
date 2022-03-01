from django.db import models
from django.utils.timezone import now


# Create your models here.

#Enum class for options
from enum import Enum

class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50)
    description = models.CharField(null=False, max_length=100)
    def __str__(self):
        return "Name: {0}\nDescription:{1}".format(self.name, self.description)

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=50)
    dealer_id = models.IntegerField()

    #For the types
    class Types(ChoiceEnum):
        MICRO = "Micro";         SEDAN = "Sedan";
        HATCHBACK = "Hatchback"; UNIVERSAL = "Universal";
        LIFTBACK = "Liftback";   COUPE = "Coupe";
        CARBIOLET = "Cabriolet"; ROADSTER = "Roadster";
        TARGA = "Targa";         LIMOUSINE = "Limousine";
        MUSCLE = "Muscle";       SPORTS = "Sports";
        SUPER = "Super";         SUV = "SUV";
        CROSSOVER = "Crossover"; PICKUP = "Pickup";
        VAN = "Van";             MINIVAN = "Minivan";
        MINIBUS = "Minibus";     CAMPERVAN = "Campervan"
        TRUCK = "Truck";         BIG_TRUCK = "Big Truck"
    type = models.CharField(max_length=15, choices = Types.choices(), default = Types.MICRO);
    year = models.DateField(null = False);
    def __str__(self):
        return "Name: {0},\nMake: {1},\n Dealer: {2},\n Type: {3}".format(self.name, self.make, self.dealer, self.type);

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id
    def __str__(self):
        return "Name:" + self.name
