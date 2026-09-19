# Functions — Heat 2D

## Visão Geral

O `functions.py` contém o coração numérico da simulação de transferência de calor 2D. Ele resolve a **equação do calor não-linear** com condutividade térmica dependente da temperatura:

\[
\rho c_p \frac{\partial T}{\partial t} = \nabla \cdot \big( k(T) \nabla T \big) + Q
\]

Onde \( k(T) = k_0 e^{k_1 (T - T_1)} \) — a condutividade varia exponencialmente com a temperatura.

---

## `calcula_Q(Qf, temp, xf, yf, nxf, nyf)`

**O que faz:** Calcula o termo fonte \( Q \) (geração interna de calor) em cada ponto da malha.

```python
Qf[:, :] = 3.0 * temp * np.exp(-temp) * (1.0 + 5.0*X + Y + 10.0*X*Y)
```

- `temp` = instante de tempo atual (`k*dt`)
- `X, Y` = coordenadas normalizadas via broadcasting (`xf[None, :]` e `yf[:, None]`)
- O termo fonte é **não-homogêneo** no espaço (depende de x e y) e **decai exponencialmente** no tempo com `temp * exp(-temp)`

**Por que vetorizado:** Usa broadcasting do NumPy em vez de loops `for` — resolve a matriz inteira de uma vez, ~10x mais rápido que a versão com loops.

---

## `max_abs_matrix(A)`

**O que faz:** Calcula a **norma do máximo** (norma infinito) de uma matriz — o maior valor absoluto entre todos os elementos.

```python
for i in range(ny):
    for j in range(nx):
        v = fabs(A[i, j])
        if v > m: m = v
```

**Por que Numba:** `np.max(np.abs(A))` aloca duas matrizes temporárias (uma pro `abs`, uma pro `max`). Essa versão percorre uma vez só, sem alocar nada. Economia de memória e cache.

**Uso:** Usada no `solver` como denominador do critério de parada.

---

## `resolve_newton(Tnf, T1f, fontef, k1f, a0f, a1f, tolf, it_mf)`

**O que faz:** Resolve a **equação não-linear local** em um único ponto usando o método de **Newton-Raphson**.

A equação que ela resolve vem da discretização:

\[
G(T) = a_0 T + a_1 e^{k_1 (T - T_1)} = \text{fonte}
\]

E o chute de Newton:

\[
T^{n+1} = T^n + \frac{\text{fonte} - G(T^n)}{a_0 + k_1 a_1 e^{k_1 (T - T_1)}}
\]

**Detalhes importantes:**

- Usa `math.exp()` escalar — **sem alocar array**, cada chamada é uma exponencial só
- Divide o erro por `|Tn0|` (normalização relativa) — se o valor inicial for zero, usa 1.0 pra não dividir por zero
- O loop interno usa `fabs()` do C (`math.fabs`)

**Por que Numba:** Esse cálculo é chamado ~**O(nx × ny × iterações)** vezes. Cada exponencial numpy custa overhead de chamada de função Python. Com `@njit`, vira uma chamada de função C pura.

---

## `preencher_exp(Ef, Tnf, k1f, T1f)`

**O que faz:** Pré-computa a matriz de exponenciais \( E = e^{k_1 (T - T_1)} \) para **toda a malha**.

```python
for i in range(ny):
    for j in range(nx):
        Ef[i, j] = exp(k1f * (Tnf[i, j] - T1f))
```

**Por que uma função separada:** As exponenciais reaparecem em várias fórmulas no solver. Em vez de recalcular `np.exp(k1*(T[i,j+1]-T1))` cada vez que precisa, calcula uma vez e reusa. Aumenta a **localidade de dados** — as exponenciais ficam em cache.

---

## `solver(Tnf, Ff, T1f, nxf, nyf, a0f, a1f, a2f, a3f, k1f, qsf, qnf, qlf, dym1f, dxm1f, tolf, it_mf)`

**O que faz:** O **coração da simulação** — resolve o sistema algébrico não-linear acoplado ponto a ponto usando o método de **Gauss-Seidel não-linear**.

### Algoritmo

