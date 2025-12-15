from datetime import datetime
from iot_support.models import LogRecord
from iot_support.rules import evaluate

def test_cold_weak_signal_rule():
    recs = [
        LogRecord(datetime(2024,5,1,8,0,0),"CHESTER-GW-02","Sklep",3.49,12.0,-15,15,"RETRYING_CONNECTION")
    ]
    findings = evaluate(recs)
    assert any("Cold + weak signal" in f.title for f in findings)
