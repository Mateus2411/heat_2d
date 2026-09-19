# heat_2d

Simulacao bidimensional da transferencia de calor por conducao em uma placa. A condutividade termica depende da temperatura por uma relacao exponencial:

`K(T) = k0 * exp(k1 * (T - T1))`

## Melhorias desta branch

- Fonte de calor vetorizada com broadcasting do NumPy.
- Solver numerico compilado com Numba usando `@njit`.
- Pre-calculo e reutilizacao da matriz de exponenciais durante o solver.
- Critério de convergencia baseado na maior variacao relativa da malha.
- Simulacao temporal com armazenamento dos frames para animacao.
- Animacao do mapa de calor com titulo atualizado a cada instante.
- Configuracao visual isolada em `viz_config.py`, incluindo tema, cores, interpolacao e janela.
- Indicacao do progresso e do tempo total da simulacao no terminal.

## Mapa do projeto

| Arquivo | Responsabilidade |
| --- | --- |
| `main.py` | Define os parametros, executa a marcha temporal, armazena os frames e reproduz a animacao. |
| `functions.py` | Calcula a fonte, preenche exponenciais e resolve o sistema nao-linear com Newton, Gauss-Seidel e Numba. |
| `viz_config.py` | Centraliza o estilo da visualizacao e tenta aplicar tema escuro na janela do Windows. |
| `CHEATSHEET.md` | Explica os parametros, a discretizacao, o solver e os pontos de configuracao. |
| `requirements.txt` | Dependencias externas fixadas para reproduzir o ambiente funcional. |
| `setup.ps1` | Cria o ambiente virtual, instala as dependencias e executa a simulacao no Windows. |
| `setup.sh` | Cria o ambiente virtual, instala as dependencias e executa a simulacao no Linux. |
| `.gitignore` | Evita versionar ambientes virtuais, caches, logs e arquivos locais. |

## Fluxo numerico

1. `main.py` cria a malha espacial e temporal.
2. O campo inicial recebe `T0`; a borda oeste recebe `To`.
3. Para cada instante, `calcula_Q` atualiza a fonte espacial de forma vetorizada.
4. `solver` atualiza bordas e pontos internos com Gauss-Seidel nao-linear.
5. `resolve_newton` resolve a equacao nao-linear de cada ponto.
6. Numba compila os loops numericos para reduzir o custo do Python.
7. Os resultados sao armazenados em `T_g` e usados pela animacao.

## Parametros ajustaveis

Os valores ficam no inicio de `main.py`.

| Grupo | Parametros |
| --- | --- |
| Numerico | `nx`, `ny`, `nt`, `lx`, `ly`, `tf`, `tol`, `it_m` |
| Propriedades | `rho`, `cp`, `k0`, `k1`, `T1` |
| Contorno | `qs`, `ql`, `qn` |
| Inicializacao | `T0`, `To` |
| Visual | Constantes de `viz_config.py` |

`qs` negativo representa entrada de calor. Valores positivos em `ql` e `qn` representam perda de calor conforme as convencoes do solver.

Aumentar `nx`, `ny` ou `nt` melhora a resolucao, mas aumenta memoria e tempo. A primeira execucao pode ser mais lenta porque o Numba compila e armazena o cache das funcoes.

## Requisitos

- Windows PowerShell 5+ ou PowerShell 7+
- Linux com Bash
- Python 3.11 ou superior
- Acesso a internet na primeira instalacao das dependencias

## Execucao automatica no Windows

Abra o PowerShell na pasta do projeto e execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\setup.ps1
```

O script procura Python no PATH, cria `.venv` se necessario, atualiza o `pip`, instala `requirements.txt` e executa `main.py`.

Para apenas preparar o ambiente sem iniciar a animacao:

```powershell
.\setup.ps1 -SkipRun
```

## Execucao automatica no Linux

Na pasta do projeto, de permissao ao script e execute:

```bash
chmod +x setup.sh
./setup.sh
```

Para apenas preparar o ambiente sem iniciar a animacao:

```bash
./setup.sh --skip-run
```

## Execucao manual

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

No Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

## Estrutura esperada

```text
heat_2d/
|-- functions.py
|-- main.py
|-- viz_config.py
|-- CHEATSHEET.md
|-- requirements.txt
|-- setup.ps1
|-- setup.sh
|-- README.md
`-- .gitignore
```

## Validacao sem janela

Para verificar a simulacao em um ambiente sem interface grafica:

```powershell
$env:MPLBACKEND = "Agg"
.\.venv\Scripts\python.exe .\main.py
```

Nesse modo o calculo e executado, mas o `plt.show()` gera um aviso esperado porque nao existe uma janela interativa para exibir a animacao.