```
1. Pré-computa matriz de exponenciais E = exp(k1*(T - T1))
2. Enquanto erro > tol e it < it_max:
   a. Para cada coluna j (1 até nx-2):
      - Sul:     resolve Newton (ponto [0,j])     com cond. contorno qs
      - Interno: resolve Newton (pontos [i,j])     sem cond. contorno
      - Norte:   resolve Newton (ponto [ny-1,j])   com cond. contorno qn
   b. Canto Sudeste:  resolve Newton c/ qs + ql
   c. Leste:          resolve Newton c/ ql
   d. Canto Nordeste: resolve Newton c/ ql + qn
   e. Atualiza erro = max_diff / denom_g
```

### Discretização

Usa **diferenças finitas centradas** no espaço e **Euler implícito** no tempo. A equação discretizada num ponto interior é:

\[
a_0 T_{i,j} + a_1 e^{k_1(T_{i,j} - T_1)} = F_{i,j} + a_2 (E_{i,j+1} + E_{i,j-1}) + a_3 (E_{i+1,j} + E_{i-1,j})
\]

Onde:
- \( a_0 = \rho c_p / \Delta t \) — termo temporal
- \( a_1 = 2 \left( \frac{k_0}{k_1 \Delta x^2} + \frac{k_0}{k_1 \Delta y^2} \right) \) — coeficiente do termo não-linear
- \( a_2 = \frac{k_0}{k_1 \Delta x^2} \) — coeficiente dos vizinhos em x
- \( a_3 = \frac{k_0}{k_1 \Delta y^2} \) — coeficiente dos vizinhos em y

### Condições de Contorno

São aplicadas **explicitamente** no lado direito da equação (como fonte extra) usando **Neumann** (fluxo prescrito):

| Fronteira | Fluxo | Termo adicional |
|-----------|-------|-----------------|
| Sul (y=0) | `qs` | `-2 * qs * Δy⁻¹` |
| Norte (y=ly) | `qn` | `-2 * qn * Δy⁻¹` |
| Leste (x=lx) | `ql` | `-2 * ql * Δx⁻¹` |
| Cantos | qs+ql, ql+qn | Soma dos dois termos |

Valores negativos de `qs` = **entra** calor, positivos = **sai** calor.

### Critério de Parada

\[
\text{erro} = \frac{\max_{i,j} |T_{i,j}^{new} - T_{i,j}^{old}|}{\max_{i,j} |T_{i,j}^{new}|}
\]

Erro relativo baseado na **variação máxima** entre iterações. Mais robusto que erro absoluto quando a temperatura escala.

### Por que Gauss-Seidel em vez de resolver matriz?

O sistema é **não-linear** por causa do termo \( e^{k_1 (T - T_1)} \). Não dá pra montar uma matriz \( A x = b \) e resolver direto. Gauss-Seidel não-linear + Newton-Raphson local é o padrão para esse tipo de problema — cada ponto resolve sua não-linearidade local com Newton enquanto "enxerga" os vizinhos.

### Por que Numba é crucial aqui

O `solver` tem **3 loops aninhados**: colunas × linhas × iterações externas. Cada iteração externa percorre todos os \( n_x \times n_y \) pontos. Para uma malha 100×100 com ~10 iterações externas, são **100 mil chamadas** a funções. `@njit` compila tudo pra código de máquina — sem interpretador Python atrapalhando.

---

## Fluxo de Execução

```
main.py (loop temporal)
  │
  ├─ calcula_Q(...)          ← termo fonte no instante t
  ├─ F = a0*T + Q            ← monta lado direito
  └─ solver(T_n, F, ...)
       │
       ├─ preencher_exp()    ← E = exp(k1*(T - T1))
       │
       └─ [loop Gauss-Seidel]
            │
            ├─ resolve_newton()  ← Sul
            ├─ resolve_newton()  ← Internos
            ├─ resolve_newton()  ← Norte
            ├─ resolve_newton()  ← Sudeste
            ├─ resolve_newton()  ← Leste
            └─ resolve_newton()  ← Nordeste
```

---

## Sobre o Numba

O `@njit(fastmath=True, cache=True)` faz:

- **`@njit`** = "no-Python mode" — compila a função inteira pra LLVM IR e depois pra código de máquina
- **`fastmath=True`** — permite reordenar operações e usar instruções SIMD (como AVX/SSE), trocando precisão máxima por ~2× de velocidade
- **`cache=True`** — salva o código compilado em disco (`__pycache__`). Na segunda execução, zero tempo de compilação

As funções Numba **não podem** chamar NumPy (a não ser funções suportadas como `np.empty_like`) — por isso os loops manuais e `math.exp` em vez de `np.exp`.
