import blogseeder
import masterseeder
import farmerseeder
import productseeder
print("Seeder Started")
blogseeder.create_blog_dummy_data()
print("Blog Dummy Data")
masterseeder.create_dummy_data()
print("Master Dummy Data")
farmerseeder.create_farmer_dummy_data()
print("Farmer Dummy Data")
productseeder.create_product_dummy_data()
print("Product Dummy Data")