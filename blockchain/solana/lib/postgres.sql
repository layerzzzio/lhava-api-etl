-- Create the raw_transaction table
CREATE TABLE public.raw_transaction (
    id TEXT,
    blockTime BIGINT,
    meta TEXT,
    slot BIGINT,
    transaction TEXT,
    blockDate DATE,
    executing_account TEXT,
    signers TEXT,
    sys_insertdatetime TIMESTAMP
);

-- Create the stage_transaction table (PK enforced)
CREATE TABLE stage_transaction (
    id TEXT PRIMARY KEY,
    blockTime BIGINT,
    meta JSONB,
    slot BIGINT,
    transaction JSONB,
    blockDate DATE,
    executing_account TEXT,
    signers TEXT[],
    sys_insertdatetime TIMESTAMP
);

-- Create the trigger function
CREATE OR REPLACE FUNCTION insert_into_stage_transaction()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO stage_transaction (id, blockTime, meta, slot, transaction, blockDate, executing_account, signers, sys_insertdatetime)
  VALUES (NEW.id, NEW.blockTime, NEW.meta::JSONB, NEW.slot, NEW.transaction::JSONB, NEW.blockDate, NEW.executing_account, string_to_array(NEW.signers, ','), NEW.sys_insertdatetime)
  ON CONFLICT (id) DO NOTHING;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger on the raw_transaction table
CREATE TRIGGER insert_into_stage_transaction_trigger
AFTER INSERT ON raw_transaction
FOR EACH ROW
EXECUTE FUNCTION insert_into_stage_transaction();

-- Create the agg_weekly_users table
CREATE TABLE public.agg_weekly_users (
    week_start_date DATE PRIMARY KEY,
    distinct_payers INT
);

-- Create the trigger function
CREATE OR REPLACE FUNCTION update_agg_weekly_users()
RETURNS TRIGGER AS $$
BEGIN
    -- Note that the calculation is done for the last 7 days from current date
    -- The week_start_date is defined as the date 7 days ago.
    WITH expanded_signers AS (
        SELECT blockdate, unnest(signers) as signer
        FROM public.stage_transaction
    )
    INSERT INTO agg_weekly_users (week_start_date, distinct_payers)
    SELECT
        CURRENT_DATE - INTERVAL '7 days' as week_start_date,
        COUNT(DISTINCT signer) as distinct_payers
    FROM
        expanded_signers
    WHERE
        blockdate != CURRENT_DATE
        AND blockdate >= CURRENT_DATE - INTERVAL '7 days'
    ON CONFLICT (week_start_date) DO UPDATE
    SET distinct_payers = EXCLUDED.distinct_payers;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger on the stage_transaction table
CREATE TRIGGER update_agg_weekly_users_trigger
AFTER INSERT ON stage_transaction
FOR EACH ROW
EXECUTE FUNCTION update_agg_weekly_users();

-- Create the agg_transaction_per_program table
CREATE TABLE public.agg_transaction_per_program (
    program_called TEXT PRIMARY KEY,
    transaction_count INT
);

CREATE OR REPLACE FUNCTION update_agg_transaction_per_program()
RETURNS TRIGGER AS $$
BEGIN
    WITH agg AS (
        SELECT
            executing_account as program_called,
            COUNT(DISTINCT id) as transaction_count
        FROM
            public.stage_transaction
        GROUP BY
            executing_account
    )
    INSERT INTO agg_transaction_per_program (program_called, transaction_count)
    SELECT
        program_called,
        transaction_count
    FROM
        agg
    ON CONFLICT (program_called) DO UPDATE
    SET transaction_count = EXCLUDED.transaction_count;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_agg_transaction_per_program_trigger
AFTER INSERT ON stage_transaction
FOR EACH ROW
EXECUTE FUNCTION update_agg_transaction_per_program();
