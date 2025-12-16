import csv

def load_vtd_csv(path):
    defects = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            defects.append({
                "km": float(row["km"]),
                "depth_percent": float(row["depth_percent"]),
                "length_mm": float(row["length_mm"]),
                "defect_type": row["defect_type"]
            })
    return defects
