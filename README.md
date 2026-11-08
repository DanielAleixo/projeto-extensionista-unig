# Projeto de Pesquisa Extensionista - Ciência da Computação (UNIG)

## 📌 Objetivo do Projeto
Promover a integração entre ciência, tecnologia e sociedade por meio da produção e socialização de material informativo em Computação (com ênfase em Inteligência Artificial, Segurança Digital e ODS), aliado à coleta e análise de dados junto à comunidade acadêmica e externa.

## 🌍 Vínculo com os ODS (Agenda 2030 ONU)
- **ODS 4 (Educação de Qualidade):** Letramento digital e conscientização tecnológica acessível.
- **ODS 9 (Indústria, Inovação e Infraestrutura):** Avaliação do acesso à infraestrutura de TI e inovação local.
- **ODS 16 (Paz, Justiça e Instituições Eficazes):** Segurança da informação, proteção de dados (LGPD) e ética digital.

## 📂 Estrutura do Repositório
- `/docs`: Plano de pesquisa, TCLE, material informativo (infográfico), artigo científico e relatório de devolutiva.
- `/instrumento`: Versão final em PDF do questionário aplicado.
- `/dados`: Base de dados bruta, base tratada/anonimizada e dicionário de variáveis.
- `/analise`: Scripts em Python para limpeza de dados, geração de gráficos e dashboard interativo.
- `/figuras`: Gráficos gerados pelas análises descritivas e cruzamentos.

## 🚀 Como Reproduzir a Análise
1. Clone este repositório.
2. Instale as dependências: `pip install -r analise/requirements.txt`
3. Execute o script de limpeza e geração de gráficos: `python analise/01_limpeza_e_analise.py`
4. Para abrir o dashboard interativo localmente: `streamlit run analise/02_dashboard_app.py`

## 📊 Link do Dashboard Interativo Público
Acesse os resultados e gráficos em tempo real aqui: [Acessar Dashboard no Streamlit (https://projeto-extensionista-unig-ndk9w3pz2a3eai87crab5d.streamlit.app)]
