from iot_support.parser import read_csv

def test_read_csv_smoke(tmp_path):
    p = tmp_path / "a.csv"
    p.write_text(
        "Timestamp,Device_ID,Location,Battery_Voltage_V,Temperature_C,Signal_SNR_dB,Send_Interval_Min,Status\n"
        "2024-05-01 08:00:00,CHESTER-GW-01,Sklad_A,3.65,21.5,12,15,OK\n",
        encoding="utf-8"
    )
    recs = read_csv(p)
    assert len(recs) == 1
    assert recs[0].device_id == "CHESTER-GW-01"
