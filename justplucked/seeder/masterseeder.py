import random
from django.utils import timezone
from master.models import (
    Country, State, District, City, UnitOfMeasure, Bank, BankBranch,
    Category, Tag, FarmingPracticeType, CropType, LivestockType, CertificationBody
)

def create_dummy_data():
    # Create 5 Countries
    countries = []
    for i in range(1, 6):
        country = Country.objects.create(
            name=f"Country {i}",
            iso_code=f"CN{i}",
            active=True,
            remarks=f"Remarks for Country {i}"
        )
        countries.append(country)
        print(f"Created Country: {country}")

    # Create 5 States for each Country
    states = []
    for country in countries:
        for i in range(1, 6):
            state = State.objects.create(
                country=country,
                name=f"State {i} of {country.name}",
                active=True,
                remarks=f"Remarks for State {i} of {country.name}"
            )
            states.append(state)
            print(f"Created State: {state}")

    # Create 5 Districts for each State
    districts = []
    for state in states:
        for i in range(1, 6):
            district = District.objects.create(
                state=state,
                name=f"District {i} of {state.name}",
                active=True,
                remarks=f"Remarks for District {i} of {state.name}"
            )
            districts.append(district)
            print(f"Created District: {district}")

    # Create 5 Cities for each District
    cities = []
    for district in districts:
        for i in range(1, 6):
            city = City.objects.create(
                district=district,
                name=f"City {i} of {district.name}",
                active=True,
                remarks=f"Remarks for City {i} of {district.name}"
            )
            cities.append(city)
            print(f"Created City: {city}")

    # Create 5 Units of Measure
    units = []
    unit_names = ["Kilogram", "Liter", "Piece", "Meter", "Box"]
    unit_symbols = ["kg", "l", "pc", "m", "box"]
    for i in range(5):
        unit = UnitOfMeasure.objects.create(
            name=unit_names[i],
            symbol=unit_symbols[i],
            description=f"Description for {unit_names[i]}",
            active=True,
            remarks=f"Remarks for {unit_names[i]}"
        )
        units.append(unit)
        print(f"Created Unit of Measure: {unit}")

    # Create 5 Banks
    banks = []
    bank_names = ["Global Bank", "National Bank", "City Bank", "Farmers Bank", "Agri Bank"]
    for i in range(5):
        bank = Bank.objects.create(
            name=bank_names[i],
            swift_code=f"SWIFT{i}12345",
            active=True,
            remarks=f"Remarks for {bank_names[i]}"
        )
        banks.append(bank)
        print(f"Created Bank: {bank}")

    # Create 5 Bank Branches for each Bank
    bank_branches = []
    for bank in banks:
        for i in range(1, 6):
            branch = BankBranch.objects.create(
                bank=bank,
                branch_name=f"Branch {i} of {bank.name}",
                location=f"Location {i} of {bank.name}",
                ifsc_code=f"IFSC{i}{bank.id}",
                active=True,
                remarks=f"Remarks for Branch {i} of {bank.name}"
            )
            bank_branches.append(branch)
            print(f"Created Bank Branch: {branch}")

    # Create 5 Categories (some with parents)
    categories = []
    for i in range(1, 6):
        parent = None
        if i > 2:  # Make some categories have parents
            parent = random.choice(categories[:2])
        category = Category.objects.create(
            name=f"Category {i}",
            parent=parent,
            description=f"Description for Category {i}",
            active=True,
            remarks=f"Remarks for Category {i}"
        )
        categories.append(category)
        print(f"Created Category: {category}")

    # Create 5 Tags
    tags = []
    for i in range(1, 6):
        tag = Tag.objects.create(
            name=f"Tag {i}"
        )
        tags.append(tag)
        print(f"Created Tag: {tag}")

    # Create 5 Farming Practice Types
    farming_practices = []
    practice_names = ["Organic", "Hydroponic", "Permaculture", "Conventional", "Biodynamic"]
    for i in range(5):
        practice = FarmingPracticeType.objects.create(
            name=practice_names[i],
            description=f"Description for {practice_names[i]} farming",
            active=True
        )
        farming_practices.append(practice)
        print(f"Created Farming Practice: {practice}")

    # Create 5 Crop Types
    crop_types = []
    crop_names = ["Wheat", "Rice", "Corn", "Soybean", "Potato"]
    for i in range(5):
        crop = CropType.objects.create(
            name=crop_names[i],
            category=random.choice(categories),
            active=True
        )
        crop_types.append(crop)
        print(f"Created Crop Type: {crop}")

    # Create 5 Livestock Types
    livestock_types = []
    livestock_names = ["Cattle", "Poultry", "Sheep", "Goat", "Pig"]
    for i in range(5):
        livestock = LivestockType.objects.create(
            name=livestock_names[i],
            active=True
        )
        livestock_types.append(livestock)
        print(f"Created Livestock Type: {livestock}")

    # Create 5 Certification Bodies
    cert_bodies = []
    cert_names = ["Organic Cert Inc", "GlobalGAP", "FairTrade", "USDA Organic", "EU Organic"]
    for i in range(5):
        cert = CertificationBody.objects.create(
            name=cert_names[i],
            country=random.choice(countries),
            active=True,
            remarks=f"Remarks for {cert_names[i]}"
        )
        cert_bodies.append(cert)
        print(f"Created Certification Body: {cert}")

    print("Dummy data creation completed successfully!")

 