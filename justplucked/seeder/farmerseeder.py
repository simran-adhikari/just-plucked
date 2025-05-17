import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django_countries import countries
from farmer.models import Farmer, Farm, FarmerDocument, CropProduction, Certification

def create_farmer_dummy_data():
    # List of realistic farmer names
    first_names = ["John", "Mary", "Robert", "Sarah", "David", "Emma", "Michael", "Olivia", "James", "Sophia"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson"]
    
    # List of realistic crops
    crops = ["Wheat", "Rice", "Corn", "Soybean", "Potato", "Tomato", "Coffee", "Tea", "Cotton", "Sugarcane"]
    
    # Create 10 farmers
    for i in range(1, 11):
        # Create a user account for the farmer
        username = f"farmer{i}"
        email = f"{username}@example.com"
        user = User.objects.create_user(
            username=username,
            email=email,
            password="password123"
        )
        
        # Generate farmer data
        full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        phone = f"+1{random.randint(200, 999)}{random.randint(1000000, 9999999)}"
        country = random.choice(list(countries))[0]
        
        farmer = Farmer.objects.create(
            user=user,
            full_name=full_name,
            gender=random.choice(['male', 'female', 'other']),
            date_of_birth=datetime.now() - timedelta(days=random.randint(20*365, 60*365)),
            marital_status=random.choice(['single', 'married', 'widowed', 'divorced']),
            phone=phone,
            alternate_phone=f"+1{random.randint(200, 999)}{random.randint(1000000, 9999999)}" if random.choice([True, False]) else "",
            email=email,
            country=country,
            state=f"State {random.randint(1, 50)}",
            district=f"District {random.randint(1, 20)}",
            municipality=f"Municipality {random.randint(1, 10)}",
            ward_no=str(random.randint(1, 30)),
            street_address=f"{random.randint(100, 999)} Main St",
            nid_number=f"ID{random.randint(1000000, 9999999)}" if random.choice([True, False]) else "",
            bank_name=random.choice(["AgriBank", "Farmers Bank", "National Bank", "Global Finance"]),
            bank_account_number=str(random.randint(100000000, 999999999)),
            bank_branch=f"Branch {random.randint(1, 20)}",
            land_area_in_acres=round(random.uniform(1, 100), 2),
            primary_crop=random.choice(crops),
            farming_experience_years=random.randint(1, 30),
            is_active=True,
            verified=random.choice([True, False])
        )
        print(f"Created Farmer: {farmer}")
        
        # Create 1-3 farms per farmer
        for j in range(1, random.randint(2, 4)):
            farm = Farm.objects.create(
                farmer=farmer,
                name=f"{farmer.full_name}'s Farm {j}",
                location_description=f"Located in {farmer.district}, near {random.choice(['river', 'mountain', 'forest', 'highway'])}",
                farm_type=random.choice(['organic', 'conventional', 'mixed']),
                land_area_in_acres=round(random.uniform(1, 50), 2),
                latitude=round(random.uniform(-90, 90), 6) if random.choice([True, False]) else None,
                longitude=round(random.uniform(-180, 180), 6) if random.choice([True, False]) else None,
                established_date=datetime.now() - timedelta(days=random.randint(365, 365*20)),
                active=True
            )
            print(f"  Created Farm: {farm}")
            
            # Create 1-3 crop productions per farm
            for k in range(1, random.randint(2, 4)):
                crop_prod = CropProduction.objects.create(
                    farm=farm,
                    crop_name=random.choice(crops),
                    season=random.choice(['Spring', 'Summer', 'Fall', 'Winter']),
                    year=random.randint(2018, 2023),
                    yield_quantity_kg=round(random.uniform(100, 5000), 2),
                    notes=f"Good harvest despite {random.choice(['drought', 'heavy rains', 'pest issues', 'ideal conditions'])}"
                )
                print(f"    Created Crop Production: {crop_prod}")
        
        # Create 1-3 documents per farmer
        for doc_num in range(1, random.randint(2, 4)):
            doc_type = random.choice(['nid', 'land_ownership', 'tax', 'other'])
            FarmerDocument.objects.create(
                farmer=farmer,
                document_type=doc_type,
                document_name=f"{doc_type.capitalize()} Document {doc_num} for {farmer.full_name}",
                file=None  # No actual file uploaded
            )
            print(f"  Created Document for {farmer}")
        
        # Create 0-2 certifications per farmer
        for cert_num in range(random.randint(0, 2)):
            title = random.choice(['Organic Certification', 'Good Agricultural Practices', 'Fair Trade Certified'])
            Certification.objects.create(
                farmer=farmer,
                title=title,
                issuing_authority=random.choice(['USDA', 'EU Organic', 'GlobalGAP', 'FairTrade International']),
                issue_date=datetime.now() - timedelta(days=random.randint(30, 365*3)),
                expiry_date=datetime.now() + timedelta(days=random.randint(30, 365*2)) if random.choice([True, False]) else None,
                certificate_file=None  # No actual file uploaded
            )
            print(f"  Created Certification for {farmer}")

    print("\nSuccessfully created 10 farmers with related data!")

 