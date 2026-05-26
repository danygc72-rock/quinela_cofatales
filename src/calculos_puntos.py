def calcular_puntos(apuesta_a, apuesta_b, real_a, real_b):
    if apuesta_a == real_a and apuesta_b == real_b:
        return 5

    def _signo(goles_a, goles_b):
        if goles_a > goles_b:
            return "local"
        if goles_b > goles_a:
            return "visita"
        return "empate"

    if _signo(apuesta_a, apuesta_b) == _signo(real_a, real_b):
        return 3

    return 0
