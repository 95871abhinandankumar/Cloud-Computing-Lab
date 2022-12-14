import sys
import numpy as np
from math import sqrt

from pyspark import SparkContext
from pyspark.mllib.clustering import KMeans

S3_DATA_SOURCE_PATH = "s3://prakhar142/data-source/adultdata.txt"
s3_DATA_OUTPUT_PATH = "s3://prakhar142/data-source/data-output"
if __name__ == "__main__":
    sc = SparkContext(appName="KMeansExample")

    #data = sc.textFile("hdfs://localhost:9000/spark-kmeans/adultdata.txt")
    data = sc.textFile(S3_DATA_SOURCE_PATH)
    parsedData = data.map(lambda line: np.array([x for x in line.split(', ')])[np.array([0,2,11])].astype(float))
    
    
    
    # Build the model (cluster the data)
    clusters = KMeans.train(parsedData, 2, maxIterations=20, initializationMode="random")
    cluster_center=clusters.centers
    print("Centers:",clusters.centers,file=sys.stdout)
    #print("Centers:",clusters.centers,file=s3_DATA_OUTPUT_PATH)
    
    results = sc.parallelize(cluster_center)
    results.saveAsTextFile(s3_DATA_OUTPUT_PATH)
    # Evaluate clustering by computing Within Set Sum of Squared Errors
    def error(point):
        center = clusters.centers[clusters.predict(point)]
        return sqrt(sum([x**2 for x in (point - center)]))

    WSSSE = parsedData.map(lambda point: error(point)).reduce(lambda x, y: x + y)
    print("Within Set Sum of Squared Error = " + str(WSSSE),file=sys.stdout)
    #WSSSE.saveAsTextFile(s3_DATA_OUTPUT_PATH)
    #WSSSE/write

    sc.stop()
