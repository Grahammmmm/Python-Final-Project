from breezypythongui import EasyFrame
# Import breezypythongui to enable GUI creation
class priceEstimator(EasyFrame):
    
    def __init__(self):
        # Create the GUI
        EasyFrame.__init__(self, title = "Corporate Vehicles GUI")
        self.setResizable(False);
        # Creation of labels
        self.addLabel(text = "Would you like to purchase new or used vehicles?", row = 0, column = 0, sticky = "NSEW")
        # Creation of Text Boxes
        self.conditionField = self.addTextField(text = "", row = 0, column = 1, sticky = "NSEW")
        # Creation of Buttons
        self.addButton(text = "Press after you input 'New' or 'Used'", row = 1, column = 0, command = self.addInputFields)

    def addInputFields (self):
        condition = self.conditionField.getText()
        # Add Labels
        self.addLabel(text = "What is the desired type of your vehicle(s)?", row = 2, column = 0, sticky = "NSEW")
        self.addLabel(text = "What is the desired brand of your vehicle(s)", row = 3, column = 0, sticky = "NSEW")
        self.addLabel(text = "How many vehicles will you purchase?", row = 4, column = 0, sticky = "NSEW")
        # Add Input Fields
        self.typeField = self.addTextField(text = "", row = 2, column = 1, sticky = "NSEW")
        self.brandField = self.addTextField(text = "", row = 3, column = 1, sticky = "NSEW")
        self.quantityField = self.addIntegerField(value = 0, row = 4, column = 1, sticky = "NSEW")
        if condition.lower() == "used":
           # Add new labels
            self.addLabel(text = "How many years old will your desired vehicle(s) be?", row = 5, column = 0, sticky = "NSEW")
            self.addLabel(text = "What is the desired mileage of your vehicle(s)", row = 6, column = 0, sticky = "NSEW")
            # Add new input fields
            self.ageField = self.addIntegerField(value = 0, row = 5, column = 1, sticky = "NSEW")
            self.mileageField = self.addIntegerField(value = 0, row = 6, column = 1, sticky = "NSEW")
        else:
            self.ageField = None
            self.mileageField = None  
        #Creates a button to view the total price
        self.addButton(text = "After you have answered all the questions, press to reveal the total price in dollars", row = 7, column = 0, command = self.createCar)
        self.priceField = self.addFloatField(value = 0, row = 8, column = 0, columnspan = 2, sticky = "NSEW")

    def createCar(self):
        vehicleType = self.typeField.getText().lower()
        vehicleBrand = self.brandField.getText().lower()
        vehicleQuantity = self.quantityField.getNumber()
        vehicleAge = self.ageField.getNumber() if self.ageField else 0
        vehicleMileage = self.mileageField.getNumber() if self.mileageField else 0
        basePrices = {
            "sedan": 33580,
            "suv": 48315,
            "truck": 42690,
            "van": 46772,
            "sports car": 47263
        }
        # Creates a list of the multiplier for each brand of vehicle
        brandMultipliers = {
            "ford": .7897,
            "chevrolet": .9237,
            "toyota": .7618,
            "honda": .8952, 
            "gmc": .8356
        }
        # Access the base price and brand multiplier
        basePrice = basePrices.get(vehicleType)
        brandMultiplier = brandMultipliers.get(vehicleBrand)
        if basePrice is None or brandMultiplier is None:
            self.priceField.setFloat(0)
            return
        # Create a car object
        car = self.Car(vehicleType, vehicleBrand, basePrice)
        # Calculate the final price
        finalPrice = car.estimatePrice(brandMultiplier, vehicleQuantity, vehicleAge, vehicleMileage)
        # Display the final price 
        self.priceField.setNumber(round(finalPrice, 2))
    class Car:
        # Creates a "car" class for easy access to variables
        def __init__(self, type, brand, price):
            self.type = type
            self.brand = brand
            self.price = price

        def estimatePrice (self, brandMultiplier, vehicleQuantity, vehicleAge=0, vehicleMileage=0):
            # Gets the initial price per unit
            pricePerUnit = self.price * brandMultiplier
            # Accounts for vehicle depreciation variables
            pricePerUnit *= (.85)**vehicleAge
            pricePerUnit *= (1- .000002) ** vehicleMileage
            # Displays the final value
            return pricePerUnit * vehicleQuantity
    
if __name__=="__main__":
    priceEstimator().mainloop()
