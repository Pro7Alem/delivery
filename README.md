# Delivery

## Descrição
Sistema administrativo desenvolvido como preparação para a abertura do próprio negócio de delivery. A ideia é ter, desde o primeiro dia de operação, uma ferramenta interna que centralize tudo — pedidos, entregadores, cardápio, funcionários, patrimônio e financeiro — no lugar de depender de anotações, planilhas e memória.

## Status
Pausado

## Estado Atual do Desenvolvimento

O projeto encontra-se em estágio de Protótipo Funcional. O foco principal foi a modelagem do domínio e a implementação das regras de negócio core.

As áreas exploradas incluem:

- **Modelagem de Entidades** — estruturação de tabelas para Pedidos, Entregadores, Cardápio, Funcionários, Patrimônio e Financeiro
- **Lógica de Negócio** — implementação de cálculo dinâmico de taxa de entrega por faixa de distância (km)
- **Interface Administrativa** — telas básicas para entrada de dados e visualização de registros

> Como o desenvolvimento foi suspenso para priorizar outros projetos, nem todos os fluxos de ponta a ponta foram exaustivamente testados ou finalizados. O repositório serve como registro de lógica de backend e organização sistêmica.

## Tecnologias
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511fa.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

## Observações
- **SQLite como banco de dados** — escolha técnica baseada na simplicidade de deploy e baixa latência para operações locais. O SQLite atende perfeitamente à volumetria de um negócio de delivery de pequeno/médio porte. A migração para um banco cliente-servidor (como PostgreSQL) só seria considerada em um cenário de alta concorrência de escrita ou necessidade de escalabilidade horizontal.
- **Arquitetura monolítica** — toda a lógica concentrada em `app.py` para agilizar o desenvolvimento solo. Gera acoplamento que dificulta manutenção e evolução do sistema a médio prazo.
- **Melhorias previstas** — modularização do monólito, autenticação e controle de acesso, dashboard financeiro com gráficos, histórico de pedidos por cliente, integração com Google Maps para roteamento e reorganização geral da estrutura do projeto. Migração para PostgreSQL seria considerada apenas se o crescimento do negócio exigir múltiplas instâncias simultâneas ou alta concorrência de escrita — cenário improvável para um delivery local, mas previsto caso a operação escale.