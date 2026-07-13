from ai.predict import predict_category
samples = [

    "SWIGGY ONLINE PAYMENT",

    "ATM CASH WDL",

    "AMAZON INDIA",

    "SALARY CREDIT",

    "NETFLIX",

    "HP PETROL",

    "OLA CAB"

]

for text in samples:

    print(text)

    print("Prediction :", predict_category(text))

    print("------------------------")