import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Configurações visuais e diretórios
sns.set_theme(style="whitegrid")
DIR_DADOS = "../dados"
DIR_FIGURAS = "../figuras"
os.makedirs(DIR_DADOS, exist_ok=True)
os.makedirs(DIR_FIGURAS, exist_ok=True)

def mapear_colunas_inteligente(df):
    """Mapeia as colunas do Google Forms usando palavras-chave de cada pergunta."""
    novo_mapa = {}
    for col in df.columns:
        c_low = col.lower()
        if "carimbo" in c_low or "timestamp" in c_low or "data/hora" in c_low:
            novo_mapa[col] = "timestamp"
        elif "faixa etária" in c_low:
            novo_mapa[col] = "faixa_etaria"
        elif "inteligência artificial" in c_low:
            novo_mapa[col] = "interesse_ia"
        elif "principais barreiras" in c_low:
            novo_mapa[col] = "barreiras_tec"
        elif "dois fatores" in c_low or "2fa" in c_low:
            novo_mapa[col] = "frequencia_2fa"
        elif "higiene de senhas" in c_low:
            novo_mapa[col] = "higiene_senhas"
        elif "lgpd" in c_low and "marco civil" in c_low:
            novo_mapa[col] = "conhecimento_lgpd"
        elif "nuvem" in c_low:
            novo_mapa[col] = "uso_nuvem"
        elif "contribui para melhorar a educação" in c_low:
            novo_mapa[col] = "relevancia_ti_ods"
        elif "metas dos ods" in c_low or "prioritárias" in c_low:
            novo_mapa[col] = "ods_prioritarios"
        elif "problema da sua realidade" in c_low:
            novo_mapa[col] = "problema_realidade"
        else:
            # A questão 1 (TCLE) não tem texto no título além de "*", então é a primeira coluna após o timestamp
            if "consentimento" not in novo_mapa.values():
                novo_mapa[col] = "consentimento"
    return df.rename(columns=novo_mapa)

def carregar_e_limpar_dados(caminho_csv):
    print("1. Carregando base bruta do Google Forms...")
    df = pd.read_csv(caminho_csv, encoding="utf-8-sig")
    df = mapear_colunas_inteligente(df)

    # Filtrar apenas participantes que concordaram com o TCLE
    if "consentimento" in df.columns:
        total_inicial = len(df)
        df = df[df["consentimento"].astype(str).str.contains("Concordo", case=False, na=False)]
        print(f"   Participantes validados pelo TCLE: {len(df)} de {total_inicial}")

    # Garantir tipagem numérica nas escalas Likert (Questões 3, 5, 6, 7, 8, 9)
    colunas_likert = [
        "interesse_ia", "frequencia_2fa", "higiene_senhas",
        "conhecimento_lgpd", "uso_nuvem", "relevancia_ti_ods"
    ]
    for col in colunas_likert:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Anonimização (LGPD): Remover carimbo de data/hora exato
    colunas_remover = [c for c in ["timestamp"] if c in df.columns]
    df_tratado = df.drop(columns=colunas_remover)

    caminho_saida = os.path.join(DIR_DADOS, "dados_tratados.csv")
    df_tratado.to_csv(caminho_saida, index=False, encoding="utf-8-sig")
    print(f"2. Base tratada e anonimizada salva em: {caminho_saida}")
    return df_tratado

def gerar_estatistica_descritiva(df):
    print("\n3. Gerando Estatística Descritiva...")
    colunas_likert = [
        "interesse_ia", "frequencia_2fa", "higiene_senhas",
        "conhecimento_lgpd", "uso_nuvem", "relevancia_ti_ods"
    ]
    existentes = [c for c in colunas_likert if c in df.columns]
    
    resumo = df[existentes].agg(["count", "mean", "std", "median", "min", "max"]).T
    resumo.columns = ["N", "Média", "Desvio Padrão", "Mediana", "Mín", "Máx"]
    print("\n--- Tabela de Médias e Desvios (Escalas Likert 1 a 5) ---")
    print(resumo.round(2))
    resumo.round(2).to_csv(os.path.join(DIR_DADOS, "resumo_estatistico_likert.csv"), encoding="utf-8-sig")

