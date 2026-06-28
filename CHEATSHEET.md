# 🧠 Cola do Heat 2D — Simulação de Condução Térmica

> Tudo que você pode mexer, o que cada coisa faz, e como a mágica acontece

---

## 📐 1. PARÂMETROS NUMÉRICOS (no `main.py`)

| Variável | Default | O que controla | Efeito se aumentar 🔼 |
|----------|---------|----------------|----------------------|
| `nx` | 60 | Pontos na direção X (horizontal) | 🔸 **Mais resolução espacial** — bordas mais nítidas, mas **simulação mais lenta** (mais pontos pra calcular) |
| `ny` | 60 | Pontos na direção Y (vertical) | 🔸 Mesmo que `nx`, só que na vertical |
| `nt` | 160 | Número de frames (passos de tempo) | 🔸 **Animação mais suave/longa** — mais frames, mas demora mais pra computar |
| `lx` | 5.0 | Comprimento do domínio em X | 🔸 Domínio mais largo. A água esquenta/esfria numa área maior |
| `ly` | 5.0 | Altura do domínio em Y | 🔸 Domínio mais alto |
| `tf` | 10.0 | Tempo total da simulação (segundos) | 🔸 **Simulação mais longa** — o calor se espalha por mais tempo. Quanto maior `tf`, mais frames precisa pra mesma suavidade |
| `tol` | 1e-4 | Tolerância de erro do solver | 🔸 (diminuir) Mais preciso, mas mais iterações. 🔹 (aumentar) Mais rápido, mas menos preciso |
| `it_m` | 100 | Máximo de iterações por passo | 🔸 Solver tenta mais antes de desistir. Bom se tiver `tol` muito baixa |

### 🧮 Derivados (calculados automaticamente)

| Variável | Fórmula | O que é |
|----------|---------|---------|
| `dx` | `lx / nx` | Espaçamento entre pontos em X (resolução) |
| `dy` | `ly / ny` | Espaçamento entre pontos em Y |
| `dt` | `tf / (nt-1)` | Quanto tempo real cada frame representa |

> 💡 **Dica rápida:** Se a animação ficar muito rápida ou muito lenta, mexe em `nt` e `tf`. Se ficar pixelada, aumenta `nx`/`ny`.

---

## 🔥 2. PARÂMETROS FÍSICOS (no `main.py`)

| Variável | Default | O que controla | Efeito se aumentar 🔼 |
|----------|---------|----------------|----------------------|
| `rho` | 1.0 | Densidade do material | 🔸 Mais denso = mais inércia térmica, esquenta/esfria mais devagar |
| `cp` | 3.0 | Calor específico | 🔸 Armazena mais calor — mesma energia aumenta menos a temperatura |
| `k0` | 0.5 | Condutividade térmica base | 🔸 **Calor se espalha mais rápido** pelo material. Se `k0=0`, material é isolante |
| `k1` | 0.01 | Sensibilidade da condutividade à temperatura | 🔸 `k(T)` varia mais com a temperatura. **Efeito não-linear** mais forte |
| `T1` | 100.0 | Temperatura de referência pra `k(T)` | Onde a condutividade `k0` é medida. Desloca a curva exponencial |
| `qs` | -10.0 | Fluxo de calor na borda **Sul** | 🔸 **Positivo** (`>0`) → **perde calor** pelo sul. 🔹 **Negativo** (`<0`) → **ganha calor** pelo sul |
| `ql` | 10.0 | Fluxo de calor na borda **Leste** | 🔸 **Positivo** (`>0`) → **perde calor** pela direita. 🔹 **Negativo** (`<0`) → **ganha calor** pela direita |
| `qn` | 10.0 | Fluxo de calor na borda **Norte** | 🔸 **Positivo** (`>0`) → **perde calor** pelo topo. 🔹 **Negativo** (`<0`) → **ganha calor** pelo topo |
| `T0` | 20.0 | Temperatura inicial de todo o domínio | 🔸 Começa mais quente |
| `To` | 100.0 | Temperatura fixa na **parede Leste** | 🔸 Fonte de calor na borda direita |

### 🧪 Condutividade Térmica — `K(T) = k0 * exp(k1 * (T - T1))`

