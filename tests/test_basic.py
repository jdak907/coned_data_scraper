from coned_utility.dataframe import transform

def test_transform_columns(tmp_path):
    p = tmp_path / "in.csv"
    p.write_text("Account,From Date,To Date,Use,Reading,KVARS\n123,2024-01-01,2024-01-31,10,EST,5\n")
    df = transform(str(p))
    assert "Utility Code" in df.columns
    assert "Utility Account Number" in df.columns
    assert len(df) == 1
