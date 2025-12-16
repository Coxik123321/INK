CREATE TABLE pipeline (
    id SERIAL PRIMARY KEY,
    diameter_mm REAL,
    wall_thickness_mm REAL,
    design_pressure REAL,
    year_built INT
);

CREATE TABLE defect (
    id SERIAL PRIMARY KEY,
    pipeline_id INT,
    depth_percent REAL,
    length_mm REAL,
    defect_type TEXT
);