- `k0` é o valor base
- `k1 > 0` → material conduz **melhor** quando **mais quente** (metal)
- `k1 < 0` → material conduz **melhor** quando **mais frio** (alguns semicondutores)
- `k1 = 0` → condutividade **constante** (simulação linear, mais rápida)

### 🔄 Por que positivo = perde calor?

No código, os fluxos aparecem como `-2.0 * qs * dym1f` na equação:

```python
fonte = ... - 2.0*qsf*dym1f    # (linha 29 do functions.py)
```

O sinal de **menos** na frente faz com que:
- `qs > 0` → `-2.0*qs*...` = termo **negativo** → **remove calor** (resfriamento)
- `qs < 0` → `-2.0*(-10)*...` = `+20*...` = **adiciona calor** (aquecimento)

É uma convenção de sinal comum em CFD: fluxo **positivo** = calor **saindo** do domínio (derivada apontando pra fora).

### 🔌 Fonte de Calor Interna — `calcula_Q()` (no `functions.py`)

Distribuição espacial que varia no tempo:
```
Q(x, y, t) = 3*t*exp(-t) * (1 + 5x + y + 10xy)
```
- Começa fraca, cresce até `t ≈ 1`, depois decai (pulso de calor)
- Mais intensa nos cantos X e Y grandes (canto Nordeste)

---

## ⚙️ 3. CONFIGURAÇÃO VISUAL (no `viz_config.py`)

### 🎨 Cores

| Variável | Default | O que faz |
|----------|---------|-----------|
| `COLORMAP` | `'coolwarm'` | Paleta de cores do mapa de calor |
| `COR_FUNDO_FIGURA` | `'#1a1a2e'` | Fundo da janela inteira |
| `COR_FUNDO_GRAFICO` | `'#16213e'` | Fundo da área do gráfico |
| `COR_TITULO` | `'#e0e0e0'` | Cor do título |
| `COR_GRADE` | `'#0f3460'` | Cor da grade (se ligada) |
| `COR_BARRA` | `'#e0e0e0'` | Texto e números da colorbar |
| `COR_LABEL` | `'#e0e0e0'` | Labels dos eixos X/Y |

### 📐 Layout

| Variável | Default | O que faz |
|----------|---------|-----------|
| `LARGURA_JANELA` | 8 | Largura da figura em polegadas |
| `ALTURA_JANELA` | 7 | Altura da figura em polegadas |
| `TAMANHO_TITULO` | 14 | Tamanho da fonte do título |
| `TAMANHO_LABEL` | 10 | Tamanho dos labels dos eixos |
| `TAMANHO_TICK` | 8 | Tamanho dos números nos eixos |

### 🔲 Bordas & Grade

| Variável | Default | O que faz |
|----------|---------|-----------|
| `MOSTRAR_BORDA_SUPERIOR` | `False` | Mostra borda no topo |
| `MOSTRAR_BORDA_INFERIOR` | `False` | Mostra borda embaixo |
| `MOSTRAR_BORDA_ESQUERDA` | `False` | Mostra borda à esquerda |
| `MOSTRAR_BORDA_DIREITA` | `False` | Mostra borda à direita |
| `MOSTRAR_GRADE` | `False` | Liga a grade |
| `GRADE_ESTILO` | `'--'` | Estilo da linha: `'-'` sólida, `'--'` tracejada, `':'` pontilhada |

### 🖼️ Interpolação

| Opção | Efeito |
|-------|--------|
| `'none'` | Pixelado, mais rápido (bom pra muitos pontos) |
| `'bilinear'` | Suavizado |
| `'bicubic'` | Bem suavizado |
| `'spline16'` | Alta qualidade |

### 🎯 Colormaps legais pra testar

| Nome | Visual |
|------|--------|
| `'coolwarm'` | Azul ↔ Vermelho (neutro no meio) |
| `'magma'` | Preto → Roxo → Amarelo (intenso) |
| `'viridis'` | Roxo → Verde → Amarelo (daltônico-safe) |
| `'inferno'` | Preto → Vermelho → Amarelo |
| `'plasma'` | Roxo escuro → Vermelho → Amarelo |
| `'hot'` | Preto → Vermelho → Amarelo → Branco |
| `'jet'` | Arco-íris (clássico, pode enganar visualmente) |

---

