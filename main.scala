import scala.io.Source
import scala.collection.mutable.ArrayBuffer
import scalax.chart.api._

object Main {
  val datasetDirectory = "CTEQ61"

  def readPDFData(flavor: Int): (Array[Double], Array[Double]) = {
    val filename = s"$datasetDirectory/cteq61_$flavor.dat"
    val source = Source.fromFile(filename)
    val lines = source.getLines().drop(1)
    val xValues = ArrayBuffer[Double]()
    val pdfValues = ArrayBuffer[Double]()

    for (line <- lines) {
      val cols = line.split("\\s+").map(_.toDouble)
      xValues.append(cols(0))
      pdfValues.append(cols(1))
    }

    source.close()
    (xValues.toArray, pdfValues.toArray)
  }

  def interpolate(xs: Array[Double], ys: Array[Double], x: Double): Double = {
    val index = xs.indexWhere(_ >= x)
    if (index == 0) ys(0)
    else if (index == -1) ys.last
    else {
      val x0 = xs(index - 1)
      val x1 = xs(index)
      val y0 = ys(index - 1)
      val y1 = ys(index)
      y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    }
  }

  def main(args: Array[String]): Unit = {
    val flavor = 1
    val (xValues, pdfValues) = readPDFData(flavor)
    val sqrtS = 13000.0
    val crossSection = ScatteringCrossSection.calculate(sqrtS)
    println(s"Total Scattering Cross Section: $crossSection")

    val dataset = new DefaultXYDataset()
    dataset.addSeries("PDF", Array(xValues, pdfValues))

    val chart = XYLineChart(dataset)
    chart.show()
  }
}
