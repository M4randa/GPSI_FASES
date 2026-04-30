# 🎵 Spotify Manager

**Sistema de Gestão de Plataforma de Streaming Musical**

Um projeto em Python que implementa um sistema completo de CRUD para gerenciar utilizadores, artistas, músicas e playlists - semelhante à estrutura de uma plataforma de streaming musical como o Spotify.

---

## 📋 Índice

- [Características](#características)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Módulos](#módulos)
- [Validações](#validações)
- [Códigos HTTP](#códigos-http)
- [Autor](#autor)

---

## ✨ Características

### Funcionalidades Principais

- ✅ **Gestão de Utilizadores**: Criar, listar, consultar, pesquisar, atualizar e remover utilizadores
- ✅ **Gestão de Artistas**: CRUD completo de artistas com discografia e top faixas
- ✅ **Gestão de Músicas**: Criar e gerir músicas com informações técnicas (bitrate, ISRC, duração)
- ✅ **Gestão de Playlists**: Criar playlists públicas/privadas e gerir conteúdo
- ✅ **Sistema de Relações**: Utilizadores seguem artistas e playlists
- ✅ **Validações Robustas**: Todos os dados são validados antes de serem armazenados
- ✅ **Códigos HTTP Padrão**: Respostas seguem convenções REST (200, 201, 404, 500)

### Entidades Geridas

| Entidade | Atributos Principais | ID |
|----------|---------------------|-----|
| **Utilizador** | Nome, username, foto, país, data nascimento, estado conta | U001, U002, ... |
| **Artista** | Nome, bio, imagem, género, verificação, discografia | A001, A002, ... |
| **Música** | Título, duração, ISRC, letra, bitrate, data lançamento | M001, M002, ... |
| **Playlist** | Nome, privacidade, descrição, capa, data criação | P001, P002, ... |

---

## 📁 Estrutura do Projeto

```
Spotify_Manager/
├── main.py              # Menu terminal e interface com utilizador
├── utilizadores.py      # CRUD da entidade Utilizador
├── artistas.py          # CRUD da entidade Artista
├── musica.py            # CRUD da entidade Música
├── Playlist.py          # CRUD da entidade Playlist
├── utils.py             # Funções de validação centralizadas
└── README.md            # Este ficheiro
```

### Separação de Responsabilidades

- **main.py**: Contém todos os `print()` e `input()` - interface com utilizador
- **utils.py**: Todas as validações centralizadas e reutilizáveis
- **Módulos de CRUD**: Lógica pura sem I/O, retornam códigos HTTP e dados

---

## 📦 Requisitos

- **Python**: 3.7 ou superior
- **Dependências**: Apenas biblioteca padrão (nenhuma instalação necessária)

---

## 🚀 Instalação

### 1. Clonar ou descarregar o repositório

```bash
git clone https://github.com/seu-usuario/spotify-manager.git
cd spotify-manager
```

### 2. Executar o programa

```bash
python main.py
```

O menu principal será apresentado:

```
===== SPOTIFY MANAGER =====
Abel Chongolola | GPSI 10A | N 01

===== MENU PRINCIPAL =====
1 - Gestao de Utilizadores
2 - Gestao de Artistas
3 - Gestao de Musicas
4 - Gestao de Playlists
0 - Sair
```

---

## 💡 Uso

### Exemplo Prático: Criar um Utilizador

1. Execute `python main.py`
2. Selecione a opção **1** (Gestão de Utilizadores)
3. Selecione **1** (Criar utilizador)
4. Preencha os dados solicitados:
   ```
   Nome de exibicao: João Silva
   Nome de utilizador (interno): joao_silva
   URL da foto de perfil: https://example.com/foto.jpg
   Pais: Portugal
   Data de nascimento (DD/MM/AAAA): 15/03/1995
   Generos preferidos (separados por virgula): Rock, Pop, Jazz
   Estado da conta (ativo/inativo/premium): ativo
   ```
5. O sistema retorna: `Utilizador criado com sucesso! ID: U001`

### Exemplo: Criar uma Música

1. Menu principal → Opção **3** (Gestão de Músicas)
2. Opção **1** (Criar música)
3. Dados necessários:
   - Título: mínimo 2 caracteres
   - ID do Artista: deve existir no sistema
   - Duração: em milissegundos (inteiro positivo)
   - Código ISRC: formato específico (ex: USRC17607839)
   - Data de lançamento: DD/MM/AAAA
   - Letra: mínimo 5 caracteres
   - Bitrate: 128, 192, 256 ou 320 kbps

---

## 📚 Módulos

### `main.py`
Interface terminal com menus interativos para todas as operações CRUD. Cada menu (utilizadores, artistas, músicas, playlists) oferece opções completas de gestão.

**Funções principais:**
- `menu_utilizadores()`
- `menu_artistas()`
- `menu_musicas()`
- `menu_playlists()`
- `main()`

### `utilizadores.py`
Gestão completa de utilizadores.

**Funções disponíveis:**
- `criar_utilizador()` → `201` ou `500`
- `listar_utilizadores()` → `200` ou `404`
- `consultar_utilizador()` → `200` ou `404`
- `pesquisar_utilizadores()` → `200` ou `404`
- `atualizar_utilizador()` → `200` ou `404`
- `remover_utilizador()` → `200` ou `404`
- `unfollow_artista()` → `200` ou `404`

### `artistas.py`
Gestão de artistas e discografia.

**Funções principais:**
- `criar_artista()` → `201` ou `500`
- `listar_artistas()` → `200` ou `404`
- `consultar_artista()` → `200` ou `404`
- `pesquisar_artistas()` → `200` ou `404`
- `atualizar_artista()` → `200` ou `500`
- `adicionar_lancamento()` → Adiciona álbum, EP ou single à discografia
- `adicionar_top_faixa()` → Máximo 5 faixas
- `remover_artista()` → `200` ou `404`
- `seguir_artista()` → Utilizador segue artista

### `musica.py`
Gestão de músicas com metadados técnicos.

**Funções principais:**
- `criar_musica()` → `201` ou `500`
- `listar_musicas()` → `200` ou `404`
- `consultar_musica()` → `200` ou `404`
- `pesquisar_musicas()` → `200` ou `404`
- `atualizar_musica()` → `200` ou `404`
- `remover_musica()` → `200` ou `404`

### `Playlist.py`
Gestão de playlists públicas e privadas.

**Funções principais:**
- `criar_playlist()` → `201` ou `500`
- `listar_playlists()` → `200` ou `404`
- `consultar_playlist()` → `200` ou `404`
- `atualizar_playlist()` → `200` ou `404`
- `adicionar_musica_playlist()` → `200` ou `404`
- `remover_musica_playlist()` → `200` ou `404`
- `remover_playlist()` → `200` ou `404`
- `seguir_playlist()` → Utilizador segue playlist

### `utils.py`
Centraliza todas as validações para garantir consistência.

**Validadores implementados:**
- `validar_nome()` - Mínimo 2 caracteres
- `validar_url()` - Começa com http:// ou https://
- `validar_data()` - Formato DD/MM/AAAA (1900-2025)
- `validar_pais()` - Mínimo 2 caracteres, sem números
- `validar_generos()` - Lista separada por vírgula
- `validar_estado_conta()` - ativo, inativo, premium
- `validar_privacidade()` - publica, privada
- `validar_isrc()` - Código ISRC (12 caracteres)
- `validar_duracao()` - Inteiro positivo (milissegundos)
- `validar_bitrate()` - 128, 192, 256 ou 320
- `validar_booleano()` - Converte múltiplos formatos para boolean

---

## ✔️ Validações

Todas as entradas são validadas antes de serem armazenadas. Exemplos:

| Campo | Validação | Exemplo Válido |
|-------|-----------|-----------------|
| Nome | ≥ 2 caracteres | "João Silva" |
| URL | Começa com http/https | "https://example.com/img.jpg" |
| Data | DD/MM/AAAA (1900-2025) | "15/03/1995" |
| ISRC | 12 caracteres (padrão ISO) | "USRC17607839" |
| Bitrate | 128, 192, 256, 320 | "320" |
| Privacidade | publica ou privada | "publica" |
| Estado | ativo, inativo, premium | "ativo" |

---

## 🔢 Códigos HTTP

O sistema utiliza códigos HTTP padrão para indicar o resultado das operações:

| Código | Significado | Exemplo |
|--------|------------|---------|
| **200** | OK - Operação bem-sucedida | Utilizador atualizado |
| **201** | Created - Recurso criado | Novo utilizador registado |
| **404** | Not Found - Recurso não encontrado | Artista não existe |
| **500** | Server Error - Validação falhou | Nome inválido |

### Exemplo de Resposta

```python
code, resultado = criar_utilizador("João", "joao", "https://...", ...)

if code == 201:
    print(f"Utilizador criado! ID: {resultado['id_utilizador']}")
elif code == 500:
    print(f"Erro: {resultado}")  # Erro de validação
```

---

## 🔐 Estrutura de Dados

### Utilizador
```python
{
    "id_utilizador": "U001",
    "nome_exibicao": "João Silva",
    "nome_utilizador": "joao_silva",
    "foto_perfil": "https://...",
    "pais": "Portugal",
    "data_nascimento": "15/03/1995",
    "generos_preferidos": ["Rock", "Pop"],
    "data_registro": "30/04/2026",
    "estado_conta": "ativo",
    "seguidores": [],
    "seguidos": ["A001"],  # IDs de artistas
    "playlists_publicas": [],
    "historico_consumo": []
}
```

### Artista
```python
{
    "id_artista": "A001",
    "nome": "The Beatles",
    "bio": "Banda britânica lendária...",
    "imagem": "https://...",
    "imagem_capa": "https://...",
    "genero": "Rock",
    "verificado": True,
    "discografia": [
        {"titulo": "Abbey Road", "tipo": "album", "ano": "1969"}
    ],
    "ouvintes_mensais": 5000000,
    "seguidores": ["U001"],
    "top_faixas": ["Hey Jude", "Let It Be"],
    "datas_concertos": [],
    "escolha_artista": ""
}
```

### Música
```python
{
    "id_musica": "M001",
    "titulo": "Hey Jude",
    "id_artista": "A001",
    "duracao_ms": 431000,
    "isrc": "GBDPG1200001",
    "data_lancamento": "26/08/1968",
    "letra": "Na, na-na-na-na...",
    "bitrate": 320,
    "contagem_reproducoes": 0,
    "flag_explicito": False,
    "status_takedown": False,
    "disponibilidade": True
}
```

### Playlist
```python
{
    "id_playlist": "P001",
    "nome_playlist": "Clássicos do Rock",
    "id_utilizador": "U001",
    "privacidade": "publica",
    "lista_ids": ["M001", "M002"],  # IDs de músicas
    "descricao": "Os melhores clássicos de rock de todos os tempos",
    "capa_playlist": "https://...",
    "data_criacao": "30/04/2026",
    "seguidores_playlist": ["U002"],
    "ordem_musicas": ["M001", "M002"],
    "flag_remocao": False
}
```

---

## 🤝 Relações entre Entidades

```
Utilizador
├── segue → Artista
├── segue → Playlist
├── cria → Playlist
└── tem → Histórico de Consumo

Artista
├── é seguido por → Utilizador
├── tem → Discografia (Álbuns/EPs/Singles)
├── tem → Top Faixas
└── tem → Seguidores

Música
├── pertence a → Artista
├── está em → Playlist
└── tem → Contagem de Reproduções

Playlist
├── pertence a → Utilizador
├── contém → Música
└── é seguida por → Utilizador
```

---

## 📝 Notas Técnicas

### Design Patterns

- **Separação de Responsabilidades**: Lógica, validação e I/O em módulos distintos
- **Centralização de Validações**: Todas em `utils.py` para consistência
- **IDs Autoincrementais**: Cada entidade tem contador único com prefixo
- **Respostas HTTP**: Padrão REST para facilitar integração futura com API

### Decisões de Implementação

- Dados armazenados em memória (dicionários) - sem persistência
- Validações rigorosas antes de armazenar
- Imports centralizados para facilitar manutenção
- Funções puras que retornam valores sem efeitos colaterais

### Possíveis Melhorias

1. **Persistência**: Integrar com base de dados (SQLite, PostgreSQL)
2. **API REST**: Converter em Flask/FastAPI
3. **Autenticação**: Sistema de login e tokens
4. **Paginação**: Para listagens com muitos registos
5. **Soft Delete**: Flag de remoção em vez de eliminação física
6. **Logs**: Sistema de auditoria de operações
7. **Testes Unitários**: Cobertura completa com pytest
8. **Cache**: Para operações frequentes de leitura

---

## 👤 Autor

**Abel Chongolola**
- Turma: GPSI 10A
- Número: 01
- Projeto: Sistema de Gestão de Plataforma de Streaming Musical

---

## 📄 Licença

Este projeto é fornecido como material educacional.

---

## 📞 Suporte

Para dúvidas ou problemas com o funcionamento, verifique:
1. Se o Python 3.7+ está instalado: `python --version`
2. Se todos os ficheiros estão no mesmo diretório
3. Se as validações são respeitadas (datas em DD/MM/AAAA, etc)
4. Os códigos HTTP retornados para identificar erros

---

**Última atualização**: 30 de Abril de 2026