## 🎬 4. COMO A ANIMAÇÃO FUNCIONA

### Fase 1 — Computação (~ silenciosa ~)

```
for k in 1..nt-1:
    calcula fonte de calor Q no tempo k
    monta vetor fonte F = a0*T + Q
    solver(T_n, F) → resolve sistema não-linear (Newton)
    guarda T no tensor T_g[:, :, k]
```

- O `solver()` usa **Newton-Raphson** dentro de um **loop global** (Gauss-Seidel-like)
- Percorre: Sul → Pontos Internos → Norte → Sudeste → Leste → Nordeste
- Aplica as condições de contorno de fluxo (`qs`, `ql`, `qn`) nas bordas
- A parede **Leste** (`j = nx-1`) tem temperatura **fixa** `To`
- Critério de parada do solver global: `erro < tol` ou `it > it_m`
- No final, `T_g` é um tensor 3D: `[y, x, tempo]` — todos os frames pré-computados

### Fase 2 — Renderização (animação suave)

```
ani = FuncAnimation(fig, atualizar, frames=nt, interval=80, blit=True)
```

- `atualizar(k)`: troca os dados da imagem `im.set_data(T_g[:,:,k])` e atualiza o título com o tempo atual
- `interval=80`: **80ms entre frames** (~12.5 FPS)
- `blit=True`: só redesenha o que mudou (mais rápido)
- `vmin=T0, vmax=To`: escala de cores fixa (não adaptativa) — a cor não "foge" conforme a temperatura muda

### ⏱️ Duração real da animação

```
duração_real = nt * interval / 1000
Ex: 160 frames * 80ms = 12.8 segundos
```

Se `tf` for 10s com `nt=160`, cada frame representa `dt = 10/159 ≈ 0.063s`.

---

## 🧪 5. EXPERIMENTOS RÁPIDOS PRA TESTAR

### 🔹 Mais suave e lento
```
nx = 100, ny = 100   # mais resolução
nt = 300              # mais frames
interval = 120        # mais lento (no viz_config ou alterando)
```

### 🔹 Mais rápido pra debug
```
nx = 30, ny = 30     # menos pontos
nt = 60              # menos frames
```

### 🔹 Material isolante
```
k0 = 0.01            # quase não conduz
k1 = 0.0             # linear (mais rápido)
```

### 🔹 Material super condutor
```
k0 = 5.0             # espalha rápido
```

### 🔹 Explosão de calor nas bordas (quentura!)
```
qs = -50, ql = -50, qn = -50   # negativo → CALOR ENTRA pelos lados
```

### 🔹 Só parede quente, sem fluxo extra
```
qs = 0, ql = 0, qn = 0      # só a parede Leste aquece
```

### 🔹 Esfriando (perdendo calor)
```
qs = 50, ql = 50, qn = 50  # positivo → CALOR SAI pelas bordas
```

---

## 🚀 6. COMO RODAR

```bash
# Ativar venv e rodar
source .venv/Scripts/activate
python main.py
```

> A simulação roda em 2 fases:
> 1. **Computação** — prints de progresso (frame a frame)
> 2. **Animação** — janela matplotlib com o vídeo

---

## ⚠️ 7. PITFALLS (coisas que podem dar errado)

| Problema | Causa | Solução |
|----------|-------|---------|
| Animação muito rápida | `interval` pequeno ou `nt` baixo | Aumenta `nt` ou `interval` |
| Animação muito lenta | `interval` grande ou `nt` alto | Diminui `nt` ou `interval` |
| Tudo da mesma cor | `vmax` muito alto pra temperatura real | Ajusta `vmax` pra temperatura máxima que aparece |
| Cores estouram | `vmin`/`vmax` mal dimensionados | Muda `vmax` pro máximo real dos dados |
| Demora séculos pra rodar | `nx, ny` altos + `nt` alto | Reduz pra 30×30×60 pra testar |
| Solver não converge | `it_m` baixo ou `tol` apertada demais | Aumenta `it_m` ou afrouxa `tol` |
| Erro NaN/inf | Parâmetro físico muito extremo | Verifica `k0, k1, qs, ql, qn` |
| Gradiente explode | `k1` muito alto com temperaturas altas | Reduz `k1` ou aumenta `T1` |

---

