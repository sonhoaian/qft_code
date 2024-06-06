import scala.math._
import scala.io.Source
import scala.collection.mutable.ArrayBuffer

object ScatteringCrossSection {
  val datasetDirectory = "/path/to/CTEQ61/dataset/directory"

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

  def integratePDFsAndAmplitude(flavor1: Int, flavor2: Int, sqrtS: Double): Double = {
    val (xValues1, pdfValues1) = readPDFData(flavor1)
    val (xValues2, pdfValues2) = readPDFData(flavor2)
    val xMin = 0.0001
    val xMax = 1.0
    val numSteps = 1000
    val dx = (xMax - xMin) / numSteps
    var totalCrossSection = 0.0

    for (i <- 0 until numSteps) {
      val x1 = xMin + i * dx
      for (j <- 0 until numSteps) {
        val x2 = xMin + j * dx
        val pdf1 = interpolate(xValues1, pdfValues1, x1)
        val pdf2 = interpolate(xValues2, pdfValues2, x2)
        val s = x1 * x2 * sqrtS * sqrtS
        val t = -s / 2.0
        val u = -s / 2.0
        val amplitude = FeynmanAmplitude.calculate(s, t, u)
        val dSigma = pdf1 * pdf2 * amplitude * amplitude
        totalCrossSection += dSigma * dx * dx
      }
    }

    totalCrossSection
  }

  def calculate(sqrtS: Double): Double = {
    val flavor1 = 1
    val flavor2 = -1
    integratePDFsAndAmplitude(flavor1, flavor2, sqrtS)
  }
}
