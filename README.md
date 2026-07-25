# 🏛️ Câmara Analytics

> **Projeto de Estudo em Engenharia e Análise de Dados**  
> Aplicação prática de conceitos de ingestão de dados, modelagem dimensional e Business Intelligence (BI) utilizando dados abertos da Câmara dos Deputados.

---

## 🎯 Sobre o Projeto

O **Câmara Analytics** é um projeto com foco acadêmico e de desenvolvimento de portfólio. O objetivo principal é construir um pipeline de dados *End-to-End* — desde a extração de dados brutos via API REST até a modelagem colunar e publicação de dashboards analíticos.

Como estudo de caso, o projeto analisa os gastos da **Cota para o Exercício da Atividade Parlamentar (CEAP)** e a produtividade dos deputados federais brasileiros durante a **57ª Legislatura**.

---

## 🏗️ Arquitetura e Fluxo de Dados

O projeto adota os princípios da **Arquitetura Medalhão** e do **Modern Data Stack**:

1. **Ingestão (Camada Bronze):** Extração automatizada dos dados brutos da API dos Dados Abertos via Python.
2. **Tratamento & Limpeza (Camada Silver):** Padronização, deduplicação e limpeza dos dados utilizando **DuckDB**.
3. **Modelagem Dimensional (Camada Gold):** Criação das tabelas Fato e Dimensão para consumo analítico.
4. **Visualização:** Construção de dashboards interativos com **Evidence.dev** (Markdown + SQL).
5. **Automação:** Orquestração do pipeline de ETL e deploy contínuo via **GitHub Actions**.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem & Ingestão:** Python (`requests`, `pandas`)
* **Banco de Dados Analítico:** DuckDB
* **Visualização & BI:** Evidence.dev (BI-as-Code)
* **Automação & CI/CD:** GitHub Actions

---

## 📁 Estrutura do Repositório

```text
├── .github/
│   └── workflows/      # Automações de ETL e Deploy
├── data/               # Banco de dados DuckDB
├── pages/              # Dashboards e relatórios (Evidence)
├── sources/            # Conexão do Evidence com o DuckDB
├── etl.py              # Script principal do pipeline de dados
├── package.json        # Configurações do Evidence (Node.js)
└── requirements.txt    # Dependências do Python
```

---

## 🚀 Como Executar Localmente

### Pré-requisitos
* Python 3.10 ou superior
* Node.js 18 ou superior

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/alvacir-junior/camara-analytics.git
   cd camara-analytics
   ```

2. **Instale as dependências do Python:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o pipeline ETL:**
   ```bash
   python etl.py
   ```

4. **Instale as dependências do Evidence e inicie o projeto:**
   ```bash
   npm install
   npm run dev
   ```

---

## 📌 Objetivos de Aprendizado

* Consumo resiliente de APIs REST públicas.
* Aplicação da Arquitetura Medalhão em bancos analíticos colunares (DuckDB).
* Modelagem Dimensional (Star Schema) voltada para Business Intelligence.
* Práticas de **BI-as-Code** (gerenciamento de BI via código e versionamento).
* Automação de rotinas de dados utilizando CI/CD com GitHub Actions.

---
