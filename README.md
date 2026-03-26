# 🎵 Spotify Manager — Sistema CRUD em Python

**Autor:** Abel Chongolola | GPSI 10A | Nº 01

Sistema de gestão de utilizadores e artistas inspirado no Spotify, desenvolvido em Python com persistência em JSON.

---

## 📁 Estrutura do Projeto

```
projeto/
├── main.py              # Ponto de entrada da aplicação
├── artistas.py          # CRUD e menu da entidade Artista
├── utilizadores.py      # CRUD e menu da entidade Utilizador
├── utils.py             # Funções de validação partilhadas
├── artistas.json        # Base de dados persistente dos artistas
└── utilizadores.json    # Base de dados persistente dos utilizadores
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.x instalado

### Passos

```bash
# Clonar ou descarregar os ficheiros do projeto
# Navegar até à pasta do projeto

python main.py
```

Os ficheiros `.json` são criados/atualizados automaticamente ao executar o programa.

---

## ⚙️ Funcionalidades

### 👤 Gestão de Utilizadores (`utilizadores.py`)

| Opção | Função |
|-------|--------|
| 1 | Criar utilizador |
| 2 | Ver utilizador por ID |
| 3 | Pesquisar utilizador por nome |
| 4 | Atualizar utilizador |
| 5 | Remover utilizador |
| 6 | Listar todos os utilizadores |

**Campos do utilizador:**
- Nome de exibição, username (único), foto de perfil (URL)
- País, data de nascimento, géneros preferidos
- Estado da conta: `ativo` / `inativo` / `premium`
- Seguidores, artistas seguidos, playlists públicas, histórico de consumo
- Data de registo (gerada automaticamente)

---

### 🎤 Gestão de Artistas (`artistas.py`)

| Opção | Função |
|-------|--------|
| 1 | Criar artista |
| 2 | Ver artista por ID |
| 3 | Pesquisar artista por nome |
| 4 | Atualizar artista |
| 5 | Remover artista |
| 6 | Listar todos os artistas |
| 7 | Utilizador seguir artista |

**Campos do artista:**
- Nome (único), biografia, imagem de perfil e capa (URL)
- Género musical, verificado (sim/não)
- Discografia (álbum, EP, single), ouvintes mensais
- Top faixas (máx. 5), datas de concertos, seguidores

---

## 🔐 Validações (`utils.py`)

Todas as entradas do utilizador são validadas antes de serem guardadas:

| Validação | Regra |
|-----------|-------|
| Nome | Mínimo 2 caracteres |
| URL | Deve começar com `http://` ou `https://` |
| Data | Formato `DD/MM/AAAA`, anos entre 1900–2025 |
| Data de concerto | Formato `DD/MM/AAAA`, anos entre 2024–2030 |
| País | Sem números, mínimo 2 caracteres |
| Género(s) | Sem números, mínimo 2 caracteres por género |
| Ouvintes | Número inteiro positivo |
| Ano | 4 dígitos, entre 1900–2025 |
| Tipo de lançamento | `album`, `ep` ou `single` |
| Estado da conta | `ativo`, `inativo` ou `premium` |

---

## 💾 Persistência de Dados

Os dados são guardados automaticamente em JSON após cada operação de escrita.

**Formato dos IDs:**
- Utilizadores: `U0001`, `U0002`, ...
- Artistas: `A0001`, `A0002`, ...

Os contadores de ID são persistidos nos ficheiros JSON para garantir unicidade entre sessões.

---

## 🔗 Relação Utilizador ↔ Artista

Um utilizador pode seguir artistas através da opção **7** do menu de artistas. Esta operação atualiza simultaneamente:
- `seguidos[]` no utilizador
- `seguidores[]` no artista

---

## 📌 Notas

- Nomes de utilizadores e artistas são únicos no sistema (verificação case-insensitive).
- O programa **não usa** `isdigit()` nem métodos built-in de validação — toda a lógica é implementada manualmente.
- Os dados são carregados automaticamente ao iniciar e guardados após cada alteração.
