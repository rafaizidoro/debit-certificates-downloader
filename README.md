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
🧠 Aprendizados reforçados:
•	Diferença entre classes e objetos em Python (Service vs service).
•	Uso adequado de WebDriverWait e ExpectedConditions.
•	Como localizar elementos de forma resiliente com XPath e By.LINK_TEXT.
•	Primeiros passos para capturar falhas com try/except.
📌 Status do Projeto:
•	Login automatizado ✅
•	Navegação até CDA automatizada ✅
•	Busca e download de CDA funcionando ✅
•	Preparado para próxima etapa: loop de múltiplas CDAs 🔄

