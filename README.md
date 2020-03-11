Question:
How did changing values on the SparkSession property parameters affect the throughput and latency of the data?

Answer:
Changing these values affected both `inputRowsPerSecond` and  `processedRowsPerSecond`


Question:
What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?

Answer:
Setting `spark.sql.shuffle.partitions : 100` and `spark.streaming.backpressure.enabled : true` was quite optimal for me. I read both their usage from the Spark Documentation. Both configs made `inputRowsPerSecond` and  `processedRowsPerSecond` to be near-equal

