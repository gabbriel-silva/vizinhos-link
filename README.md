# VIZINHOS LINK
## REDE COMUNITARIA DE BAIRRO

---

PROJETO EXTENSIONISTA — UNINTER
SISTEMA DE INTERACAO HIPERLOCAL E ZELADORIA COLETIVA

---

### 01. CONTEXTO E IMPACTO SOCIAL

O Vizinhos Link e uma plataforma desenvolvida sob as diretrizes de acao social e engajamento comunitario da UNINTER. O sistema foi projetado para mitigar o isolamento nos grandes centros urbanos, centralizar comunicados de utilidade publica e impulsionar o comercio local por meio de uma interface unificada.

* ZELADORIA COLETIVA: Centraliza registros de infraestrutura e seguranca, permitindo o acompanhamento ate a resolucao.
* ECONOMIA CIRCULAR: Apoia o pequeno comerciante e o prestador de servicos local atraves de uma categoria exclusiva de perfil.
* LEVANTAMENTO DE DADOS: O painel estatistico traduz o engajamento da comunidade em metricas quantitativas, servindo como base cientifica para o relatorio de extensao academica.

---

### 02. DIRETRIZES DE DESIGN: RETRO MINIMALISTA

A interface do projeto foi completamente revitalizada para seguir uma estetica editorial classica, flat e de alto contraste, eliminando distracoes visuais para focar estritamente na informacao.

* SEM EMOJIS: A iconografia grafica foi abolida. A hierarquia e a navegacao dependem exclusivamente da tipografia e da diagramacao estruturada.
* GEOMETRIA RIGIDA: Bordas arredondadas e sombras suaves foram substituidas por cantos retos (0px) e sombras planas bidimensionais (block shadows).
* CODIFICACAO CROMATICA: A diferenciacao de criticidade (alertas urgentes, pedidos de ajuda ou registros resolvidos) e feita atraves de blocos de cor solidos e de alta visibilidade.
* SUPORTE A TEMAS: Gerenciamento nativo de modos claro e escuro atraves de propriedades customizadas CSS, com tratamento assincrono para prevencao de falhas de carregamento (flash de tema).

---

### 03. RECURSOS DO SISTEMA

* AUTENTICACAO: Registro e controle de sessoes com distincao estrutural entre perfis do tipo Morador e Parceiro Local.
* MURAL INTEGRADO: Publicacao de mensagens de texto com suporte a anexos de imagens e marcacoes de contexto.
* FILTRAGEM AVANCADA: Segmentacao do feed por categorias (Seguranca, Eventos, Servicos, Adocao, Doacoes, Avisos) e por estado da demanda (Em aberto ou Resolvidos).
* MODERACAO descentralizada: Mecanismo de seguranca que restringe a exclusao e a alternancia de status (resolucao) exclusivamente ao autor da publicacao.
* ACESSIBILIDADE (A11y): Estrutura adaptada com skip-links para navegacao por teclado, rotulos semanticos para leitores de tela e conformidade com a diretiva prefers-reduced-motion.

---

### 04. ENGENHARIA E MELHORIAS TECNICAS

Para atender aos criterios formais de avaliacao tecnica, o nucleo da aplicacao recebeu as seguintes implementacoes de arquitetura e seguranca:

1. PROTECAO CSRF REAL: Ativacao global do framework Flask-WTF no backend. Todas as requisicoes do tipo POST exigem e validam tokens criptograficos dinamicos, mitigando ataques de falsificacao de requisicao.
2. ISOLAMENTO DE UPLOADS: Substituicao dos nomes originais de arquivos por identificadores unicos universais (UUID4). O procedimento anula o risco de sobreposicao acidental de arquivos e bloqueia exploracoes de Path Traversal.
3. REESTRUTURACAO DE ENDPOINTS: Correcao do mecanismo da rota de resolucao (/resolve/<id>), reconfigurado para operacao exclusiva via metodo POST, impedindo disparos maliciosos ou indexacoes acidentais por navegadores.
4. PAGINACAO DE PERFORMANCE: Otimizacao de queries SQL com limite estrito de 5 publicacoes por pagina. A abordagem protege a memoria do servidor e reduz o overhead de transferencia de dados.
5. DASHBOARD ANALITICO: Desenvolvimento de endpoint estatistico (/dashboard) integrado a biblioteca Chart.js, renderizando graficos volumetricos diretamente dos dados agregados pelo ORM.

---

### 05. ARQUITETURA DE TECNOLOGIA

* BACKEND: Python 3 / Flask Framework
* PERSISTENCIA: SQLite / Flask-SQLAlchemy
* SEGURANCA: Flask-Login / Flask-WTF (CSRFProtect)
* FRONTEND: HTML5 / CSS3 Estrutural Puro / JavaScript Vanilla
* METRICAS: Chart.js (via CDN assincrona)

---

### 06. CONFIGURACAO E INSTALACAO

Siga os comandos estruturados abaixo para replicar o ambiente de execucao local:

1. COMPILAR O AMBIENTE VIRTUAL
   No Windows:
   $ python -m venv venv
   $ venv\Scripts\activate

   No Linux/macOS:
   $ python3 -m venv venv
   $ source venv/bin/activate

2. INSTALAR DEPENDENCIAS DO ECOSSISTEMA
   $ pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF werkzeug

3. INICIALIZAR E POPULAR O BANCO DE DADOS (SEED)
   O comando criara a estrutura relacional e inserira dados realistas de teste:
   $ python seed.py

4. EXECUTAR O SERVIDOR DE DESENVOLVIMENTO
   $ python app.py

O sistema estara acessivel pelo endereco local: http://127.0.0.1:5000

CREDENCIAIS DE TESTE: Todos os perfis gerados pelo script de semente (incluindo ana_silva, carlos_fonseca e os estabelecimentos comerciais PetShopAmigos e MercadoBairro) utilizam a senha padrao: 123456