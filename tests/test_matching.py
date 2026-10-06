from app.matching import match
def test_ssd():assert match('NVMe SSD PCIe 4.0 1TB')[0]=='SSD'
def test_dram():assert match('DDR5 RDIMM ECC server memory')[0]=='DRAM'
def test_other():assert match('office paper')[1]==0
