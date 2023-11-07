from pyspark.sql import DataFrame

jdbc_url = "jdbc:postgresql://db.jyestwasjqmvyzrqdfkn.supabase.co:5432/postgres"

connection_properties = {
    "user": "postgres",
    # WARNING !
    # Not good to do that but easy solution for the assignment ONLY
    # The good practise if to save that in the secret section of the given GitHub repository
    "password": *******,
    "driver": "org.postgresql.Driver"
}

url: str = "https://db.jyestwasjqmvyzrqdfkn.supabase.co"


def to_db(df: DataFrame, table: str):
    df.write \
        .format("jdbc") \
        .option("url", url) \
        .option("dbtable", table) \
        .mode("append") \
        .jdbc(jdbc_url, f"public.{table}", properties=connection_properties)
