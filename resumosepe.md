Desenvolvimento de um simulador do processo de condução de calor não linear bidimensional em regime transiente
	 	
Equipe:
Colocar o nome de cada um de vocês
Mateus Henrique da Silva 
Davi…
Fábio …
Adriano Rodrigues de Melo

RESUMO

Métodos numéricos são determinantes para a compreensão de problemas reais das engenharias e das ciências, dado que geralmente são ferramentas acessíveis para obter sua solução. Este trabalho trata do desenvolvimento de um simulador numérico da transferência de calor por condução em uma placa 2D, com condutividade térmica dependente exponencialmente da temperatura (caso típico em materiais semicondutores). Os métodos computacionais utilizados foram diferenças finitas centrais (no espaço), Euler (no tempo), Gauss-Seidel não linear e Newton (para a construção do solver). O código-fonte, implementado em Python, recebeu melhorias para reduzir o tempo de execução, com destaque para o uso da biblioteca Numba. O simulador, embora ainda demande melhorias em sua interface, já possui visualização gráfica e execução relativamente rápida.

Palavras-chave: Simulação numérica; numba; semicondutores.


1 INTRODUÇÃO

Muitos problemas das ciências e das engenharias são modelados por equações diferenciais parciais (EDP), cuja solução só é viável por meio de métodos computacionais. A resolução por métodos numéricos transforma o modelo contínuo (EDP), num modelo discreto (equações algébricas). Essa transformação, também chamada de discretização, leva à produção de sistemas algébricos, nos quais a matriz associada é normalmente de grande porte e esparsa.
Nesses sistemas, métodos diretos (aqueles que promovem resolução exata) podem se tornar inconvenientes ou mesmo inviáveis, pois, durante sua aplicação, costumam produzir muitas entradas não nulas (QUARTERONI et al., 2000). Neste caso, métodos iterativos ou aproximados são mais indicados, tendo em vista sua eficiência em termos de armazenamento e de computação (BURDEN; FAIRES, 2011). Entretanto, tais métodos iterativos têm boa convergência apenas no início do processo e tendem a perder eficiência no decorrer das iterações (BRIGGS et al., 2000; TROTTENBERG et al., 2001).
A equação do calor não linear é um modelo que possui diversas aplicações nas ciências dos materiais (ZHANG et al., 2022), como na produção de microchips (FILIPOV et al., 2023), na indústria aeroespacial moderna (KUMAR et al., 2013) e na engenharia mecânica (BAGHERIZADEH et al., 2011). Quando a condutividade térmica depende da temperatura, a EDP se torna não linear. Nesse caso, é comum aplicar algum método de linearização, como Newton ou Picard (BURDEN; FAIRES, 2011), para a solução do sistema não linear resultante da discretização. Métodos não lineares também são viáveis e podem produzir bons resultados, mas padecem do mesmo problema de perder eficiência no decorrer das iterações (ZEN et al., 2025).
Este trabalho teve o objetivo de desenvolver um simulador para o problema de condução de calor não linear numa região retangular, buscando melhorar seu tempo de execução a partir da ferramenta de aceleração Numba, da linguagem de programação Python.

2 METODOLOGIA

O trabalho, ainda em andamento, teve início em março de 2026, em parceria com a Fábrica de Software. Conta com a participação de dois estudantes do Curso Técnico em Informática para Internet e dois docentes do IFC, Campus Araquari.
O código base foi desenvolvido segundo um modelo composto pela EDP do calor com condutividade térmica exponencial, típica em materiais semicondutores (RENCZ; SZEKELY, 2004), com temperatura prescrita no contorno esquerdo (condição de Dirichlet) e fluxo de calor prescrito nas demais fronteiras (condições de Neumann), além de uma fonte de calor.
Para a discretização, utilizou-se o método das diferenças finitas de segunda ordem no espaço e o método de Euler no tempo. O sistema não linear é resolvido pelo método iterativo de Gauss-Seidel não linear, com o método de Newton incorporado a cada iteração. Utiliza-se um duplo critério de convergência em ambos os processos iterativos, que consiste em um número máximo de iterações e em uma tolerância mínima para a razão entre as normas da diferença entre os iterados subsequentes e a norma da estimativa inicial.
Esse código-base, implementado na linguagem de programação Python, foi encaminhado à Fábrica de Software para o desenvolvimento de uma interface. A aceleração foi realizada por meio da ferramenta Numba, um compilador just-in-time que traduz funções Python e loops numéricos para código de máquina durante a execução (NUMBA DEVELOPERS, 2026).

