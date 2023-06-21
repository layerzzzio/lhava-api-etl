# OPTIMIZATION AND TROUBLESHOOTING

## Bottlenecks

The two main bottlenecks are:
- fetching the data from the blockchain
- writing the data to the Postgres (potential)

In other words, the extract and load steps.

### Bottleneck #1: Fetching data (extract)

Fetching data from the blockchain is currently done via API calls that are performed sequentially. It means, one call needs to be done to execute the next one. It is the slowest step in the program as it takes more than 95% of the entire program execution duration.

Precisely, what I do is the following:
- I first call the getSignaturesForAddress endpoint to retrieve signatures for confirmed transactions. This steps returns an array of signatures that can be numerous (in the 100s in what I have seen so far)
- Then, I loop over the signatures and call the getTransaction endpoint to return transaction details for a confirmed transaction

The looping part is what takes time since 100s sequential calls can be executed against the blockchain API.
Given a call takes a bit less than 1 sec to complete, 100 sequential calls, roughly take 100 sec to complete. It is a lot in comparison to other steps!

#### Solution 1: Parallelize API calls

Instead of making sequential API calls, parallelizing the calls to fetch data concurrently would help. asyncio is the perfect library to do so. Perfect for I/O bound code as they say.

#### Solution 2: Caching data

I am not 100% versed in the Solana data but I imagine some getTransaction calls could be the same for two different mint addresses. If this is confirmed, we could reduce the number of getTransaction calls by caching them so subsequent runs wouldn't need to fetch the same data from the API.

The same goes with subsequent runs for the same mint address. Caching data we already fetched before would help reduce this step.

#### Solution 3: Realtime via WebSocket

Instead of making a one-time API call to extract data, I would establish a WebSocket connection to the Solana blockchain and continuously receive real-time updates.

Then I would process and transform the received data in near real-time using PySpark's streaming capabilities.

#### Solution 4: Full Pub/Sub architecture

Implementing a real-time (pub/sub) architecture for the ETL program is the extension of solution #3. This solution is a much heavier one compared to #1 and #2 since the overall architecture needs to be rethought completely.

Indeed, with the current architecture, I am thinking of "batch" and "orchestrated ETL". What I mean by that is that an orchestrated program runs periodically at fixed hours (min or sec).

The real-time or pub/sub-architecture would be as follows :
- instead of directly making API calls to the Solana blockchain, a Kafka producer is set up to receive the blockchain data in real-time
- the Kafka producer can subscribe to the blockchain's websocket endpoints and capture the data as it becomes available
- the extracted data is then published to Kafka topics (the data are stored here)
- set up Kafka consumers that subscribe to the Kafka topics and process the incoming data
- implement the transformations using PySpark within the Kafka consumer
- the transformed data can be published to separate Kafka topics or directly consumed by a Kafka sink connector that loads the data into PostgreSQL

### Bottleneck #2: Writing data to Postgres (load)

With the current code and example I worked with, the load wasn't identified as a bottleneck.

But it could.

I particularly have in mind an issue I encountered 4 years ago.

We were inserting lots of data in MySQL database and one day had an issue in production since no connection with the database was available anymore.

In other words, if you are establishing a new connection for each insert statement, it can lead to overhead in connection establishment and teardown. 

#### Solution 1: Connection pooling

Implement connection pooling to reuse connections and reduce the overhead of creating new connections for each insert.

I have never tried but Apache [HikariCP](https://github.com/brettwooldridge/HikariCP)
 seems to be a promising connection pooling library.

## Pipeline failure

### What to do in case of transformation failure - how to troubleshoot?

#### Step #1: Good logging & Spark knowledge

When designing data pipelines, multiple logs should be implemented as checkpoints so we know which part of the code failed. Troubleshooting starts by that. Knowing where is the problem and what it is. It all starts with good logging.

Then debugging PySpark code can be easy or tricky.
The easy part is when the logs are self-explanatory and the issue is easy to fix.

The tricky part is when the error is hidden. A few things to know about Spark:
- It is sensitive to skewed data. It can leave joins hanging for a very long time. This can be found out by knowing your data well. Broadcast joins can help with that. One way to see that is by looking at the Spark jobs dashboard; The DAG is described showing the paint points in the code.
- It is also sensitive to small files. If input files are too numerous and too small, reading a bunch of files can be slow. A good practise is to size the files' chuncks at roughly the size of an HDFS block.

Basically I would go from there and drill down as I get more logs.

#### Step #2: knowing the stack pretty well

Sometimes an error can originate from an unrelated element of stack that failed. Knowing the stack and having a good monitoring of the entire system is also important.