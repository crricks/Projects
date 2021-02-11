import pytest
import os
import sqlite3

from src.inventory_app.warehouse_inventory import Inventory

# debated about using unittest MacicMock vs. setting up test database

@pytest.fixture(scope='function')
def setup_db():
    """Fixture to set up Inventory object and add items"""
    db = Inventory('test')

    db.add_item('test item 1', 'test location 1')
    db.add_item('test item 2', 'test location 2')

    yield db

    # returns db.cursor()
    # yield db.open_db()

def test_db_add_items_method(setup_db):

    # opens database and returns cursor()
    db = setup_db
    cur = db.open_db()

    # test data entered
    assert len(list(cur.execute('SELECT * FROM Items'))) == 2
    assert len(list(cur.execute('SELECT * FROM Locations'))) == 2
    assert len(list(cur.execute('SELECT * FROM Inventory'))) == 2

    # test can't enter duplicate data
    result = db.add_item('test item 1', 'test location 1')
    assert result == "Item already entered in system."

def test_db_update_location_method(setup_db):

    # opens database and returns cursor()
    db = setup_db
    cur = db.open_db()

    # test if location of 'test item 1' is updated and 'another location' added
    db.update_location('test item 1', 'another location')
    assert len(list(cur.execute('SELECT * FROM Locations'))) == 3

    # test updated in Inventory table
    cur.execute('''SELECT Items.name, Locations.name
                         FROM Inventory JOIN Items JOIN Locations ON
                         Items.id = Inventory.items_id AND
                         Locations.id = Inventory.locations_id
                         WHERE Items.name = (?)''', ('test item 1',))
    assert cur.fetchone() == ('test item 1', 'another location')

    # test can't update location of item not entered
    result = db.update_location('test item 3', 'another location')
    assert result == "Item not entered in system"

def test_db_remove_item_method(setup_db):

    # opens database and returns cursor()
    db = setup_db
    cur = db.open_db()

    # test removing item
    db.remove_item('test item 2')
    assert len(list(cur.execute('SELECT * FROM Items'))) == 1

def test_db_view_items_method(setup_db):

    # opens database and returns cursor()
    db = setup_db
    cur = db.open_db()

    # test view items method that compiles ids from Items and Locations tables
    result = db.view_items('Locations')
    assert result == [('test item 1', 'another location'), ('test item 2', 'test location 2')]

def test_end():
    os.remove('test.sqlite')