3 RESULTADOS E DISCUSSÕES

O método das diferenças finitas traduz o modelo contínuo em esquemas de passos no tempo. O domínio retangular de dimensões L por M é dividido uniformemente em (n+1).(m+1) blocos menores de tamanhos L/n por M/m, enquanto que a linha temporal é subdividida em T/k, em que T é o tempo de simulação e k é o número de frames. Com esse processo de discretização, o número de incógnitas se expressa como n.(m+1).k (apenas o contorno esquerdo é conhecido). Ou seja, basta uma discretização grosseira, com n = m = k = 100, por exemplo, para levar o número de incógnitas a superar a casa dos milhões. Não suficiente, cada incógnita é visitada várias vezes, tanto no nível das iterações de Gauss-Seidel quanto das linearizações de Newton.
Todas as observações anteriores foram feitas para justificar a importância da aceleração promovida pelo uso da biblioteca Numba e das demais estratégias utilizadas para otimizar o código, como a vetorização do cálculo da fonte de calor, o pré-cálculo das exponenciais, o reaproveitamento da estimativa anterior e a separação entre a simulação e a renderização. Para efeito de comparação, uma simulação executada em 35 minutos, com as modificações, passou a ser executada em media 5 minutos.

4 CONSIDERAÇÕES FINAIS
Este trabalho teve o objetivo de desenvolver um simulador do processo de condução de calor bidimensional em regime transiente, com condutividade térmica dependente da temperatura, na perspectiva de melhorar seu tempo de execução. O código foi implementado na linguagem Python, que permitiu o uso da biblioteca Numba para acelerar o tempo de execução. O simulador possui visualização gráfica e é razoavelmente rápido em malhas intermediárias. Pontos de melhoria incluem aperfeiçoar a interface gráfica, modificar as condições de contorno para Robin (que são mais realistas que as de Neumann) e melhorar o solver com o acelerador de convergência multigrid.

5 REFERÊNCIAS

BAGHERIZADEH, E.; KIANI, Y.; ESLAMI, M. Mechanical buckling of functionally graded material cylindrical shells surrounded by pasternak elastic foundation. Composite Structures, v. 93, n. 11, p. 30633071, 2011. ISSN 0263-8223.

BRIGSS, W. L.; HENSON, V. E.; MCCORMICK, S. F. A Multigrid Tutorial, 2nd Edition, SIAM, Philadelphia, 2000.
BURDEN, R. L.; FAIRES, J. D. Numerical Analysis. 9nd. ed. Boston: Cengage Learning, 2011.

FILIPOV, S.; HRISTOV, J.; AVDZHIEVA, A.; FARAGÓ, I. A coupled PDE-ODE model for nonlinear transient heat transfer with convection heating at the boundary: Numerical solution by implicit time discretization and sequential decoupling. Axioms, v. 12, n. 4, 2023.

KUMAR, S.; Murthy Reddy, K.; KUMAR, A.; Rohini Devi, G. Development and characterization of polymerceramic continuous fiber reinforced functionally graded composites for aerospace application. Aerospace Science and Technology, v. 26, n. 1, p. 185191, 2013.

NUMBA DEVELOPERS. Numba Documentation. Versão 0.67.0. 2026. Disponível em: https://numba.pydata.org/. Acesso em: 15 set. 2026.

QUARTERONI, A.; SACCO, R.; SALERI, F. Numerical mathematics. New York: Springer-Verlag, 2000.

RENCZ, M.; SZEKELY, V. Studies on the nonlinearity effects in dynamic compact model generation of packages. IEEE Transactions on Components and Packaging Technologies, v. 27, n. 1, p. 124130, 2004.

TROTTENBERG, U.; OOSTERLEE, C.; SCHÜLLER, A. Multigrid, Academic Press, San Diego, 2001.

ZEN, P. D., PINTO, M .A. V., FRANCO, S. R.: A multigrid waveform relaxation method for solving the nonlinear silicon problem with relaxing boundary conditions. Numerical Heat Transfer, Part B: Fundamentals, v. 86, n. 9, p. 30023017, 2025.

ZHANG, Y.; RABCZUK, T.; LU, J.; LIN, S.; LIN, J. Space-time backward substitution method for nonlinear transient heat conduction problems in functionally graded materials. Computers & Mathematics with Applications, v. 124, p. 98110, 2022.
