# heat_2d

Simulacao bidimensional da transferencia de calor por conducao em uma placa. A condutividade termica depende da temperatura por uma relacao exponencial:

`K(T) = k0 * exp(k1 * (T - T1))`

## Mapa do projeto

| Arquivo | Responsabilidade |
| --- | --- |
| `main.py` | Define os parametros numericos e fisicos, inicializa os campos, executa a marcha no tempo e exibe o mapa de temperatura final. |
| `functions.py` | Implementa o termo fonte (`calcula_Q`), o solver local de Newton (`resolve_newton`) e o solver iterativo global (`solver`). |
| `requirements.txt` | Dependencias externas necessarias para executar o modelo. |
| `setup.ps1` | Cria o ambiente virtual, instala as dependencias e executa a simulacao no Windows. |
| `.gitignore` | Evita versionar ambiente virtual, caches, logs e arquivos locais. |

## Fluxo numerico

1. `main.py` cria a malha espacial e temporal.
2. O campo inicial recebe `T0`; a borda oeste recebe `To`.
3. Para cada passo de tempo, `calcula_Q` atualiza a fonte espacial.
4. `solver` percorre as bordas e os pontos internos usando Gauss-Seidel.
5. Cada ponto e atualizado por `resolve_newton` para tratar a nao linearidade de `K(T)`.
6. O resultado do ultimo passo e exibido com `matplotlib`.

## Parametros ajustaveis

Os valores ficam no inicio de `main.py`.

| Grupo | Parametros |
| --- | --- |
| Numerico | `nx`, `ny`, `nt`, `lx`, `ly`, `tf`, `tol`, `it_m` |
| Propriedades | `rho`, `cp`, `k0`, `k1`, `T1` |
| Contorno | `qs`, `ql`, `qn` |
| Inicializacao | `T0`, `To` |

Diminuir `tol` aumenta a precisao e pode aumentar o tempo de execucao. Aumentar `nx`, `ny` ou `nt` aumenta a resolucao da simulacao.

## Requisitos

- Windows PowerShell 5+ ou PowerShell 7+
- Python 3.10 ou superior
- Acesso a internet na primeira instalacao das dependencias

## Execucao automatica no Windows

Abra o PowerShell na pasta do projeto e execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\setup.ps1
```

O script procura Python no PATH, cria `.venv` se necessario, atualiza o `pip`, instala `requirements.txt` e executa `main.py`. A janela com o mapa de calor aparece ao final.

Para apenas preparar o ambiente sem executar a simulacao:

```powershell
.\setup.ps1 -SkipRun
```

## Execucao manual

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Estrutura esperada

```text
heat_2d/
|-- functions.py
|-- main.py
|-- requirements.txt
|-- setup.ps1
|-- README.md
`-- .gitignore
```

## Validacao rapida

Para verificar o solver em uma sessao sem abrir janela grafica:

```powershell
$env:MPLBACKEND = "Agg"
.\.venv\Scripts\python.exe .\main.py
```

Esse comando deve finalizar com um aviso do `matplotlib` sobre `plt.show()` nao interativo; o aviso e esperado nesse modo.
