# BLG317E-G8

After activation of the virtual environment run the commands sequentially
  
####  pip install requirements.txt  
####  python src/db/import.py
####  python src/main.py
# Dataset
Dataset in this project is designed as a fictitious eCommerce clothing site for educational and training purposes in data analysis and machine learning. The dataset includes detailed information about customers, products, orders, logistics, web events, and digital marketing. The tables covers all the information and attributes that a simple e-commerce site should have.
Tables in this dataset are:
- Users
- Events
- Orders
- Order Items
- Inventory Items
- Products
- Distribution Centers
![image](https://github.com/itudb2308/itudb2308/assets/92018010/781009c7-ace4-49a0-81b2-1c5868158322)

![image](https://github.com/itudb2308/itudb2308/assets/92018010/14e3465b-61c9-4c22-af69-aadf51311e22)

# Access to Admin Panel
You can access to admin panel by adding /admin at the end of the localhost:5000 URL. Without logging, you can not view anything in the admin panel.
Inorder to login, use admin@admin.net as username and admin as password. 
# Admin Panel
Admin can use some of the CRUD operations on this panel. Can delete and read user, update order status, create-update-delete distribution center, add-delete-update product etc.

# Customer Panel
Without logging or signing up, customers can not view anything in this panel. After customers signs up they will be automatically logged in.

Customers can open the categories they want by clicking on the options from the home page or they can open the products page and filter the products.
From the product detail page, customers can add the product they wish to purchase to their cart. 

After they are done with their shopping, they can open the cart page. In the cart page, customers can remove the products they dont want to purchase or remove all the items from the cart. 
They can see the total price of the cart as well. After they click at the buy button, they will be redirected to order detail page.
