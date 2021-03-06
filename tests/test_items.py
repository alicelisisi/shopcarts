import unittest
import os
from app.models import Item, DataValidationError
from app import app,db

DATABASE_URI = os.getenv('DATABASE_URI', None)

######################################################################
#  T E S T   C A S E S
######################################################################
class TestItems(unittest.TestCase):
    """ Test Cases for Items """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.logger.info(DATABASE_URI)
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_an_item(self):
        """ Create an item and assert that it exists """
        item = Item(sku="ID111", count=3, price=2.00, name="test_item",
                    link="test.com", brand_name="gucci", is_available=True)
        self.assertTrue(item != None)
        self.assertEqual(item.id, None)
        self.assertEqual(item.sku, "ID111")
        self.assertEqual(item.count, 3)
        self.assertEqual(item.price, 2.00)
        self.assertEqual(item.name, "test_item")
        self.assertEqual(item.link, "test.com")
        self.assertEqual(item.brand_name, "gucci")
        self.assertEqual(item.is_available, True)

    def test_add_an_item(self):
        """ Create an item and add it to the database """
        items = Item.all()
        self.assertEqual(items, [])
        item = Item(sku="ID111", count=3, price=2.00, name="test_item",
                    link="test.com", brand_name="gucci", is_available=True)
        self.assertTrue(item != None)
        self.assertEqual(item.id, None)
        item.save()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(item.id, 1)
        items = Item.all()
        self.assertEqual(len(items), 1)

    def test_update_an_item(self):
        """ Update an Item """
        item = Item(sku="ID111", count=3, price=2.00, name="test_item",
                    link="test.com", brand_name="gucci", is_available=True)
        item.save()
        self.assertEqual(item.id, 1)
        # Change it an save it
        item.sku = "ID222"
        item.save()
        self.assertEqual(item.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        items = Item.all()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].sku, "ID222")

    def test_delete_an_item(self):
        """ Delete an Item """
        item = Item(sku="ID111", count=3, price=2.00, name="test_item",
                    link="test.com", brand_name="gucci", is_available=True)
        item.save()
        self.assertEqual(len(Item.all()), 1)
        # delete the item and make sure it isn't in the database
        item.delete()
        self.assertEqual(len(Item.all()), 0)

    def test_delete_all_items(self):
        """ Delete all Items """
        item = Item(sku="ID111", count=3, price=2.00, name="test_item",
             link="test.com", brand_name="gucci", is_available=True)
        item.save()
        Item(sku="ID222", count=5, price=10.00, name="some_item",
             link="link.com", brand_name="nike", is_available=False).save()
        self.assertEqual(len(Item.all()), 2)

        # Remove all items from the Items table
        Item.query.delete()

        # Check if the number of items in Item table is zero because they were removed
        self.assertEqual(len(Item.all()), 0)


    def test_serialize_an_item(self):
        """ Test serialization of an Item """
        item = Item(sku="ID111", count=3, price=2.00, name="test_item",
                    link="test.com", brand_name="gucci", is_available=True)
        data = item.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], None)
        self.assertIn('sku', data)
        self.assertEqual(data['sku'], "ID111")
        self.assertIn('count', data)
        self.assertEqual(data['count'], 3)
        self.assertIn('price', data)
        self.assertEqual(data['price'], 2.00)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "test_item")
        self.assertIn('link', data)
        self.assertEqual(data['link'], "test.com")
        self.assertIn('brand_name', data)
        self.assertEqual(data['brand_name'], "gucci")
        self.assertIn('is_available', data)
        self.assertEqual(data['is_available'], True)

    def test_deserialize_an_item(self):
        """ Test deserialization of a Item """
        data = {"id": 1, "sku": "ID111", "count": 3, "price": 2.00, "name": "test_item",
                "link": "test.com", "brand_name": "gucci", "is_available": True}
        item = Item()
        item.deserialize(data)
        self.assertNotEqual(item, None)
        self.assertEqual(item.id, None)
        self.assertEqual(item.sku, "ID111")
        self.assertEqual(item.count, 3)
        self.assertEqual(item.price, 2.00)
        self.assertEqual(item.name, "test_item")
        self.assertEqual(item.link, "test.com")
        self.assertEqual(item.brand_name, "gucci")
        self.assertEqual(item.is_available, True)

    def test_find_item(self):
        """ Find an Item by ID """
        Item(sku="ID111", count=3, price=2.00, name="test_item",
             link="test.com", brand_name="gucci", is_available=True).save()
        test_item = Item(sku="ID222", count=5, price=10.00, name="some_item",
             link="link.com", brand_name="nike", is_available=False)
        test_item.save()
        item = Item.find(test_item.id)
        self.assertIsNot(item, None)
        self.assertEqual(item.sku, test_item.sku)
        self.assertEqual(item.count, 5)
        self.assertEqual(item.price, 10.00)
        self.assertEqual(item.name, "some_item")
        self.assertEqual(item.link, "link.com")
        self.assertEqual(item.is_available, False)

    def test_find_or_404(self):
        """ Find an Item by ID """
        Item(sku="ID111", count=3, price=2.00, name="test_item",
             link="test.com", brand_name="gucci", is_available=True).save()
        test_item = Item(sku="ID222", count=5, price=10.00, name="some_item",
             link="link.com", brand_name="nike", is_available=False)
        test_item.save()
        item = Item.find_or_404(test_item.id)
        self.assertIsNot(item, None)
        self.assertEqual(item.sku, test_item.sku)
        self.assertEqual(item.count, 5)
        self.assertEqual(item.price, 10.00)
        self.assertEqual(item.name, "some_item")
        self.assertEqual(item.link, "link.com")
        self.assertEqual(item.is_available, False)

    def test_find_by_sku(self):
        """ Find Items by SKU """
        Item(sku="ID111", count=3, price=2.00, name="test_item",
             link="test.com", brand_name="gucci", is_available=True).save()
        Item(sku="ID222", count=5, price=10.00, name="some_item",
                         link="link.com", brand_name="nike", is_available=False).save()
        items = Item.find_by_sku("ID222")
        self.assertEqual(items[0].sku, "ID222")
        self.assertEqual(items[0].count, 5)
        self.assertEqual(items[0].price, 10.00)
        self.assertEqual(items[0].name, "some_item")
        self.assertEqual(items[0].link, "link.com")
        self.assertEqual(items[0].brand_name, "nike")
        self.assertEqual(items[0].is_available, False)

    def test_find_by_price(self):
        """ Find an Item by Price """
        Item(sku="ID111", count=3, price=2.00, name="test_item",
             link="test.com", brand_name="gucci", is_available=True).save()
        Item(sku="ID222", count=5, price=10.00, name="some_item",
             link="link.com", brand_name="nike", is_available=False).save()
        items = Item.find_by_price(2.00)
        self.assertEqual(items[0].sku, "ID111")
        self.assertEqual(items[0].count, 3)
        self.assertEqual(items[0].price, 2.00)
        self.assertEqual(items[0].name, "test_item")
        self.assertEqual(items[0].link, "test.com")
        self.assertEqual(items[0].brand_name, "gucci")
        self.assertEqual(items[0].is_available, True)

    def test_find_by_availability(self):
        """ Find an Item by Availability"""
        Item(sku="ID111", count=3, price=2.00, name="test_item",
             link="test.com", brand_name="gucci", is_available=True).save()
        Item(sku="ID222", count=5, price=10.00, name="some_item",
             link="link.com", brand_name="nike", is_available=False).save()
        items = Item.find_by_availability(True)
        self.assertEqual(items[0].sku, "ID111")
        self.assertEqual(items[0].count, 3)
        self.assertEqual(items[0].price, 2.00)
        self.assertEqual(items[0].name, "test_item")
        self.assertEqual(items[0].link, "test.com")
        self.assertEqual(items[0].brand_name, "gucci")
        self.assertEqual(items[0].is_available, True)

    def test_find_by_brand(self):
        """ Find an Item by Availability"""
        Item(sku="ID111", count=3, price=2.00, name="test_item",
             link="test.com", brand_name="gucci", is_available=True).save()
        Item(sku="ID222", count=5, price=10.00, name="some_item",
             link="link.com", brand_name="nike", is_available=False).save()
        items = Item.find_by_brand("nike")
        self.assertEqual(items[0].sku, "ID222")
        self.assertEqual(items[0].count, 5)
        self.assertEqual(items[0].price, 10.00)
        self.assertEqual(items[0].name, "some_item")
        self.assertEqual(items[0].link, "link.com")
        self.assertEqual(items[0].brand_name, "nike")
        self.assertEqual(items[0].is_available, False)

    def test_find_by_name(self):
        """ Find an Item by Name"""
        Item(sku="ID111", count=3, price=2.00, name="test_item",
             link="test.com", brand_name="gucci", is_available=True).save()
        Item(sku="ID222", count=5, price=10.00, name="some_item",
             link="link.com", brand_name="nike", is_available=False).save()
        items = Item.find_by_name("some_item")
        self.assertEqual(items[0].sku, "ID222")
        self.assertEqual(items[0].count, 5)
        self.assertEqual(items[0].price, 10.00)
        self.assertEqual(items[0].name, "some_item")
        self.assertEqual(items[0].link, "link.com")
        self.assertEqual(items[0].brand_name, "nike")
        self.assertEqual(items[0].is_available, False)

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
