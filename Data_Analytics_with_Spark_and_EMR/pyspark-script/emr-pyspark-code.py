from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local")
        .config(conf=SparkConf()).getOrCreate()

df = spark.read.format("csv")
        .option("header", "true")
        .load("hdfs:///user-data-acg/user-data-*.csv")

results = df.groupBy("`dob.age`","`gender`")
            .count()
            .orderBy("count", ascending=False)

results.show()

results.coalesce(1).write.csv("hdfs:///results", sep=",", header="true")