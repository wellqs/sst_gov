# Documentação SST_GOV

## Stack e módulos
- **Backend**: Django 5 + PostgreSQL (Docker Compose expõe web em 8002 e DB em 5433).
- **Apps**: core (gestão), acidentes (S-2210/CAT), epi (catálogo/entregas), exames (S-2220), relatorios. Inspeções/treinamentos ainda em construção.
- **Chat IA**: endpoint `/api/chat` usa OPENAI_API_KEY do `.env`.

# SST_GOV — Sistema de Segurança e Saúde do Trabalhador
**Documentação Técnica Completa – Versão 1.0**  
**Autor:** Uélinton Quintão Silvério

---

# Índice

- [1. Introdução](#1-introdução)
  - [1.1 Objetivo Geral](#11-objetivo-geral)
  - [1.2 Objetivos Específicos](#12-objetivos-específicos)
  - [1.3 Escopo do Sistema](#13-escopo-do-sistema)

- [2. Fragilidades e Dificuldades Encontradas](#2-fragilidades-e-dificuldades-encontradas)
  - [2.1 Fragmentação e Ausência de Sistema Unificado](#21-fragmentação-e-ausência-de-sistema-unificado)

- [3. Funcionalidades Principais](#3-funcionalidades-principais)

- [4. Arquitetura de Alto Nível](#4-arquitetura-de-alto-nível)
  - [4.1 Componentes Principais](#41-componentes-principais)
  - [4.2 Serviços Complementares (Futuro)](#42-serviços-complementares-futuro)

- [5. Fluxo Operacional](#5-fluxo-operacional)

- [6. Modelo de Dados](#6-modelo-de-dados)

- [7. Requisitos do Sistema](#7-requisitos-do-sistema)

- [8. Considerações Finais](#8-considerações-finais)

---
# 1. Introdução

O **SST_GOV** é um sistema desenvolvido para modernizar, unificar e automatizar os processos relacionados ao **Serviço de Segurança e Saúde do Trabalhador** no setor público.

> Importante: O sistema foi projetado seguindo princípios de prevenção, transparência, rastreabilidade e governança institucional.

---

## 1.1 Objetivo Geral

Estabelecer um sistema completo que permita gestão integrada de:

- Acidentes;
- Entrega de EPIs;
- Treinamentos;
- Exames (futuro);
- Riscos (futuro);
- Indicadores estratégicos;
- Integração com eSocial.

---

## 1.2 Objetivos Específicos

- Centralizar dados ocupacionais;
- Automatizar fluxos críticos;
- Facilitar auditorias;
- Reduzir riscos legais;
- Gerar inteligência operacional.

---

## 1.3 Escopo do Sistema

O SST_GOV cobre a estrutura completa de segurança e saúde do trabalhador, com expansão progressiva para módulos avançados como riscos, PGR, PCMSO, BI e gestão ambiental.

---

# 2. Fragilidades e Dificuldades Encontradas

O diagnóstico inicial revelou diversas falhas na gestão institucional que justificam a criação do sistema.

---

## 2.1 Fragmentação e Ausência de Sistema Unificado

> Nota: Esta é a principal deficiência dos órgãos públicos no contexto de SST.

Problemas identificados:

- Uso de planilhas desconexas;
- Falta de histórico;
- Inexistência de auditoria interna;
- Informações duplicadas ou contraditórias;
- Falta de indicadores;
- Dependência de conhecimento individual;
- Riscos legais devido à não conformidade.

---

# 3. Funcionalidades Principais

As funções disponíveis no SST_GOV incluem:

- Cadastro de servidores;
- Gestão de EPIs;
- Emissão e histórico de entregas;
- Registro de acidentes;
- Dashboard operacional;
- Auditoria;
- Treinamentos;
- Módulos programados (futuro).

---

# 4. Arquitetura de Alto Nível

A arquitetura adota uma estrutura **modular**, **escalável** e **seguindo boas práticas de engenharia de software**, utilizando Django como núcleo.

---

## 4.1 Componentes Principais

### Frontend Web

- Templates Django;
- CSS próprio (`static/css/main.css`);
- JavaScript Vanilla;
- Grid responsiva;
- Chat integrado;
- Interface otimizada para desktop e mobile.

---

### Backend

- Regras de negócio;
- Validação de EPI/CA;
- Ocorrências e CAT;
- Treinamentos;
- Indicadores;
- Autenticação e permissões;
- Auditoria interna.

---

### Banco de Dados

- PostgreSQL ou MySQL;
- Entidades principais:
  - Servidor;
  - Cargos e Setores;
  - EPIs;
  - Entregas;
  - Ocorrências;
  - Treinamentos;
  - Auditoria.

---

## 4.2 Serviços Complementares (Futuro)

### Integração com eSocial

Eventos:

- S-2210 — Acidente;
- S-2220 — Saúde do Trabalhador;
- S-2240 — Riscos e condições ambientais.

> Importante: Reduz passivos legais e garante conformidade normativa.

---

### Módulo de Analytics e BI

- Dashboards executivos;
- Relatórios de conformidade;
- Análises preditivas;
- Rankings e comparativos;
- Painéis de indicadores.

---

### Automação de Fluxos Operacionais

Exemplos:

- Acidente → Notificação → Investigação → Relatório;
- EPI entregue → Registro automático;
- Exame a vencer → Alerta programado.

---

### Integração com Almoxarifado e Compras

- Controle de estoque;
- Rastreabilidade;
- Reposição automática;
- Integração com sistemas patrimoniais.

---

### Módulo de Exames Ocupacionais

- ASOs;
- Exames complementares;
- Alertas;
- Histórico médico ocupacional.

---

### Módulo de Gestão de Riscos (NR-01 e NR-09)

- Identificação de perigos;
- Avaliação probabilidade × severidade;
- Plano de ação;
- Integração com EPIs e treinamentos;
- Emissão de PGR.

> Importante: Mitigação significa **reduzir impacto e probabilidade** sem eliminar totalmente o risco.

---

### Módulo de Gestão Ambiental

Recursos:

- Controle de resíduos;
- Indicadores ambientais;
- Não conformidades;
- Auditorias ambientais;
- Mapeamento de impactos;
- Relatórios ambientais.

> Nota: Alinha o sistema às diretrizes ESG.

---

# 5. Fluxo Operacional

O fluxo envolve:

1. Cadastro;
2. Registros;
3. Entregas / Ocorrências;
4. Indicadores;
5. Auditoria.

---

# 6. Modelo de Dados

Tabelas principais:

- Servidor;
- Cargo;
- Setor;
- EPI;
- EntregaEPI;
- Ocorrencia;
- Treinamento.

---

# 7. Requisitos do Sistema

### Requisitos Técnicos

- Python 3.10+;
- Django;
- MySQL/PostgreSQL;
- Ambiente Linux recomendado.

---

### Requisitos Operacionais

- Setores devidamente treinados;
- Procedimentos internos padronizados.

---

# 8. Considerações Finais

O SST_GOV se consolida como uma ferramenta moderna, robusta e alinhada à real necessidade das instituições públicas no campo da segurança e saúde do trabalhador.

---

# **Documento desenvolvido por Uélinton Quintão Silvério — Autor e idealizador do sistema SST_GOV.**
