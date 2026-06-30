"""
Arquivo de configuração visual para o heat_2d
==============================================
Mexe aqui pra mudar a aparência do gráfico sem bagunçar a simulação!
"""

import sys
import ctypes
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
COR_FUNDO_BARRA    = '#1a1a2e'   # fundo do eixo da colorbar (pra não destoar)
COR_LABEL          = '#e0e0e0'   # cor dos labels dos eixos
PADDING_SUPERIOR   = 0.95        # posição do topo da área do gráfico (0-1)
PADDING_INFERIOR   = 0.08        # posição da base (pra footer não ficar claro)
PADDING_ESQUERDO   = 0.10        # posição da esquerda
PADDING_DIREITO    = 0.90        # posição da direita (pra incluir a colorbar)
COR_TICK_CBAR      = '#e0e0e0'   # cor dos números da barra de calor

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

    # Ajuste do layout pra header e footer ficarem escuros também
    fig.subplots_adjust(
        top=PADDING_SUPERIOR,
        bottom=PADDING_INFERIOR,
        left=PADDING_ESQUERDO,
        right=PADDING_DIREITO
    )

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
    cbar.ax.tick_params(colors=COR_TICK_CBAR, labelsize=TAMANHO_TICK)
    cbar.outline.set_visible(False)  # tira a borda da barra
    cbar.ax.set_facecolor(COR_FUNDO_BARRA)  # fundo da barra escuro tb


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


def configurar_janela(fig):
    """
    Aplica tema escuro na janela INTEIRA:
    - Barra de título (minimizar/maximizar/fechar) no Windows 10/11
    - Toolbar inferior (Home, Pan, Zoom, etc.)
    - Fundo da janela
    """
    try:
        fm = fig.canvas.manager
        janela = fm.window

        # ── 1. Barra de título escura (Windows 10/11 via DWM API) ──
        if sys.platform == 'win32':
            try:
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                hwnd = ctypes.windll.user32.GetParent(janela.winfo_id())
                valor = ctypes.c_int(1)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                    ctypes.byref(valor), ctypes.sizeof(valor))
            except Exception:
                pass  # versão do Windows sem suporte → ignora

        # ── 2. Fundo da janela ──
        janela.config(bg=COR_FUNDO_FIGURA)

        # ── 3. Toolbar inferior escura ──
        tb = fm.toolbar
        if tb:
            tb.config(bg='#1a1a2e')
            for child in tb.winfo_children():
                try:
                    child.config(bg='#1a1a2e', fg='#ffffff')
                except Exception:
                    pass
            # labels dos botões (Message widgets)
            try:
                for msg in tb.winfo_children():
                    if 'message' in str(msg.winfo_class()).lower():
                        msg.config(bg='#1a1a2e', fg='#ffffff')
            except Exception:
                pass

    except Exception:
        pass  # seguro — se falhar, a simulação roda normal
