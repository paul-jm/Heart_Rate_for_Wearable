from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import requests


def get_sql_context_instance(spark_context):
	if ('sqlContextSingletonInstance' not in globals()):
		globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
	return globals()['sqlContextSingletonInstance']
def process_rdd(time, rdd):
	print("----------- %s -----------" % str(time))
	try:
 # Get spark sql singleton context from the current context
		sql_context = get_sql_context_instance(rdd.context)
 # convert the RDD to Row RDD
		row_rdd = rdd.map(lambda w: Row(time=w[0], heart_rate=w[1]))
 # create a DF from the Row RDD
		hr_df = sql_context.createDataFrame(row_rdd)
 # Register the dataframe as table
		hr_df.registerTempTable("heartrate")
 # get the top 10 hashtags from the table using SQL and print them
		hr_counts_df = sql_context.sql("select time, heart_rate from heartrate order by time asc") 
		hr_counts_df.toPandas().to_csv('heart_rate.csv')
		hr_counts_df.show()
        
	except:
		e = sys.exc_info()[0]
		print("Error: %s" % e)

def updateFunction(newValues, runningCount):
    if runningCount is None:
        runningCount = 0
        return sum(newValues, runningCount)
    else: 
        return runningCount

# create spark configuration
conf = SparkConf()
conf.setAppName("FitbitStreamApp")
# create spark context with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# create the Streaming Context from the above spark context with interval size 2 seconds
ssc = StreamingContext(sc, 3)
# setting a checkpoint to allow RDD recovery
ssc.checkpoint("checkpoint_FitbitApp")
# read data from port 9009
lines = ssc.socketTextStream("localhost",45001)
#print(dataStream)
# split each tweet into words  
words = lines.map(lambda line: line.split()).map(lambda items: (items[0],int(items[1])))

whole = words.updateStateByKey(updateFunction)
whole.foreachRDD(process_rdd)
whole.pprint()

# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()