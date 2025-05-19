📌 Status do Projeto:
•	Login automatizado ✅
•	Navegação até CDA automatizada ✅
•	Busca e download de CDA funcionando ✅
•	Preparado para próxima etapa: loop de múltiplas CDAs 🔄

📋 Resumo do Dia (28/04/2025)

•	Finalizamos a instalação do Python e do Selenium.
•	Organizamos a estrutura de pastas para o projeto.
•	Criamos e executamos com sucesso o primeiro script Selenium (abrir e fechar o navegador).
•	Entendemos a diferença entre Classe e Objeto em Python.
•	Analisamos e planejamos toda a navegação no site da dívida ativa:
    o	Clique no botão "PROJUDI".
    o	Clique no menu "Impressão de CDA".
    o	Preenchimento do número da CDA.
    o	Clique no botão "Pesquisar".
    o	Clique no botão "Imprimir" (Download).
•	Finalizamos a Fase 1: Planejamento da automação.

•	📋 Resumo do Dia (30/04/2025)
1.	Refatoração com WebDriverWait:
Substituímos todos os time.sleep() por espera inteligente, usando expected_conditions para tornar a automação mais estável e profissional.
2.	Automatização do Login:
Automação dos campos de usuário e senha + clique no botão "Entrar".
3.	Navegação após login:
Acesso ao botão "PROJUDI" e ao menu lateral "Impressão de CDA", com tratamento de erro para quando o botão ainda não estiver visível.
4.	Interação com o formulário:
Inserção do número da CDA, clique em "Pesquisar" e clique no botão "Imprimir".
5.	Resolução de erro real:
Corrigido erro de XPath no botão "PROJUDI" e identificado que o encerramento manual do navegador provoca erro de sessão (InvalidSessionIdException).

•	📋 Resumo do Dia (19/05/2025)
Definimos a visão do projeto como "CDA Manager":
Uma aplicação completa que irá baixar, alterar, excluir e suspender CDAs.

Priorizamos o primeiro objetivo:
Automatizar o download em massa de CDAs, visando escalabilidade e velocidade.

Escolhemos o formato de entrada dos dados:
Leitura de CDA a partir de um arquivo .txt, com suporte para milhares de linhas.

Criamos o loop de processamento:
Lê cada CDA do arquivo, digita no sistema, clica em "Pesquisar" e "Imprimir", e passa para o próximo.

Adicionamos logs automáticos:
Cada CDA processado com sucesso ou erro é registrado em um arquivo log.txt com data e hora.

Organizamos o código por seções comentadas:
Facilitando manutenção, testes e futuras melhorias.



