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

Relatório Diário – 20/05/2025
✅ Atividades concluídas:
Ajustamos o script para ler a lista de CDAs a partir de um arquivo .csv
Substituímos o .txt por um .csv mais flexível, permitindo expansão futura.
Criamos um sistema de log em arquivo output_log.csv
Para cada CDA processado, registramos:
    Número da CDA
    Status (Success/Failed)
    Data e hora
    Mensagem de erro (caso falhe)
Adicionamos tratamento de erros com try/except
Evitamos que falhas interrompam o processamento de outras CDAs.
Implementamos lógica de tentativa com retry
Caso uma CDA falhe, o script tenta novamente até 2 vezes antes de registrar como “Failed”.
Corrigimos comportamento do Excel (notação científica)
Aplicamos formatação automática para manter os números longos como texto no arquivo .csv.
Mantivemos a estrutura organizada com boas práticas de importação e encerramento correto do log

Relatório Diário – 21/05/2025

✅ Atividades realizadas:
Implementação de mensagens de status no terminal

Agora o script exibe:
🔄 Iniciando serviços, 🔐 Efetuando login no Sitafe, 📥 Iniciando downloads, ✅ Downloads concluídos.

Validação e criação automática da pasta de downloads
O script verifica se a pasta CDAs existe e, se não existir, cria automaticamente, informando o usuário via terminal.
Transformação do bloco de verificação da pasta de downloads em uma função modular
A função setup_download_directory() melhora a legibilidade e reaproveitamento do código.
Correção na ordem de execução do caminho de download
Ajustado para garantir que a pasta exista antes de configurar as preferências do Chrome.
