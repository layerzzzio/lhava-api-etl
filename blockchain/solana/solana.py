from blockchain import Blockchain
from blockchain.solana.lib.signatures import get_signatures_for_address, extract_signatures
from blockchain.solana.lib.transactions import get_transaction_details
from utils.db import to_db
from utils.persist import persist_json, spark_read_json, EXTRACT_FOLDER
from pyspark.sql.functions import current_date, from_unixtime, to_date, expr, col, current_timestamp, slice
from pyspark.sql import DataFrame
import logging


class Solana(Blockchain):
    transaction_file = 'solana_transaction'

    def extract(self,  mint_address: str):
        # API CALLS
        signatures_obj = get_signatures_for_address(mint_address)
        logging.info(f"get_signatures_for_address count={len(signatures_obj)}")
        # limit the signatures to 10 to make the process faster (testing purposes)
        signatures = extract_signatures(signatures_obj)[0:10]
        logging.info(f"extract_signatures count={len(signatures)}. Example: {signatures[0]}")
        transaction = get_transaction_details(signatures)
        logging.info(f"transaction count={len(transaction)}")

        # PERSISTING
        logging.info(f"persist_parquet transaction to parquet")
        persist_json(transaction, EXTRACT_FOLDER, self.transaction_file)

    def transform(self) -> DataFrame:
        # LOAD TRANSACTION
        logging.info(f"load transaction data from json")
        tx = spark_read_json(EXTRACT_FOLDER, self.transaction_file)

        # FILTER DATA (2 YEARS ONLY)
        logging.info(f"filter and transform data")
        two_years_ago = current_date() - expr("interval 2 years")
        tx_with_date = tx.withColumn("blockDate", to_date(from_unixtime(tx["blockTime"])))
        filtered_tx = tx_with_date.filter(tx_with_date["blockDate"] >= two_years_ago)

        # Extract transaction_id based on the first element of 'signatures' array
        filtered_tx_with_id = filtered_tx\
            .withColumn("id", col("transaction")['signatures'][0])\
            .withColumn("programId", col("transaction")['message']['instructions'][0]['programIdIndex'])\
            .withColumn("signers_number", col("transaction")['message']['header']['numRequiredSignatures'])\
            .withColumn("account_keys", col("transaction")['message']['accountKeys'])\
            .withColumn("signers", expr("slice(account_keys, 1, signers_number)"))\
            .withColumn("executing_account", col("account_keys").getItem(col("programId")))\
            .withColumn("sys_insertdatetime", current_timestamp())

        # Define the selected columns
        selected_columns = ['id', 'blockTime', 'meta', 'slot', 'transaction', 'blockDate', 'executing_account', 'signers', 'sys_insertdatetime']
        result = filtered_tx_with_id\
            .select(*selected_columns)\
            .selectExpr(
                "id",
                "blockTime",
                "to_json(meta) AS meta",
                "slot",
                "to_json(transaction) AS transaction",
                "blockDate",
                "executing_account",
                "signers",
                "sys_insertdatetime"
            )

        return result

    def load(self, df: DataFrame):
        logging.info(f"write data to postgres")
        to_db(df, 'raw_transaction')