def gerar_visualizacoes(df):
    print("\n4. Gerando gráficos de alta resolução em /figuras...")

    # GRÁFICO 1: Barras Horizontais - Barreiras Tecnológicas na Região (Q4)
    if "barreiras_tec" in df.columns:
        plt.figure(figsize=(10, 5))
        # No Google Forms, checkboxes são separados por vírgula ou ponto e vírgula
        barreiras = df["barreiras_tec"].dropna().str.split(r",\s*(?=[A-Z])|;").explode().str.strip()
        contagem = barreiras.value_counts()
        sns.barplot(x=contagem.values, y=contagem.index, palette="magma")
        plt.title("Principais Barreiras Percebidas para o Avanço Tecnológico Regional", fontsize=13, fontweight="bold")
        plt.xlabel("Quantidade de Menções")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig(os.path.join(DIR_FIGURAS, "01_barras_barreiras_regionais.png"), dpi=300)
        plt.close()

    # GRÁFICO 2: Pizza - Distribuição por Faixa Etária (Q2)
    if "faixa_etaria" in df.columns:
        plt.figure(figsize=(7, 7))
        contagem_idade = df["faixa_etaria"].value_counts()
        plt.pie(contagem_idade, labels=contagem_idade.index, autopct="%1.1f%%", startangle=140, colors=sns.color_palette("Set2"))
        plt.title("Perfil dos Participantes por Faixa Etária", fontsize=14, fontweight="bold")
        plt.tight_layout()
        plt.savefig(os.path.join(DIR_FIGURAS, "02_pizza_faixa_etaria.png"), dpi=300)
        plt.close()

    # GRÁFICO 3: Barras Agrupadas - Médias dos Indicadores de Segurança, IA e Nuvem (Likert 1-5)
    nomes_amigaveis = {
        "interesse_ia": "Interesse em IA (Q3)",
        "frequencia_2fa": "Uso de 2FA (Q5)",
        "higiene_senhas": "Higiene de Senhas (Q6)",
        "conhecimento_lgpd": "Conhecimento LGPD (Q7)",
        "uso_nuvem": "Uso de Nuvem (Q8)",
        "relevancia_ti_ods": "TI para ODS (Q9)"
    }
    cols_validas = [c for c in nomes_amigaveis.keys() if c in df.columns]
    if cols_validas:
        plt.figure(figsize=(10, 6))
        medias = df[cols_validas].mean().rename(index=nomes_amigaveis).sort_values(ascending=True)
        ax = medias.plot(kind="barh", color="#2b5c8f")
        plt.xlim(0, 5.3)
        for i, v in enumerate(medias):
            ax.text(v + 0.08, i, f"{v:.2f}", va="center", fontweight="bold")
        plt.title("Média Geral dos Indicadores Avaliados (Escala 1 a 5)", fontsize=14, fontweight="bold")
        plt.xlabel("Pontuação Média (1 = Mínimo | 5 = Máximo)")
        plt.tight_layout()
        plt.savefig(os.path.join(DIR_FIGURAS, "03_barras_medias_likert.png"), dpi=300)
        plt.close()

    # GRÁFICO 4: Heatmap - Cruzamento Faixa Etária vs. Médias de Segurança e LGPD
    cols_seg = [c for c in ["frequencia_2fa", "higiene_senhas", "conhecimento_lgpd"] if c in df.columns]
    if "faixa_etaria" in df.columns and cols_seg:
        plt.figure(figsize=(8, 5))
        cruzamento = df.groupby("faixa_etaria")[cols_seg].mean()
        cruzamento = cruzamento.rename(columns={
            "frequencia_2fa": "Uso de 2FA",
            "higiene_senhas": "Higiene de Senhas",
            "conhecimento_lgpd": "Direitos LGPD"
        })
        sns.heatmap(cruzamento, annot=True, fmt=".2f", cmap="YlGnBu", vmin=1, vmax=5, cbar_kws={'label': 'Média (1 a 5)'})
        plt.title("Cruzamento: Práticas de Segurança Digital por Faixa Etária", fontsize=13, fontweight="bold")
        plt.ylabel("Faixa Etária")
        plt.tight_layout()
        plt.savefig(os.path.join(DIR_FIGURAS, "04_heatmap_seguranca_por_idade.png"), dpi=300)
        plt.close()

    # GRÁFICO 5: Prioridades de ODS para o Município (Q10)
    if "ods_prioritarios" in df.columns:
        plt.figure(figsize=(9, 5))
        ods = df["ods_prioritarios"].dropna().str.split(r",\s*(?=ODS)|;").explode().str.strip()
        contagem_ods = ods.value_counts()
        sns.barplot(x=contagem_ods.values, y=contagem_ods.index, palette="viridis")
        plt.title("Metas dos ODS Prioritárias para Aplicação no Município", fontsize=13, fontweight="bold")
        plt.xlabel("Votos")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig(os.path.join(DIR_FIGURAS, "05_barras_ods_prioritarios.png"), dpi=300)
        plt.close()

    # GRÁFICO 6: Nuvem de Palavras da Questão Aberta (Q11)
    if "problema_realidade" in df.columns:
        texto = " ".join(df["problema_realidade"].dropna().astype(str).tolist())
        stopwords_pt = {
            "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não", "uma",
            "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "foi", "ao", "ele",
            "das", "tem", "à", "seu", "sua", "ou", "ser", "quando", "muito", "há", "nos", "já",
            "está", "eu", "também", "só", "pelo", "pela", "até", "isso", "ela", "entre", "depois"
        }
        if len(texto.strip()) > 3:
            wc = WordCloud(width=900, height=450, background_color="white", stopwords=stopwords_pt, colormap="crest").generate(texto)
            plt.figure(figsize=(10, 5))
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.title("Nuvem de Palavras: 'Que problema da sua realidade a Computação poderia melhorar?'", fontsize=12, fontweight="bold")
            plt.tight_layout()
            plt.savefig(os.path.join(DIR_FIGURAS, "06_nuvem_palavras_aberta.png"), dpi=300)
            plt.close()

    print("   Todos os 6 gráficos foram salvos na pasta '/figuras'!")

if __name__ == "__main__":
    arquivo_bruto = os.path.join(DIR_DADOS, "dados_brutos.csv")
    if os.path.exists(arquivo_bruto):
        df_limpo = carregar_e_limpar_dados(arquivo_bruto)
        gerar_estatistica_descritiva(df_limpo)
        gerar_visualizacoes(df_limpo)
    else:
        print(f"Aguardando arquivo '{arquivo_bruto}'. Quando baixar do Google Forms, renomeie para 'dados_brutos.csv' e coloque na pasta 'dados/'.")