object FeynmanAmplitude {
  val alpha_s: Double = 0.118
  val pi: Double = math.Pi

  def calculate(s: Double, t: Double, u: Double): Double = {
    val g_s = math.sqrt(4 * pi * alpha_s)
    val CF = 4.0 / 3.0
    val t_channel = (CF * g_s * g_s) / t
    val u_channel = (CF * g_s * g_s) / u
    val amplitude = t_channel + u_channel
    amplitude
  }
}
