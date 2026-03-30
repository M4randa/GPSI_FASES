# 🎵 Spotify Manager — Sistema CRUD em Python

**Autor:** Abel Chongolola | **Curso:** GPSI | **Ano:** 10° A | **Nº:** 01

---

## 📋 Descrição

Sistema de gestão inspirado no Spotify, desenvolvido em Python.
Permite gerir as entidades **Utilizador** e **Artista** com operações completas de Create, Read, Update e Delete (CRUD).

---

## 📁 Estrutura do Projeto

```
projeto/
│
├── main.py          -> ponto de entrada, todos os inputs, prints e menus
├── utilizadores.py  -> CRUD da entidade Utilizador
├── artistas.py      -> CRUD da entidade Artista
└── utils.py         -> funcoes de validacao e geradores de ID partilhados
```

---

## 🗂️ Entidades

### Utilizador
| Campo | Descrição |
|---|---|
| `id_utilizador` | Gerado automaticamente (ex: U001) |
| `nome_exibicao` | Nome visível no perfil |
| `nome_utilizador` | Username interno (único) |
| `foto_perfil` | URL da foto de perfil |
| `pais` | País do utilizador |
| `data_nascimento` | Data no formato DD/MM/AAAA |
| `generos_preferidos` | Lista de géneros musicais |
| `data_registro` | Gerada automaticamente pelo sistema |
| `estado_conta` | ativo / inativo / premium |
| `seguidores` | Lista de IDs que seguem este utilizador |
| `seguidos` | Lista de IDs de artistas que segue |
| `playlists_publicas` | Lista de playlists públicas |
| `historico_consumo` | Histórico de músicas ouvidas |

### Artista
| Campo | Descrição |
|---|---|
| `id_artista` | Gerado automaticamente (ex: A001) |
| `nome` | Nome do artista (único) |
| `bio` | Biografia |
| `imagem` | URL da imagem de perfil |
| `imagem_capa` | URL da imagem de capa |
| `genero` | Género musical |
| `verificado` | Selo de verificação (True/False) |
| `ouvintes_mensais` | Número de ouvintes mensais |
| `seguidores` | Lista de IDs de utilizadores que seguem |
| `top_faixas` | Até 5 faixas em destaque |
| `discografia` | Lista de álbuns, EPs e singles |
| `datas_concertos` | Datas de concertos agendados |
| `escolha_artista` | Mensagem ou playlist em destaque |

---

## ⚙️ CRUD implementado

| Operação | Utilizador | Artista |
|---|---|---|
| **Create** | `criar_utilizador()` | `criar_artista()` |
| **Read** | `listar_utilizadores()` `consultar_utilizador()` `pesquisar_utilizadores()` | `listar_artistas()` `consultar_artista()` `pesquisar_artistas()` |
| **Update** | `atualizar_utilizador()` | `atualizar_artista()` `adicionar_lancamento()` `adicionar_top_faixa()` |
| **Delete** | `remover_utilizador()` | `remover_artista()` |

---

## 🔁 Relação entre entidades

- Um utilizador pode **seguir** um artista → `seguir_artista()`
- Um utilizador pode **deixar de seguir** um artista → `unfollow_artista()`

---

## 📡 Códigos de resposta

As funções das entidades devolvem sempre um tuplo `(codigo, mensagem)` seguindo o padrão HTTP:

| Código | Significado |
|---|---|
| `201` | Criado com sucesso |
| `200` | Operação bem sucedida |
| `404` | Não encontrado |
| `500` | Erro de validação |

---

## ✅ Validações (utils.py)

Todas as validações estão centralizadas em `utils.py` e partilhadas pelos dois módulos. Nenhuma usa `try/except`:

- **Nomes** — mínimo 2 caracteres
- **URLs** — obrigatório começar com `http://` ou `https://`
- **Datas** — formato `DD/MM/AAAA` com intervalos lógicos
- **País** — sem números, mínimo 2 caracteres
- **Estado da conta** — apenas `ativo`, `inativo` ou `premium`
- **Géneros** — mínimo 2 caracteres por género
- **Ouvintes** — número inteiro positivo

---

## 🏗️ Estrutura de Dados

Conforme recomendado no enunciado:

- **Dicionários `{}`** — acesso rápido por ID para utilizadores e artistas
- **Listas `[]`** — para agrupar múltiplos itens onde a ordem importa (seguidores, discografia, playlists, top faixas)

---

## 🚀 Como executar

```bash
python main.py
```
