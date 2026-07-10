import numpy as np
from numba import njit
from math import exp, fabs


# Fonte de calor - versão vetorizada
def calcula_Q(Qf, temp, xf, yf, nxf, nyf):
    X = xf[None, :]
    Y = yf[:, None]

    Qf[:, :] = 3.0 * temp * np.exp(-temp) * (
        1.0 + 5.0 * X + Y + 10.0 * X * Y
    )

    return Qf


@njit(fastmath=True, cache=True)
def max_abs_matrix(A):
    ny, nx = A.shape
    m = 0.0

    for i in range(ny):
        for j in range(nx):
            v = fabs(A[i, j])
            if v > m:
                m = v

    return m


@njit(fastmath=True, cache=True)
def resolve_newton(Tnf, T1f, fontef, k1f, a0f, a1f, tolf, it_mf):
    erro = 1.0
    it = 0
    Tn0 = Tnf

    denom = fabs(Tn0)
    if denom < 1e-14:
        denom = 1.0

    while erro > tolf and it < it_mf:
        e = exp(k1f * (Tnf - T1f))

        G = a0f * Tnf + a1f * e
        div = 1.0 / (a0f + k1f * a1f * e)

        inc = div * (fontef - G)

        Tnf = Tnf + inc
        erro = fabs(inc) / denom

        it += 1

    return Tnf


@njit(fastmath=True, cache=True)
def preencher_exp(Ef, Tnf, k1f, T1f):
    ny, nx = Tnf.shape

    for i in range(ny):
        for j in range(nx):
            Ef[i, j] = exp(k1f * (Tnf[i, j] - T1f))


@njit(fastmath=True, cache=True)
def solver(
    Tnf, Ff, T1f, nxf, nyf,
    a0f, a1f, a2f, a3f,
    k1f, qsf, qnf, qlf,
    dym1f, dxm1f,
    tolf, it_mf
):
    erro_g = 1.0
    it_g = 0

    Ef = np.empty_like(Tnf)
    preencher_exp(Ef, Tnf, k1f, T1f)

    while erro_g > tolf and it_g < it_mf:
        max_diff = 0.0

        denom_g = max_abs_matrix(Tnf)
        if denom_g < 1e-14:
            denom_g = 1.0

        # Sul + internos + norte
        for j in range(1, nxf - 1):
            # Sul
            fonte = (
                Ff[0, j]
                + a2f * (Ef[0, j + 1] + Ef[0, j - 1])
                + 2.0 * a3f * Ef[1, j]
                - 2.0 * qsf * dym1f
            )

            old = Tnf[0, j]
            new = resolve_newton(old, T1f, fonte, k1f, a0f, a1f, tolf, it_mf)

            Tnf[0, j] = new
            Ef[0, j] = exp(k1f * (new - T1f))

            diff = fabs(new - old)
            if diff > max_diff:
                max_diff = diff

            # Pontos internos
            for i in range(1, nyf - 1):
                fonte = (
                    Ff[i, j]
                    + a2f * (Ef[i, j + 1] + Ef[i, j - 1])
                    + a3f * (Ef[i + 1, j] + Ef[i - 1, j])
                )

                old = Tnf[i, j]
                new = resolve_newton(old, T1f, fonte, k1f, a0f, a1f, tolf, it_mf)

                Tnf[i, j] = new
                Ef[i, j] = exp(k1f * (new - T1f))

                diff = fabs(new - old)
                if diff > max_diff:
                    max_diff = diff

            # Norte
            i = nyf - 1

            fonte = (
                Ff[i, j]
                + a2f * (Ef[i, j + 1] + Ef[i, j - 1])
                + 2.0 * a3f * Ef[i - 1, j]
                - 2.0 * qnf * dym1f
            )

            old = Tnf[i, j]
            new = resolve_newton(old, T1f, fonte, k1f, a0f, a1f, tolf, it_mf)

            Tnf[i, j] = new
            Ef[i, j] = exp(k1f * (new - T1f))

            diff = fabs(new - old)
            if diff > max_diff:
                max_diff = diff

        # Sudeste
        j = nxf - 1

        fonte = (
            Ff[0, j]
            + 2.0 * a2f * Ef[0, j - 1]
            + 2.0 * a3f * Ef[1, j]
            - 2.0 * (qsf * dym1f + qlf * dxm1f)
        )

        old = Tnf[0, j]
        new = resolve_newton(old, T1f, fonte, k1f, a0f, a1f, tolf, it_mf)

        Tnf[0, j] = new
        Ef[0, j] = exp(k1f * (new - T1f))

        diff = fabs(new - old)
        if diff > max_diff:
            max_diff = diff

        # Leste
        for i in range(1, nyf - 1):
            fonte = (
                Ff[i, j]
                + 2.0 * a2f * Ef[i, j - 1]
                + a3f * (Ef[i + 1, j] + Ef[i - 1, j])
                - 2.0 * qlf * dxm1f
            )

            old = Tnf[i, j]
            new = resolve_newton(old, T1f, fonte, k1f, a0f, a1f, tolf, it_mf)

            Tnf[i, j] = new
            Ef[i, j] = exp(k1f * (new - T1f))

            diff = fabs(new - old)
            if diff > max_diff:
                max_diff = diff

        # Nordeste
        i = nyf - 1

        fonte = (
            Ff[i, j]
            + 2.0 * a2f * Ef[i, j - 1]
            + 2.0 * a3f * Ef[i - 1, j]
            - 2.0 * (qlf * dxm1f + qnf * dym1f)
        )

        old = Tnf[i, j]
        new = resolve_newton(old, T1f, fonte, k1f, a0f, a1f, tolf, it_mf)

        Tnf[i, j] = new
        Ef[i, j] = exp(k1f * (new - T1f))

        diff = fabs(new - old)
        if diff > max_diff:
            max_diff = diff

        it_g += 1
        erro_g = max_diff / denom_g

    return Tnf
