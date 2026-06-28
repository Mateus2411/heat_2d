"""
Arquivo de configuração visual para o heat_2d
==============================================
Mexe aqui pra mudar a aparência do gráfico sem bagunçar a simulação!
"""

import matplotlib.pyplot as plt

# ============================================================
# 1. COR DO MAPA DE CALOR (colormap)
# ============================================================
# Opções legais:
#   'coolwarm'  → azul gelado → vermelho quente (default)
#   'magma'     → preto → roxo → amarelo (intenso)
#   'viridis'   → roxo → verde → amarelo (daltônico-safe)
#   'inferno'   → preto → vermelho → amarelo claro
#   'plasma'    → roxo escuro → vermelho → amarelo
#   'jet'       → arco-íris (clássico mas engana视觉)
#   'hot'       → preto → vermelho → amarelo → branco
COLORMAP = 'coolwarm'

# ============================================================
# 2. CORES DA JANELA
# ============================================================
COR_FUNDO_FIGURA   = '#1a1a2e'   # fundo da janela inteira
COR_FUNDO_GRAFICO  = '#16213e'   # fundo da área do gráfico
COR_BORDA_SUPERIOR = None        # cor da borda de cima  (None = invisível)
COR_BORDA_INFERIOR = None        # cor da borda de baixo
COR_BORDA_ESQUERDA = None        # cor da borda esquerda
COR_BORDA_DIREITA  = None        # cor da borda direita
COR_TITULO         = '#e0e0e0'   # cor do texto do título
COR_GRADE          = '#0f3460'   # cor da grade (se ativada)
COR_BARRA          = '#e0e0e0'   # cor do texto e ticks da colorbar
COR_LABEL          = '#e0e0e0'   # cor dos labels dos eixos

# ============================================================
# 3. BORDAS (SPINES) - quais mostrar
# ============================================================
# True  = mostra a borda naquela posição
# False = esconde a borda
MOSTRAR_BORDA_SUPERIOR = False
MOSTRAR_BORDA_INFERIOR = False
MOSTRAR_BORDA_ESQUERDA = False
MOSTRAR_BORDA_DIREITA  = False

# ============================================================
# 4. GRADE
# ============================================================
MOSTRAR_GRADE = False          # True = liga a grade
GRADE_ESTILO  = '--'           # '-' sólida, '--' tracejada, ':' pontilhada

# ============================================================
# 5. TAMANHO DA JANELA
# ============================================================
LARGURA_JANELA = 8             # polegadas
ALTURA_JANELA  = 7             # polegadas

# ============================================================
# 6. TAMANHO DA FONTE
# ============================================================
TAMANHO_TITULO  = 14           # tamanho do título
TAMANHO_LABEL   = 10           # tamanho dos labels dos eixos
TAMANHO_TICK    = 8            # tamanho dos números dos eixos e colorbar

# ============================================================
# 7. INTERPOLAÇÃO (suaviza os pixels)
# ============================================================
# Opções:
#   'none'       → pixelado, mais rápido (bom pra muitos pontos)
#   'bilinear'   → suavizado, mais lento
#   'bicubic'    → bem suavizado, mais lento ainda
#   'spline16'   → suavizado de alta qualidade
INTERPOLACAO = 'spline16'

# ============================================================
# 8. TÍTULO DO GRÁFICO
# ============================================================
TITULO_TEXTO = "Mapa de Calor"

# ============================================================
# NÃO MEXE DAQUI PRA BAIXO - é a função que aplica tudo
# ============================================================
def configurar_figura():
    """Cria e configura a figura e os eixos com as opções acima."""
    fig, ax = plt.subplots(figsize=(LARGURA_JANELA, ALTURA_JANELA))

    # Cores de fundo
    fig.patch.set_facecolor(COR_FUNDO_FIGURA)
    ax.set_facecolor(COR_FUNDO_GRAFICO)

    # Bordas (spines)
    for spine_name, mostrar in [
        ('top',   MOSTRAR_BORDA_SUPERIOR),
        ('bottom', MOSTRAR_BORDA_INFERIOR),
        ('left',  MOSTRAR_BORDA_ESQUERDA),
        ('right', MOSTRAR_BORDA_DIREITA),
    ]:
        ax.spines[spine_name].set_visible(mostrar)

    # Cores das bordas que estão visíveis
    if MOSTRAR_BORDA_SUPERIOR and COR_BORDA_SUPERIOR:
        ax.spines['top'].set_color(COR_BORDA_SUPERIOR)
    if MOSTRAR_BORDA_INFERIOR and COR_BORDA_INFERIOR:
        ax.spines['bottom'].set_color(COR_BORDA_INFERIOR)
    if MOSTRAR_BORDA_ESQUERDA and COR_BORDA_ESQUERDA:
        ax.spines['left'].set_color(COR_BORDA_ESQUERDA)
    if MOSTRAR_BORDA_DIREITA and COR_BORDA_DIREITA:
        ax.spines['right'].set_color(COR_BORDA_DIREITA)

    # Cores dos ticks
    ax.tick_params(colors=COR_BARRA, labelsize=TAMANHO_TICK)

    # Labels dos eixos
    ax.xaxis.label.set_color(COR_LABEL)
    ax.yaxis.label.set_color(COR_LABEL)

    # Grade (só passa parâmetros se estiver ligada)
    if MOSTRAR_GRADE:
        ax.grid(True, linestyle=GRADE_ESTILO, color=COR_GRADE, alpha=0.3)
    else:
        ax.grid(False)

    return fig, ax


def configurar_colorbar(cbar):
    """Aplica estilo na barra de cores."""
    cbar.ax.tick_params(colors=COR_BARRA, labelsize=TAMANHO_TICK)
    cbar.outline.set_visible(False)  # tira a borda da barra


def criar_titulo(ax, texto_inicial):
    """Cria o título com a cor e tamanho configurados."""
    return ax.set_title(
        texto_inicial,
        color=COR_TITULO,
        fontsize=TAMANHO_TITULO,
        pad=10          # espaçamento entre título e gráfico
    )


def atualizar_titulo(titulo, texto):
    """Atualiza o texto do título."""
    titulo.set_text(texto)
