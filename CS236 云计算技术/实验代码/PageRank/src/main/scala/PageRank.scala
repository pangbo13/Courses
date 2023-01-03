
import org.apache.spark.graphx.GraphLoader
import org.apache.spark.sql.SparkSession

object PageRankExample {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession
      .builder
      .appName(s"${this.getClass.getSimpleName}")
      .getOrCreate()
    val sc = spark.sparkContext

    val graph = GraphLoader.edgeListFile(sc, "data/graphx/wiki-Vote.txt")
    val ranks = graph.pageRank(0.00001).vertices

    println(ranks.collect().sortBy(fields => fields._2).reverse.slice(0,20).mkString("\n"))
    spark.stop()
  }
}
