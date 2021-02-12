from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
from datetime import datetime

from src.avy.avy_report import AvyReport, create_chart

test_report = AvyReport()
area = 'North San Juan'
today = datetime.now().strftime("%d")
zone = 'Above Treeline'
prg = '../src/avy/avy_report.py'

# -------------------------------------------------
def test_exists():
    """check if the file exists"""
    assert os.path.isfile(prg)

# -------------------------------------------------
def test_get_area_method():
    """tests area is correct"""
    result = test_report.get_area()
    assert result == 'North San Juan'

# -------------------------------------------------
def test_get_date_method():
    """tests date is correct"""
    res_date, res_author = test_report.get_today()
    assert today in res_date

# -------------------------------------------------
def test_zones_compiles():
    """tests zones and information are gathered"""
    result = test_report.get_zones()
    assert zone in result
    assert result[zone] is not None

# -------------------------------------------------
def test_summary():
    """tests summary report is gathered"""
    result = test_report.get_summary()
    assert result is not None

# -------------------------------------------------
def test_station_data():
    """tests weather station data is gathered"""
    result = test_report.get_station_data()
    assert result is not None
