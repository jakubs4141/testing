from datetime import datetime
from iot_support.models import LogRecord
from iot_support.analysis import snr_voltage_correlation

def test_correlation_runs():
    recs = [
        LogRecord(datetime(2024,5,1,8,0,0),"D","X",3.6,20,10,15,"OK"),
        LogRecord(datetime(2024,5,1,9,0,0),"D","X",3.5,20,-10,15,"OK"),
    ]
    c = snr_voltage_correlation(recs)
    assert isinstance(c, float)
