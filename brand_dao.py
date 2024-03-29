import psycopg2
from psycopg2 import Error

class BrandDao:
    def __init__(self, connection):
        self.connection = connection

    def create(self, brand):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""INSERT INTO brands (href, name, replied_complaint, total_complaint, average_reply_sec, rating_count, rating) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
                              (brand.href, brand.name, brand.replied_complaint, brand.total_complaint, 
                               brand.average_reply_sec, brand.rating_count, brand.rating))
            self.connection.commit()
            print("Brand created successfully.")
        except Error as e:
            print(f"Error while inserting brand: {e}")

    def read(self, brand_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM brands WHERE id = %s", (brand_id,))
            brand_data = cursor.fetchone()
            if brand_data:
                return Brand(*brand_data)
            else:
                print("Brand not found.")
        except Error as e:
            print(f"Error while fetching brand: {e}")

    def update(self, brand):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""UPDATE brands SET href = %s, name = %s, replied_complaint = %s, total_complaint = %s,
                              average_reply_sec = %s, rating_count = %s, rating = %s WHERE id = %s""",
                              (brand.href, brand.name, brand.replied_complaint, brand.total_complaint,
                               brand.average_reply_sec, brand.rating_count, brand.rating, brand.id))
            self.connection.commit()
            print("Brand updated successfully.")
        except Error as e:
            print(f"Error while updating brand: {e}")

    def delete(self, brand_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM brands WHERE id = %s", (brand_id,))
            self.connection.commit()
            print("Brand deleted successfully.")
        except Error as e:
            print(f"Error while deleting brand: {e}")

