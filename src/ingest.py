import os
from astroquery.gaia import Gaia
import pyarrow as pa
import pyarrow.parquet as pq

def fetch_gaia_sample(row_limit=100_000, output_path="data/raw/gaia_dr3_sample.parquet"):
    """
    Queries the public Gaia Archive TAP service and downloads optical astrometry data
    including proper motions for spatial cross-matching.
    """
    print(f"--- Launching Gaia DR3 TAP Query (Limit: {row_limit:,} rows) ---")
    
    # ADQL Query to fetch Right Ascension, Declination, and Proper Motion parameters
    adql_query = f"""
    SELECT TOP {row_limit}
        source_id,
        ra,
        dec,
        pmra,
        pmdec,
        ref_epoch
    FROM gaiadr3.gaia_source
    WHERE ra IS NOT NULL 
      AND dec IS NOT NULL 
      AND pmra IS NOT NULL 
      AND pmdec IS NOT NULL
    """
    
    # Execute asynchronous TAP query
    job = Gaia.launch_job_async(adql_query)
    results = job.get_results()
    
    # Convert Astropy Table to PyArrow Table and save as Parquet
    df = results.to_pandas()
    table = pa.Table.from_pandas(df)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pq.write_table(table, output_path)
    
    print(f"Successfully downloaded {len(df):,} rows to '{output_path}'.")
    return output_path

if __name__ == "__main__":
    fetch_gaia_sample()