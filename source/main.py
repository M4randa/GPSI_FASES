# ==============================
# gui.py
# Interface Tkinter estilo Spotify
# ==============================

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import webbrowser
import threading
from io import BytesIO

import requests

# Import do spotify_online.py
from spotify_online import (
    pesquisar_musicas as sp_pesquisar_musicas,
    pesquisar_artistas as sp_pesquisar_artistas,
    get_musicas_artista,
    get_musicas_populares,
    testar_conexao,
    obter_imagem_artista
)

from utilizadores import (
    criar_utilizador, listar_utilizadores, consultar_utilizador,
    pesquisar_utilizadores, atualizar_utilizador, remover_utilizador,
    unfollow_artista
)
from artistas import (
    criar_artista, listar_artistas, consultar_artista,
    pesquisar_artistas, atualizar_artista, adicionar_lancamento,
    adicionar_top_faixa, remover_artista, seguir_artista
)
from musica import (
    criar_musica, listar_musicas, consultar_musica,
    pesquisar_musicas, atualizar_musica, remover_musica,
    registar_reproducao, carregar_musicas
)
from Playlist import (
    criar_playlist, listar_playlists, consultar_playlist,
    atualizar_playlist, adicionar_musica_playlist,
    remover_musica_playlist, remover_playlist, seguir_playlist
)

# ==============================
# CORES SPOTIFY
# ==============================
BG = "#121212"
SIDEBAR = "#000000"
CARD = "#1e1e1e"
GREEN = "#1DB954"
WHITE = "#FFFFFF"
GRAY = "#b3b3b3"
HOVER = "#282828"
INPUT_BG = "#2a2a2a"
FONT = "Segoe UI"
BLACK_TEXT = "#000000"


# ==============================
# JANELA FORMULARIO GENERICA
# ==============================

def abrir_form(titulo, campos, callback):
    win = tk.Toplevel()
    win.title(titulo)
    win.configure(bg=BG)
    win.resizable(False, False)
    win.grab_set()

    tk.Label(win, text=titulo, bg=BG, fg=GREEN,
             font=(FONT, 14, "bold")).pack(pady=(18, 6), padx=24)

    entries = {}
    placeholders = {}
    frame = tk.Frame(win, bg=BG)
    frame.pack(padx=24, pady=6)

    for i, campo in enumerate(campos):
        label, chave = campo[0], campo[1]
        ph = campo[2] if len(campo) > 2 else ""

        tk.Label(frame, text=label, bg=BG, fg=GRAY,
                 font=(FONT, 10), anchor="w").grid(row=i, column=0, sticky="w", pady=4, padx=(0, 12))

        e = tk.Entry(frame, bg=INPUT_BG, fg=WHITE, insertbackground=WHITE,
                     font=(FONT, 10), width=32, relief="flat", bd=6)
        if ph:
            e.insert(0, ph)
            e.config(fg=GRAY)
            placeholders[chave] = ph

            def _on_focus_in(event, entry=e, placeholder=ph):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg=WHITE)

            def _on_focus_out(event, entry=e, placeholder=ph):
                if entry.get() == "":
                    entry.insert(0, placeholder)
                    entry.config(fg=GRAY)

            e.bind("<FocusIn>", _on_focus_in)
            e.bind("<FocusOut>", _on_focus_out)

        e.grid(row=i, column=1, pady=4)
        entries[chave] = e

    def submeter():
        vals = {}
        for chave, entry in entries.items():
            v = entry.get().strip()
            if chave in placeholders and v == placeholders[chave]:
                vals[chave] = ""
            else:
                vals[chave] = v
        callback(vals, win)

    btn = tk.Button(win, text="Confirmar", bg=GREEN, fg=BLACK_TEXT,
                    font=(FONT, 11, "bold"), relief="flat", cursor="hand2",
                    padx=20, pady=8, command=submeter)
    btn.pack(pady=(12, 20))


# ==============================
# PAINEL DE OUTPUT
# ==============================

class PainelOutput(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=CARD, **kwargs)
        self.configure(highlightbackground=GREEN, highlightthickness=1, highlightcolor=GREEN)

        text_frame = tk.Frame(self, bg=CARD)
        text_frame.pack(fill="both", expand=True, padx=2, pady=2)

        self._texto = scrolledtext.ScrolledText(
            text_frame, bg=CARD, fg=WHITE, font=(FONT, 10),
            relief="flat", state="disabled", wrap="word",
            selectbackground=GREEN, selectforeground=BLACK_TEXT,
            borderwidth=0, highlightthickness=0
        )
        self._texto.pack(fill="both", expand=True)

    def mostrar(self, texto):
        self._texto.config(state="normal")
        self._texto.delete("1.0", tk.END)
        self._texto.insert(tk.END, texto)
        self._texto.config(state="disabled")

    def limpar(self):
        self.mostrar("")


# ==============================
# MINI PLAYER
# ==============================

class MiniPlayer(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="#181818", height=72, **kwargs)
        self.pack(fill="x", side="bottom")
        self.pack_propagate(False)
        self.current_url = None
        self.current_spotify_url = None

        # ── esquerda: info da música ──
        left = tk.Frame(self, bg="#181818")
        left.pack(side="left", fill="y", padx=16)

        self.cover_lbl = tk.Label(left, text="♫", bg=HOVER, fg=GREEN,
                                   font=(FONT, 16), width=3, height=1)
        self.cover_lbl.pack(side="left", pady=14)

        info = tk.Frame(left, bg="#181818")
        info.pack(side="left", padx=10, fill="y", pady=14)

        self.now_playing_label = tk.Label(
            info, text="Nada a reproduzir", bg="#181818", fg=WHITE,
            font=(FONT, 10, "bold"), anchor="w", width=30
        )
        self.now_playing_label.pack(anchor="w")
        self.artist_label = tk.Label(
            info, text="–", bg="#181818", fg=GRAY,
            font=(FONT, 9), anchor="w"
        )
        self.artist_label.pack(anchor="w")

        # ── centro: botões ──
        center = tk.Frame(self, bg="#181818")
        center.pack(side="left", expand=True)

        self.btn_play = tk.Button(
            center, text="▶", bg=GREEN, fg=BLACK_TEXT,
            relief="flat", cursor="hand2", font=(FONT, 14, "bold"),
            width=3, command=self._abrir_spotify
        )
        self.btn_play.pack(side="left", padx=6)

        tk.Button(center, text="🔗 Abrir no Spotify", bg=HOVER, fg=WHITE,
                  relief="flat", cursor="hand2", font=(FONT, 9),
                  activebackground=GREEN, activeforeground=BLACK_TEXT,
                  command=self._abrir_spotify_url).pack(side="left", padx=4)

        self.is_playing = False
        self.current_music = None
        self.current_artist = None

    def set_music(self, titulo, artista, preview_url=None, spotify_url=None):
        self.current_music = titulo
        self.current_artist = artista
        self.current_url = preview_url
        self.current_spotify_url = spotify_url
        self.now_playing_label.config(text=titulo[:32])
        self.artist_label.config(text=artista[:28])
        self.btn_play.config(text="▶")
        self.is_playing = False

    def _abrir_spotify(self):
        """Abre a prévia (30s) no browser"""
        url = self.current_url or self.current_spotify_url
        if url:
            webbrowser.open(url)
            self.btn_play.config(text="⏸")
            self.is_playing = True
            if hasattr(self.master, "set_status"):
                self.master.set_status(f"🎵 A ouvir no Spotify: {self.current_music}")
        else:
            messagebox.showinfo("Info", "Nenhuma música selecionada. Usa 'Ver Top Músicas' para escolher.")

    def _abrir_spotify_url(self):
        url = self.current_spotify_url or self.current_url
        if url:
            webbrowser.open(url)
        else:
            messagebox.showinfo("Info", "Nenhuma música selecionada.")

    def _play_pause(self):
        self._abrir_spotify()

    def _next(self):
        pass

    def _prev(self):
        pass


# ==============================
# FORMATADORES
# ==============================

def fmt_utilizador(u):
    s = f"  ID               : {u['id_utilizador']}\n"
    s += f"  Nome Exibicao    : {u['nome_exibicao']}\n"
    s += f"  Username         : {u['nome_utilizador']}\n"
    s += f"  Pais             : {u['pais']}\n"
    s += f"  Nascimento       : {u['data_nascimento']}\n"
    s += f"  Estado           : {u['estado_conta']}\n"
    s += f"  Generos          : {', '.join(u['generos_preferidos'])}\n"
    s += f"  Seguidores       : {len(u['seguidores'])}\n"
    s += f"  Seguindo         : {len(u['seguidos'])}\n"
    s += f"  Playlists        : {len(u['playlists_publicas'])}\n"
    return s


def fmt_artista(a):
    s = f"  ID               : {a['id_artista']}\n"
    s += f"  Nome             : {a['nome']}\n"
    s += f"  Genero           : {a['genero']}\n"
    s += f"  Verificado       : {'Sim' if a['verificado'] else 'Nao'}\n"
    s += f"  Ouvintes Mensais : {a['ouvintes_mensais']}\n"
    s += f"  Seguidores       : {len(a['seguidores'])}\n"
    s += f"  Discografia      : {len(a['discografia'])} lancamento(s)\n"
    if a['discografia']:
        for d in a['discografia']:
            s += f"    - {d['tipo'].upper()} | {d['titulo']} ({d['ano']})\n"
    return s


def fmt_musica(m):
    s = f"  ID               : {m['id_musica']}\n"
    s += f"  Titulo           : {m['titulo']}\n"
    s += f"  ID Artista       : {m['id_artista']}\n"
    s += f"  Duracao          : {m['duracao_ms']} ms\n"
    s += f"  ISRC             : {m['isrc']}\n"
    s += f"  Lancamento       : {m['data_lancamento']}\n"
    s += f"  Letra            : {m['letra'][:50]}...\n"
    s += f"  Bitrate          : {m['bitrate']} kbps\n"
    s += f"  Reproducoes      : {m['contagem_reproducoes']}\n"
    s += f"  Explicito        : {'Sim' if m['flag_explicito'] else 'Nao'}\n"
    s += f"  Disponivel       : {'Sim' if m['disponibilidade'] else 'Nao'}\n"
    return s


def fmt_playlist(p):
    s = f"  ID               : {p['id_playlist']}\n"
    s += f"  Nome             : {p['nome_playlist']}\n"
    s += f"  Utilizador       : {p['id_utilizador']}\n"
    s += f"  Privacidade      : {p['privacidade']}\n"
    s += f"  Descricao        : {p['descricao']}\n"
    s += f"  Criada em        : {p['data_criacao']}\n"
    s += f"  Musicas          : {len(p['lista_ids'])}\n"
    s += f"  Seguidores       : {len(p['seguidores_playlist'])}\n"
    if p['lista_ids']:
        s += f"  IDs musicas      : {', '.join(p['lista_ids'][:5])}"
        if len(p['lista_ids']) > 5:
            s += f" (+{len(p['lista_ids']) - 5} mais)"
        s += "\n"
    return s


# ==============================
# TAB UTILIZADORES
# ==============================

class TabUtilizadores(tk.Frame):
    def __init__(self, master, output, **kw):
        super().__init__(master, bg=BG, **kw)
        self.output = output
        self._build()

    def _build(self):
        tk.Label(self, text="👤 Utilizadores", bg=BG, fg=WHITE,
                 font=(FONT, 16, "bold")).pack(anchor="w", padx=20, pady=(16, 8))

        btns = [
            ("➕ Criar", self._criar),
            ("📋 Listar todos", self._listar),
            ("🔍 Consultar por ID", self._consultar),
            ("🔎 Pesquisar", self._pesquisar),
            ("✏️ Atualizar", self._atualizar),
            ("🗑️ Remover", self._remover),
            ("🚫 Unfollow Artista", self._unfollow),
            ("📀 Minhas Playlists", self._minhas_playlists),
        ]
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=20)
        for txt, cmd in btns:
            _make_btn(bar, txt, cmd).pack(side="left", padx=4, pady=4)

    def _criar(self):
        campos = [
            ("Nome Exibicao", "nome"),
            ("Username", "nome_util"),
            ("URL Foto Perfil", "foto"),
            ("Pais", "pais"),
            ("Data Nascimento (DD/MM/AAAA)", "data"),
            ("Generos (virgula)", "generos"),
            ("Estado (ativo/inativo/premium)", "estado"),
        ]

        def cb(v, win):
            code, obj = criar_utilizador(
                v["nome"] or "", v["nome_util"] or "", v["foto"] or "",
                v["pais"] or "", v["data"] or "", v["generos"] or "", (v["estado"] or "").lower()
            )
            _handle(code, obj, win, self.output, lambda o: f"✅ Utilizador criado!\n\n{fmt_utilizador(o)}")

        abrir_form("Criar Utilizador", campos, cb)

    def _listar(self):
        code, obj = listar_utilizadores()
        if code == 200:
            txt = "👥 LISTA DE UTILIZADORES\n" + "─" * 50 + "\n"
            for u in obj.values():
                txt += fmt_utilizador(u) + "─" * 50 + "\n"
            self.output.mostrar(txt)
        else:
            self.output.mostrar(f"[{code}] {obj}")

    def _consultar(self):
        _pedir_id(self, "ID do Utilizador", lambda id_u: self._do_consultar(id_u))

    def _do_consultar(self, id_u):
        code, obj = consultar_utilizador(id_u)
        if code == 200:
            self.output.mostrar(fmt_utilizador(obj))
        else:
            self.output.mostrar(f"[{code}] {obj}")

    def _pesquisar(self):
        campos = [("Nome a pesquisar", "nome")]

        def cb(v, win):
            code, obj = pesquisar_utilizadores(v["nome"] or "")
            win.destroy()
            if code == 200:
                txt = "🔎 RESULTADOS\n" + "─" * 50 + "\n"
                for u in obj.values():
                    txt += fmt_utilizador(u) + "─" * 50 + "\n"
                self.output.mostrar(txt)
            else:
                self.output.mostrar(f"[{code}] {obj}")

        abrir_form("Pesquisar Utilizadores", campos, cb)

    def _atualizar(self):
        campos = [
            ("ID do Utilizador", "id_u"),
            ("Novo Nome (vazio=manter)", "nome"),
            ("Nova Foto URL (vazio=manter)", "foto"),
            ("Novo Pais (vazio=manter)", "pais"),
            ("Novo Estado (vazio=manter)", "estado"),
            ("Novos Generos (vazio=manter)", "generos"),
        ]

        def cb(v, win):
            code, obj = atualizar_utilizador(
                v["id_u"] or "",
                v["nome"] or None, v["foto"] or None, v["pais"] or None,
                (v["estado"] or "").lower() or None, v["generos"] or None
            )
            _handle(code, obj, win, self.output, lambda o: f"✅ Atualizado!\n\n{fmt_utilizador(o)}")

        abrir_form("Atualizar Utilizador", campos, cb)

    def _remover(self):
        _pedir_id(self, "ID do Utilizador", lambda id_u: self._do_remover(id_u))

    def _do_remover(self, id_u):
        code, obj = remover_utilizador(id_u)
        if code == 200:
            self.output.mostrar(f"🗑️ Utilizador {obj} removido com sucesso!")
        else:
            self.output.mostrar(f"[{code}] {obj}")

    def _unfollow(self):
        campos = [("ID Utilizador", "id_u"), ("ID Artista", "id_a")]

        def cb(v, win):
            code, obj = unfollow_artista(v["id_u"] or "", v["id_a"] or "")
            _handle(code, obj, win, self.output, lambda o: "🚫 Deixou de seguir o artista!")

        abrir_form("Unfollow Artista", campos, cb)

    def _minhas_playlists(self):
        _pedir_id(self, "ID do Utilizador", lambda id_u: self._do_minhas_playlists(id_u))

    def _do_minhas_playlists(self, id_u):
        code, obj = consultar_utilizador(id_u)
        if code == 200:
            playlists_ids = obj.get("playlists_publicas", [])
            if playlists_ids:
                txt = f"📀 PLAYLISTS DE {obj['nome_exibicao']}\n" + "─" * 50 + "\n"
                for p_id in playlists_ids:
                    p_code, playlist = consultar_playlist(p_id)
                    if p_code == 200:
                        txt += f"  📁 {playlist['nome_playlist']} (ID: {p_id}) - {len(playlist['lista_ids'])} musicas\n"
                self.output.mostrar(txt)
            else:
                self.output.mostrar("Nenhuma playlist encontrada para este utilizador")
        else:
            self.output.mostrar(f"[{code}] {obj}")


# ==============================
# TAB ARTISTAS
# ==============================

class TabArtistas(tk.Frame):
    def __init__(self, master, output, **kw):
        super().__init__(master, bg=BG, **kw)
        self.output = output
        self._build()

    def _build(self):
        tk.Label(self, text="🎤 Artistas", bg=BG, fg=WHITE,
                 font=(FONT, 16, "bold")).pack(anchor="w", padx=20, pady=(16, 8))

        btns = [
            ("➕ Criar", self._criar),
            ("📋 Listar", self._listar),
            ("🔍 Consultar", self._consultar),
            ("🔎 Pesquisar", self._pesquisar),
            ("✏️ Atualizar", self._atualizar),
            ("💿 Add Lancamento", self._add_lanc),
            ("⭐ Add Top Faixa", self._add_faixa),
            ("🗑️ Remover", self._remover),
            ("➕ Seguir Artista", self._seguir),
            ("🏆 Mais Seguidos", self._mais_seguidos),
        ]
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=20)
        for txt, cmd in btns:
            _make_btn(bar, txt, cmd).pack(side="left", padx=4, pady=4)

    def _criar(self):
        campos = [
            ("Nome", "nome"), ("Biografia", "bio"),
            ("URL Imagem", "imagem"), ("URL Capa", "imagem_capa"),
            ("Genero", "genero"), ("Verificado (s/n)", "verificado"),
        ]

        def cb(v, win):
            code, obj = criar_artista(
                v["nome"] or "", v["bio"] or "", v["imagem"] or "",
                v["imagem_capa"] or "", v["genero"] or "", (v["verificado"] or "").lower()
            )
            _handle(code, obj, win, self.output, lambda o: f"✅ Artista criado!\n\n{fmt_artista(o)}")

        abrir_form("Criar Artista", campos, cb)

    def _listar(self):
        code, obj = listar_artistas()
        if code == 200:
            txt = "🎵 LISTA DE ARTISTAS\n" + "─" * 50 + "\n"
            for a in obj.values():
                txt += fmt_artista(a) + "─" * 50 + "\n"
            self.output.mostrar(txt)
        else:
            self.output.mostrar(f"[{code}] {obj}")

    def _consultar(self):
        _pedir_id(self, "ID do Artista", lambda id_a: self._do_consultar(id_a))

    def _do_consultar(self, id_a):
        code, obj = consultar_artista(id_a)
        if code == 200:
            self.output.mostrar(fmt_artista(obj))
        else:
            self.output.mostrar(f"[{code}] {obj}")

    def _pesquisar(self):
        campos = [("Nome a pesquisar", "nome")]

        def cb(v, win):
            code, obj = pesquisar_artistas(v["nome"] or "")
            win.destroy()
            if code == 200:
                txt = "🔎 RESULTADOS\n" + "─" * 50 + "\n"
                for a in obj.values():
                    txt += fmt_artista(a) + "─" * 50 + "\n"
                self.output.mostrar(txt)
            else:
                self.output.mostrar(f"[{code}] {obj}")

        abrir_form("Pesquisar Artistas", campos, cb)

    def _atualizar(self):
        campos = [
            ("ID Artista", "id_a"),
            ("Novo Nome", "nome"), ("Nova Bio", "bio"),
            ("Nova URL Imagem", "imagem"), ("Nova URL Capa", "imagem_capa"),
            ("Novo Genero", "genero"), ("Verificado s/n", "verificado"),
            ("Ouvintes Mensais", "ouvintes"), ("Escolha Artista", "escolha"),
        ]

        def cb(v, win):
            code, obj = atualizar_artista(
                v["id_a"] or "",
                v["nome"] or None, v["bio"] or None,
                v["imagem"] or None, v["imagem_capa"] or None,
                v["genero"] or None,
                (v["verificado"] or "").lower() or None,
                v["ouvintes"] or None, v["escolha"] or None
            )
            _handle(code, obj, win, self.output, lambda o: f"✅ Artista atualizado!\n\n{fmt_artista(o)}")

        abrir_form("Atualizar Artista", campos, cb)

    def _add_lanc(self):
        campos = [("ID Artista", "id_a"), ("Titulo", "titulo"),
                  ("Tipo (album/ep/single)", "tipo"), ("Ano", "ano")]

        def cb(v, win):
            code, obj = adicionar_lancamento(
                v["id_a"] or "", v["titulo"] or "",
                (v["tipo"] or "").lower(), v["ano"] or ""
            )
            _handle(code, obj, win, self.output, lambda o: f"💿 Lancamento adicionado!\n\n{fmt_artista(o)}")

        abrir_form("Adicionar Lancamento", campos, cb)

    def _add_faixa(self):
        campos = [("ID Artista", "id_a"), ("Nome da Faixa", "faixa")]

        def cb(v, win):
            code, obj = adicionar_top_faixa(v["id_a"] or "", v["faixa"] or "")
            _handle(code, obj, win, self.output, lambda o: "⭐ Top faixa adicionada!")

        abrir_form("Adicionar Top Faixa", campos, cb)

    def _remover(self):
        _pedir_id(self, "ID do Artista", lambda id_a: self._do_remover(id_a))

    def _do_remover(self, id_a):
        code, obj = remover_artista(id_a)
        if code == 200:
            self.output.mostrar(f"🗑️ Artista {obj} removido com sucesso!")
        else:
            self.output.mostrar(f"[{code}] {obj}")

    def _seguir(self):
        campos = [("ID Utilizador", "id_u"), ("ID Artista", "id_a")]

        def cb(v, win):
            code, obj = seguir_artista(v["id_u"] or "", v["id_a"] or "")
            _handle(code, obj, win, self.output, lambda o: "➕ Agora segue o artista!")

        abrir_form("Seguir Artista", campos, cb)

    def _mais_seguidos(self):
        from artistas import carregar_artistas
        artistas = carregar_artistas()
        sorted_artistas = sorted(artistas.values(), key=lambda x: len(x['seguidores']), reverse=True)[:10]

        txt = "🏆 ARTISTAS MAIS SEGUIDOS\n" + "─" * 50 + "\n"
        for i, a in enumerate(sorted_artistas, 1):
            txt += f"{i}. {a['nome']} - {len(a['seguidores'])} seguidores\n"
            if a.get('verificado'):
                txt += "   ✓ Verificado\n"
        self.output.mostrar(txt)


# ==============================
# TAB MUSICAS
# ==============================

class TabMusicas(tk.Frame):
    def __init__(self, master, output, **kw):
        super().__init__(master, bg=BG, **kw)
        self.output = output
        self._build()

    def _build(self):
        tk.Label(self, text="🎵 Musicas", bg=BG, fg=WHITE,
                 font=(FONT, 16, "bold")).pack(anchor="w", padx=20, pady=(16, 8))

        btns = [
            ("➕ Criar", self._criar),
            ("📋 Listar", self._listar),
            ("🔍 Consultar", self._consultar),
            ("🔎 Pesquisar", self._pesquisar),
            ("✏️ Atualizar", self._atualizar),
            ("🗑️ Remover", self._remover),
            ("🎵 Reproduzir", self._reproduzir),
            ("🏆 Top Musicas", self._top_musicas),
        ]
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=20)
        for txt, cmd in btns:
            _make_btn(bar, txt, cmd).pack(side="left", padx=4, pady=4)

    def _criar(self):
        campos = [
            ("Titulo", "titulo"), ("ID Artista", "id_artista"),
            ("Duracao ms", "duracao_ms"), ("ISRC (12 chars)", "isrc"),
            ("Data Lancamento (DD/MM/AAAA)", "data"),
            ("Letra", "letra"), ("Bitrate (320)", "bitrate"),
            ("Explicito (s/n)", "explicito"),
            ("Takedown (s/n)", "takedown"),
            ("Disponivel (s/n)", "disponivel"),
        ]

        def cb(v, win):
            code, obj = criar_musica(
                v["titulo"] or "", v["id_artista"] or "", v["duracao_ms"] or "",
                v["isrc"] or "", v["data"] or "", v["letra"] or "",
                v["bitrate"] or "", (v["explicito"] or "").lower(),
                (v["takedown"] or "").lower(), (v["disponivel"] or "").lower()
            )
            _handle(code, obj, win, self.output, lambda o: f"✅ Musica criada!\n\n{fmt_musica(o)}")

        abrir_form("Criar Musica", campos, cb)

    def _listar(self):
        code, obj = listar_musicas()
        if code == 200:
            txt = "🎶 LISTA DE MUSICAS\n" + "─" * 50 + "\n"
            for m in obj.values():
                txt += fmt_musica(m) + "─" * 50 + "\n"
            self.output.mostrar(txt)
        else:
            self.output.mostrar(f"[{code}] {obj}")

    def _consultar(self):
        _pedir_id(self, "ID da Musica", lambda id_m: self._do_consultar(id_m))

    def _do_consultar(self, id_m):
        code, obj = consultar_musica(id_m)
        if code == 200:
            self.output.mostrar(fmt_musica(obj))
        else:
            self.output.mostrar(f"[{code}] {obj}")

    def _pesquisar(self):
        campos = [("Titulo a pesquisar", "titulo")]

        def cb(v, win):
            code, obj = pesquisar_musicas(v["titulo"] or "")
            win.destroy()
            if code == 200:
                txt = "🔎 RESULTADOS\n" + "─" * 50 + "\n"
                for m in obj.values():
                    txt += fmt_musica(m) + "─" * 50 + "\n"
                self.output.mostrar(txt)
            else:
                self.output.mostrar(f"[{code}] {obj}")

        abrir_form("Pesquisar Musicas", campos, cb)

    def _atualizar(self):
        campos = [
            ("ID Musica", "id_m"),
            ("Novo Titulo", "titulo"), ("Nova Duracao ms", "duracao"),
            ("Nova Letra", "letra"), ("Novo Bitrate", "bitrate"),
            ("Explicito s/n", "explicito"), ("Disponivel s/n", "disponivel"),
        ]

        def cb(v, win):
            code, obj = atualizar_musica(
                v["id_m"] or "",
                v["titulo"] or None, v["duracao"] or None,
                v["letra"] or None, v["bitrate"] or None,
                (v["explicito"] or "").lower() or None,
                (v["disponivel"] or "").lower() or None
            )
            _handle(code, obj, win, self.output, lambda o: f"✅ Musica atualizada!\n\n{fmt_musica(o)}")

        abrir_form("Atualizar Musica", campos, cb)

    def _remover(self):
        _pedir_id(self, "ID da Musica", lambda id_m: self._do_remover(id_m))

    def _do_remover(self, id_m):
        code, obj = remover_musica(id_m)
        if code == 200:
            self.output.mostrar(f"🗑️ Musica {obj} removida com sucesso!")
        else:
            self.output.mostrar(f"[{code}] {obj}")

    def _reproduzir(self):
        win = tk.Toplevel()
        win.title("Reproduzir Musica")
        win.configure(bg=BG)
        win.resizable(False, False)
        win.grab_set()

        tk.Label(win, text="🎵 Reproduzir Musica", bg=BG, fg=GREEN,
                 font=(FONT, 14, "bold")).pack(pady=(18, 6), padx=24)

        frame = tk.Frame(win, bg=BG)
        frame.pack(padx=24, pady=6)

        tk.Label(frame, text="ID da Musica:", bg=BG, fg=GRAY,
                 font=(FONT, 10)).grid(row=0, column=0, sticky="w", pady=4, padx=(0, 12))
        entry_musica = tk.Entry(frame, bg=INPUT_BG, fg=WHITE, font=(FONT, 10), width=30)
        entry_musica.grid(row=0, column=1, pady=4)

        tk.Label(frame, text="ID do Utilizador:", bg=BG, fg=GRAY,
                 font=(FONT, 10)).grid(row=1, column=0, sticky="w", pady=4, padx=(0, 12))
        entry_user = tk.Entry(frame, bg=INPUT_BG, fg=WHITE, font=(FONT, 10), width=30)
        entry_user.grid(row=1, column=1, pady=4)

        def reproduzir():
            id_m = entry_musica.get().strip()
            id_u = entry_user.get().strip()
            if not id_m or not id_u:
                messagebox.showerror("Erro", "Preencha ambos os IDs", parent=win)
                return

            code, obj = registar_reproducao(id_m, id_u)
            if code == 200:
                from artistas import consultar_artista
                musica = obj
                a_code, artista = consultar_artista(musica['id_artista'])
                nome_artista = artista['nome'] if a_code == 200 else "Artista"

                if hasattr(self.master, 'mini_player'):
                    self.master.mini_player.set_music(musica['titulo'], nome_artista)
                    self.master.mini_player.is_playing = True
                    self.master.mini_player.btn_play.config(text="⏸")
                    self.master.set_status(f"🎵 A reproduzir: {musica['titulo']}")

                win.destroy()
                self.output.mostrar(f"✅ Musica reproduzida!\n\n{fmt_musica(musica)}")
            else:
                messagebox.showerror("Erro", f"[{code}] {obj}", parent=win)

        btn = tk.Button(win, text="▶ Reproduzir", bg=GREEN, fg=BLACK_TEXT,
                        font=(FONT, 11, "bold"), relief="flat", cursor="hand2",
                        padx=20, pady=8, command=reproduzir)
        btn.pack(pady=(12, 20))

    def _top_musicas(self):
        musicas = carregar_musicas()
        sorted_musicas = sorted(musicas.values(), key=lambda x: x['contagem_reproducoes'], reverse=True)[:10]

        txt = "🏆 TOP 10 MÚSICAS MAIS REPRODUZIDAS\n" + "─" * 50 + "\n"
        for i, m in enumerate(sorted_musicas, 1):
            txt += f"{i}. {m['titulo']} - {m['contagem_reproducoes']} reproduções\n"
            txt += f"   ID: {m['id_musica']}\n"
        self.output.mostrar(txt)


# ==============================
# TAB PLAYLISTS
# ==============================

class TabPlaylists(tk.Frame):
    def __init__(self, master, output, **kw):
        super().__init__(master, bg=BG, **kw)
        self.output = output
        self._build()

    def _build(self):
        tk.Label(self, text="📀 Playlists", bg=BG, fg=WHITE,
                 font=(FONT, 16, "bold")).pack(anchor="w", padx=20, pady=(16, 8))

        btns = [
            ("➕ Criar", self._criar),
            ("📋 Listar", self._listar),
            ("🔍 Consultar", self._consultar),
            ("✏️ Atualizar", self._atualizar),
            ("🎵 Add Musica", self._add_musica),
            ("🗑️ Rem Musica", self._rem_musica),
            ("🗑️ Remover", self._remover),
            ("➕ Seguir Playlist", self._seguir),
            ("⭐ Playlists Spotify", self._ver_playlists_spotify),
        ]
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=20)
        for txt, cmd in btns:
            _make_btn(bar, txt, cmd).pack(side="left", padx=4, pady=4)

    def _criar(self):
        campos = [
            ("Nome Playlist", "nome"), ("ID Utilizador", "id_u"),
            ("Privacidade (publica/privada)", "priv"),
            ("Descricao", "desc"), ("URL Capa", "capa"),
        ]

        def cb(v, win):
            code, obj = criar_playlist(
                v["nome"] or "", v["id_u"] or "",
                (v["priv"] or "").lower(), v["desc"] or "", v["capa"] or ""
            )
            _handle(code, obj, win, self.output, lambda o: f"✅ Playlist criada!\n\n{fmt_playlist(o)}")

        abrir_form("Criar Playlist", campos, cb)

    def _listar(self):
        code, obj = listar_playlists()
        if code == 200:
            txt = "📀 LISTA DE PLAYLISTS\n" + "─" * 50 + "\n"
            for p in obj.values():
                txt += fmt_playlist(p) + "─" * 50 + "\n"
            self.output.mostrar(txt)
        else:
            self.output.mostrar(f"[{code}] {obj}")

    def _consultar(self):
        _pedir_id(self, "ID da Playlist", lambda id_p: self._do_consultar(id_p))

    def _do_consultar(self, id_p):
        code, obj = consultar_playlist(id_p)
        if code == 200:
            self.output.mostrar(fmt_playlist(obj))
        else:
            self.output.mostrar(f"[{code}] {obj}")

    def _atualizar(self):
        campos = [
            ("ID Playlist", "id_p"),
            ("Novo Nome", "nome"), ("Nova Privacidade", "priv"),
            ("Nova Descricao", "desc"), ("Flag Remocao s/n", "flag"),
        ]

        def cb(v, win):
            code, obj = atualizar_playlist(
                v["id_p"] or "",
                v["nome"] or None,
                (v["priv"] or "").lower() or None,
                v["desc"] or None,
                (v["flag"] or "").lower() or None
            )
            _handle(code, obj, win, self.output, lambda o: f"✅ Playlist atualizada!\n\n{fmt_playlist(o)}")

        abrir_form("Atualizar Playlist", campos, cb)

    def _add_musica(self):
        campos = [("ID Playlist", "id_p"), ("ID Musica", "id_m")]

        def cb(v, win):
            code, obj = adicionar_musica_playlist(v["id_p"] or "", v["id_m"] or "")
            _handle(code, obj, win, self.output, lambda o: "🎵 Musica adicionada a playlist!")

        abrir_form("Adicionar Musica a Playlist", campos, cb)

    def _rem_musica(self):
        campos = [("ID Playlist", "id_p"), ("ID Musica", "id_m")]

        def cb(v, win):
            code, obj = remover_musica_playlist(v["id_p"] or "", v["id_m"] or "")
            _handle(code, obj, win, self.output, lambda o: "🗑️ Musica removida da playlist!")

        abrir_form("Remover Musica da Playlist", campos, cb)

    def _remover(self):
        _pedir_id(self, "ID da Playlist", lambda id_p: self._do_remover(id_p))

    def _do_remover(self, id_p):
        code, obj = remover_playlist(id_p)
        if code == 200:
            self.output.mostrar(f"🗑️ Playlist {obj} removida com sucesso!")
        else:
            self.output.mostrar(f"[{code}] {obj}")

    def _seguir(self):
        campos = [("ID Utilizador", "id_u"), ("ID Playlist", "id_p")]

        def cb(v, win):
            code, obj = seguir_playlist(v["id_u"] or "", v["id_p"] or "")
            _handle(code, obj, win, self.output, lambda o: "➕ Agora segue a playlist!")

        abrir_form("Seguir Playlist", campos, cb)

    def _ver_playlists_spotify(self):
        """Mostra as 3 playlists pre-definidas do sistema com botoes de reproduzir"""
        from Playlist import carregar_playlists
        playlists = carregar_playlists()

        ids = [_ID_PL_TOP, _ID_PL_BESTOF, _ID_PL_ESSENC]
        encontradas = [playlists[i] for i in ids if i in playlists]

        if not encontradas:
            self.output.mostrar("As playlists pre-definidas ainda nao foram criadas.\nReinicia a aplicacao.")
            return

        txt = "PLAYLISTS PRE-DEFINIDAS DO SPOTIFY MANAGER\n" + "=" * 55 + "\n\n"
        for p in encontradas:
            txt += f"  ID       : {p['id_playlist']}\n"
            txt += f"  Nome     : {p['nome_playlist']}\n"
            txt += f"  Descricao: {p['descricao']}\n"
            txt += f"  Criada   : {p['data_criacao']}\n"
            txt += f"  Musicas  : {len(p['lista_ids'])}\n"
            txt += f"  Seguidor.: {len(p['seguidores_playlist'])}\n\n"
        self.output.mostrar(txt)

        # Frame de botoes de reproducao
        win = tk.Toplevel()
        win.title("Playlists Pre-definidas")
        win.configure(bg=BG)
        win.resizable(False, False)

        tk.Label(win, text="Playlists Pre-definidas", bg=BG, fg=GREEN,
                 font=(FONT, 13, "bold")).pack(pady=(16, 6), padx=24)

        for p in encontradas:
            row = tk.Frame(win, bg=BG)
            row.pack(fill="x", padx=20, pady=4)
            tk.Label(row, text=p['nome_playlist'], bg=BG, fg=WHITE,
                     font=(FONT, 10), width=32, anchor="w").pack(side="left")
            query = p.get('spotify_query', p['nome_playlist']).replace(' ', '+')
            url = f"https://open.spotify.com/search/{query}/playlists"
            _make_btn(row, "▶ Reproduzir",
                      lambda u=url: webbrowser.open(u)).pack(side="left", padx=6)

        tk.Button(win, text="Fechar", bg=HOVER, fg=WHITE,
                  font=(FONT, 10), relief="flat", cursor="hand2",
                  padx=16, pady=6, command=win.destroy).pack(pady=(8, 16))


# ==============================
# TAB SPOTIFY ONLINE
# ==============================

class TabSpotifyOnline(tk.Frame):
    def __init__(self, master, output, **kw):
        super().__init__(master, bg=BG, **kw)
        self.output = output
        self._build()

    def _build(self):
        tk.Label(self, text="🌐 Spotify Online", bg=BG, fg=WHITE,
                 font=(FONT, 18, "bold")).pack(anchor="w", padx=20, pady=(16, 6))

        # ── Botões de ação rápida ──────────────────────────────────────────
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=20, pady=(0, 12))
        _make_btn(bar, "🌍 Músicas Populares", self._musicas_populares).pack(side="left", padx=(0, 6))
        _make_btn(bar, "🔧 Testar Conexão",    self._testar_conexao).pack(side="left")

        # ── Barra de pesquisa de MÚSICAS ──────────────────────────────────
        tk.Label(self, text="🎵  Pesquisar Músicas", bg=BG, fg=GRAY,
                 font=(FONT, 9, "bold")).pack(anchor="w", padx=22)

        row_m = tk.Frame(self, bg=HOVER, pady=0)
        row_m.pack(fill="x", padx=20, pady=(2, 10))

        tk.Label(row_m, text="🔍", bg=HOVER, fg=GRAY,
                 font=(FONT, 11)).pack(side="left", padx=(10, 4))

        self.music_entry = tk.Entry(
            row_m, bg=HOVER, fg=WHITE, insertbackground=WHITE,
            font=(FONT, 11), relief="flat", bd=0,
            highlightthickness=0
        )
        self.music_entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.music_entry.bind("<Return>", lambda e: self._pesquisar_musicas())
        self.music_entry.bind("<FocusIn>",  lambda e: row_m.config(bg=INPUT_BG) or self.music_entry.config(bg=INPUT_BG))
        self.music_entry.bind("<FocusOut>", lambda e: row_m.config(bg=HOVER)    or self.music_entry.config(bg=HOVER))

        _make_btn(row_m, "Pesquisar", self._pesquisar_musicas).pack(side="right", padx=6, pady=4)

        # ── Barra de pesquisa de ARTISTAS ─────────────────────────────────
        tk.Label(self, text="🎤  Pesquisar Artistas", bg=BG, fg=GRAY,
                 font=(FONT, 9, "bold")).pack(anchor="w", padx=22)

        row_a = tk.Frame(self, bg=HOVER, pady=0)
        row_a.pack(fill="x", padx=20, pady=(2, 10))

        tk.Label(row_a, text="🔍", bg=HOVER, fg=GRAY,
                 font=(FONT, 11)).pack(side="left", padx=(10, 4))

        self.artist_entry = tk.Entry(
            row_a, bg=HOVER, fg=WHITE, insertbackground=WHITE,
            font=(FONT, 11), relief="flat", bd=0,
            highlightthickness=0
        )
        self.artist_entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.artist_entry.bind("<Return>", lambda e: self._pesquisar_artistas())
        self.artist_entry.bind("<FocusIn>",  lambda e: row_a.config(bg=INPUT_BG) or self.artist_entry.config(bg=INPUT_BG))
        self.artist_entry.bind("<FocusOut>", lambda e: row_a.config(bg=HOVER)    or self.artist_entry.config(bg=HOVER))

        _make_btn(row_a, "Pesquisar", self._pesquisar_artistas).pack(side="right", padx=6, pady=4)

        # ── Frame de resultados (botões de prévia) ─────────────────────────
        self.artist_buttons_frame = tk.Frame(self, bg=BG)
        self.artist_buttons_frame.pack(fill="x", padx=20, pady=4)

    def _musicas_populares(self):
        self.output.mostrar("🌍 A buscar músicas populares... Aguarde...")
        self.update()

        def buscar():
            code, resultado = get_musicas_populares(20)
            self.after(0, lambda: self._mostrar_musicas_populares(code, resultado))

        threading.Thread(target=buscar, daemon=True).start()

    def _mostrar_musicas_populares(self, code, resultado):
        if code == 200:
            txt = "MUSICAS POPULARES DO MOMENTO\n" + "=" * 70 + "\n\n"
            for m in resultado:
                txt += f"#{m['posicao']:2d} {m['titulo']}\n     {m['artista']}\n     Album: {m['album']}\n"
                txt += "     preview ok\n" if m.get('preview_url') else "     (abre no Spotify)\n"
                txt += "\n"
            self.output.mostrar(txt)

            # Botoes ▶ para as top 5
            for widget in self.artist_buttons_frame.winfo_children():
                widget.destroy()
            tk.Label(self.artist_buttons_frame, text="▶ Reproduzir — Populares:",
                     bg=BG, fg=GREEN, font=(FONT, 10, "bold")).pack(anchor="w", pady=(4, 2))
            btn_row = tk.Frame(self.artist_buttons_frame, bg=BG)
            btn_row.pack(fill="x")
            for m in resultado[:5]:
                titulo_enc = m['titulo'].replace(' ', '+')
                artista_enc = m['artista'].replace(' ', '+')
                url_fallback = f"https://open.spotify.com/search/{artista_enc}+{titulo_enc}/tracks"
                url = m.get('preview_url') or url_fallback
                _make_btn(btn_row, f"▶ {m['titulo'][:22]}",
                          lambda u=url, t=m['titulo'], a=m['artista']: self._reproduzir_musica(u, t, a)
                          ).pack(side="left", padx=3, pady=2)
        else:
            self.output.mostrar(f"[{code}] {resultado}")

    def _pesquisar_musicas(self):
        query = self.music_entry.get().strip()
        if not query:
            messagebox.showwarning("Aviso", "Digite o nome da música!")
            return
        self.output.mostrar(f"🔍 A pesquisar por '{query}'...")
        self.update()

        def buscar():
            code, resultado = sp_pesquisar_musicas(query, 15)
            self.after(0, lambda: self._mostrar_musicas(code, resultado, query))

        threading.Thread(target=buscar, daemon=True).start()

    def _mostrar_musicas(self, code, resultado, query):
        if code == 200:
            txt = f"RESULTADOS PARA '{query.upper()}'\n" + "=" * 70 + "\n\n"
            for i, m in enumerate(resultado, 1):
                txt += f"{i:2d}. {m['titulo']}\n     {m['artista_principal']}\n     Album: {m['album']}\n     {m['duracao_ms'] // 60000}:{(m['duracao_ms'] // 1000) % 60:02d}"
                txt += "  preview ok\n" if m.get('preview_url') else "  (abre no Spotify)\n"
                txt += "\n"
            self.output.mostrar(txt)

            # Botoes de reproduzir para as primeiras 5 musicas — sempre visíveis
            for widget in self.artist_buttons_frame.winfo_children():
                widget.destroy()
            tk.Label(self.artist_buttons_frame, text=f"▶ Reproduzir — '{query}':",
                     bg=BG, fg=GREEN, font=(FONT, 10, "bold")).pack(anchor="w", pady=(4, 2))
            btn_row = tk.Frame(self.artist_buttons_frame, bg=BG)
            btn_row.pack(fill="x")
            for m in resultado[:5]:
                titulo_enc = m['titulo'].replace(' ', '+')
                artista_enc = m['artista_principal'].replace(' ', '+')
                url_fallback = f"https://open.spotify.com/search/{artista_enc}+{titulo_enc}/tracks"
                url = m.get('preview_url') or url_fallback
                _make_btn(btn_row, f"▶ {m['titulo'][:22]}",
                          lambda u=url, t=m['titulo'], a=m['artista_principal']: self._reproduzir_musica(u, t, a)
                          ).pack(side="left", padx=3, pady=2)
        else:
            self.output.mostrar(f"[{code}] {resultado}")

    def _reproduzir_musica(self, url, titulo, artista):
        # Atualiza o mini player e abre no browser
        app = self.winfo_toplevel()
        if hasattr(app, 'mini_player'):
            app.mini_player.set_music(titulo, artista, url, url)
        webbrowser.open(url)

    def _pesquisar_artistas(self):
        query = self.artist_entry.get().strip()
        if not query:
            messagebox.showwarning("Aviso", "Digite o nome do artista!")
            return
        self.output.mostrar(f"🔍 A pesquisar por artista '{query}'...")
        self.update()

        def buscar():
            code, resultado = sp_pesquisar_artistas(query, 10)
            self.after(0, lambda: self._mostrar_artistas(code, resultado, query))

        threading.Thread(target=buscar, daemon=True).start()

    def _mostrar_artistas(self, code, resultado, query):
        for widget in self.artist_buttons_frame.winfo_children():
            widget.destroy()
        if code == 200:
            txt = f"🔎 ARTISTAS ENCONTRADOS PARA '{query.upper()}'\n" + "═" * 70 + "\n\n"
            for i, a in enumerate(resultado, 1):
                seguidores = f"{a['seguidores']:,}" if a.get('seguidores') else "A carregar..."
                txt += f"{i:2d}. 🎤 {a['nome']}\n     👥 Seguidores: {seguidores}\n"
                if a.get('generos'):
                    txt += f"     🏷️ Géneros: {', '.join(a['generos'][:3])}\n"
                txt += f"     🔗 {a['url']}\n\n"

                # Bloco de botões por artista
                sep = tk.Frame(self.artist_buttons_frame, bg=GREEN, height=1)
                sep.pack(fill="x", pady=(6, 2))
                nome_label = tk.Label(self.artist_buttons_frame,
                                      text=f"🎤 {a['nome']}  |  👥 Seguidores: {seguidores}",
                                      bg=BG, fg=WHITE, font=(FONT, 9, "bold"))
                nome_label.pack(anchor="w")

                btn_frame = tk.Frame(self.artist_buttons_frame, bg=BG)
                btn_frame.pack(fill="x", pady=2)
                _make_btn(btn_frame, "🖼️ Ver Imagem",
                          lambda aid=a['id'], aimg=a.get('imagem'): self._ver_imagem(aid, aimg)).pack(side="left", padx=2)
                _make_btn(btn_frame, "▶ 5 Músicas",
                          lambda aid=a['id'], anome=a['nome']: self._reproduzir_5_musicas(aid, anome)).pack(side="left", padx=2)
                _make_btn(btn_frame, "📋 3 Playlists",
                          lambda aid=a['id'], anome=a['nome']: self._mostrar_playlists_artista(aid, anome)).pack(side="left", padx=2)
                _make_btn(btn_frame, "🔗 Spotify",
                          lambda url=a['url']: webbrowser.open(url)).pack(side="left", padx=2)

                # Se seguidores = 0, buscar valor real em background
                if not a.get('seguidores'):
                    self._atualizar_seguidores(a['id'], nome_label)

            self.output.mostrar(txt)
        else:
            self.output.mostrar(f"[{code}] {resultado}")

    def _atualizar_seguidores(self, artista_id, label):
        """Busca seguidores reais do endpoint do artista e atualiza o label"""
        def buscar():
            code, token_result = __import__('spotify_online')._obter_token()
            if code == 200:
                try:
                    import requests as req
                    r = req.get(f"https://api.spotify.com/v1/artists/{artista_id}",
                                headers={"Authorization": f"Bearer {token_result}"}, timeout=8)
                    if r.status_code == 200:
                        dados = r.json()
                        total = dados.get("followers", {}).get("total", 0)
                        nome = dados.get("name", "")
                        seg_txt = f"{total:,}" if total else "N/D"
                        self.after(0, lambda: label.config(
                            text=f"🎤 {nome}  |  👥 Seguidores: {seg_txt}"))
                except Exception:
                    pass
        threading.Thread(target=buscar, daemon=True).start()

    def _reproduzir_5_musicas(self, artista_id, artista_nome):
        """Busca e mostra 5 músicas com botões de reproduzir"""
        self.output.mostrar(f"🎵 A carregar músicas de {artista_nome}...")

        def buscar():
            code, musicas = get_musicas_artista(artista_id, 5)
            self.after(0, lambda: self._mostrar_5_musicas_play(code, musicas, artista_nome))

        threading.Thread(target=buscar, daemon=True).start()

    def _mostrar_5_musicas_play(self, code, musicas, artista_nome):
        if code != 200:
            self.output.mostrar(f"[{code}] {musicas}")
            return

        txt = f"🎵 TOP 5 MUSICAS -- {artista_nome.upper()}\n" + "=" * 60 + "\n\n"
        for i, m in enumerate(musicas[:5], 1):
            mins = m['duracao_ms'] // 60000
            secs = (m['duracao_ms'] // 1000) % 60
            txt += f"  {i}. {m['titulo']}\n"
            txt += f"     Album: {m['album']}  {mins}:{secs:02d}"
            txt += "  preview ok\n" if m.get('preview_url') else "  (abre no Spotify)\n"
            txt += "\n"
        self.output.mostrar(txt)

        for widget in self.artist_buttons_frame.winfo_children():
            widget.destroy()

        tk.Label(self.artist_buttons_frame,
                 text=f"▶ Reproduzir — {artista_nome}",
                 bg=BG, fg=GREEN, font=(FONT, 10, "bold")).pack(anchor="w", pady=(4, 2))
        btn_row = tk.Frame(self.artist_buttons_frame, bg=BG)
        btn_row.pack(fill="x")
        for m in musicas[:5]:
            # preview_url = 30s audio direto; fallback = busca no Spotify
            titulo_enc = m['titulo'].replace(' ', '+')
            artista_enc = artista_nome.replace(' ', '+')
            url_fallback = f"https://open.spotify.com/search/{artista_enc}+{titulo_enc}/tracks"
            url = m.get('preview_url') or url_fallback
            _make_btn(btn_row, f"▶ {m['titulo'][:24]}",
                      lambda u=url, t=m['titulo'], a=artista_nome: self._reproduzir_musica(u, t, a)
                      ).pack(side="left", padx=3, pady=2)

    def _mostrar_playlists_artista(self, artista_id, artista_nome):
        """Define 3 playlists temáticas para o artista com botão reproduzir"""
        for widget in self.artist_buttons_frame.winfo_children():
            widget.destroy()

        playlists = [
            {"nome": f"🔥 {artista_nome} – Top Hits",      "query": f"{artista_nome} top hits"},
            {"nome": f"🌙 {artista_nome} – Best Of",        "query": f"{artista_nome} best songs"},
            {"nome": f"🎧 {artista_nome} – Álbuns Essenc.", "query": f"{artista_nome} essential albums"},
        ]

        txt = f"📋 PLAYLISTS DE {artista_nome.upper()}\n" + "═" * 60 + "\n\n"
        for i, pl in enumerate(playlists, 1):
            txt += f"  {i}. {pl['nome']}\n"
        txt += "\n💡 Clique em '▶ Reproduzir' para abrir a playlist no Spotify."
        self.output.mostrar(txt)

        tk.Label(self.artist_buttons_frame,
                 text=f"📋 Playlists — {artista_nome}",
                 bg=BG, fg=GREEN, font=(FONT, 10, "bold")).pack(anchor="w", pady=(4, 2))

        for pl in playlists:
            row = tk.Frame(self.artist_buttons_frame, bg=BG)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=pl['nome'], bg=BG, fg=WHITE,
                     font=(FONT, 9), width=35, anchor="w").pack(side="left")
            query_encoded = pl['query'].replace(' ', '+')
            url_spotify = f"https://open.spotify.com/search/{query_encoded}/playlists"
            _make_btn(row, "▶ Reproduzir Playlist",
                      lambda u=url_spotify: webbrowser.open(u)).pack(side="left", padx=4)

    def _reproduzir_musica(self, url, titulo, artista):
        app = self.winfo_toplevel()
        if hasattr(app, 'mini_player'):
            app.mini_player.set_music(titulo, artista, url, url)
        webbrowser.open(url)

    def _ver_imagem(self, artista_id, imagem_url):
        if imagem_url:
            webbrowser.open(imagem_url)
            messagebox.showinfo("Info", "Imagem a abrir no navegador!", parent=self)
        else:
            self.output.mostrar("🔍 A buscar imagem do artista...")

            def buscar():
                code, url = obter_imagem_artista(artista_id)
                if code == 200:
                    self.after(0, lambda: webbrowser.open(url))
                    self.after(0, lambda: messagebox.showinfo("Info", "Imagem a abrir no navegador!", parent=self))
                else:
                    self.after(0, lambda: messagebox.showinfo("Info", "Artista sem imagem disponível", parent=self))

            threading.Thread(target=buscar, daemon=True).start()

    def _ver_musicas_artista(self, artista_id, artista_nome):
        self.output.mostrar(f"🎵 A buscar músicas de {artista_nome}...")
        self.update()

        def buscar():
            code, resultado = get_musicas_artista(artista_id, 10)
            self.after(0, lambda: self._mostrar_musicas_artista(code, resultado, artista_nome))

        threading.Thread(target=buscar, daemon=True).start()

    def _mostrar_musicas_artista(self, code, resultado, artista_nome):
        if code == 200:
            txt = f"🎵 TOP MÚSICAS DE {artista_nome.upper()}\n" + "═" * 70 + "\n\n"
            for i, m in enumerate(resultado, 1):
                txt += f"{i:2d}. {m['titulo']}\n     📀 Álbum: {m['album']}\n     ⏱️ {m['duracao_ms'] // 60000}:{(m['duracao_ms'] // 1000) % 60:02d}\n"
                if m.get('preview_url'):
                    txt += f"     🎧 Prévia disponível\n"
                txt += "\n"
            self.output.mostrar(txt)

            for widget in self.artist_buttons_frame.winfo_children():
                widget.destroy()
            tk.Label(self.artist_buttons_frame, text="🎵 Clique para ouvir a prévia:", bg=BG, fg=GREEN, font=(FONT, 10, "bold")).pack(anchor="w", pady=5)
            for i, m in enumerate(resultado[:5]):
                if m.get('preview_url'):
                    btn_frame = tk.Frame(self.artist_buttons_frame, bg=BG)
                    btn_frame.pack(fill="x", pady=2)
                    _make_btn(btn_frame, f"🎧 {m['titulo']}", lambda url=m['preview_url']: self._tocar_previa(url)).pack(side="left", padx=2)
        else:
            self.output.mostrar(f"[{code}] {resultado}")

    def _tocar_previa(self, preview_url):
        if not preview_url:
            messagebox.showinfo("Info", "Prévia não disponível para esta música", parent=self)
            return
        webbrowser.open(preview_url)
        messagebox.showinfo("🎵 Prévia", "A música vai abrir no seu navegador!\nClique no play para ouvir os 30 segundos.", parent=self)

    def _testar_conexao(self):
        self.output.mostrar("🔧 A testar conexão com Spotify API...")
        self.update()

        def testar():
            code, msg = testar_conexao()
            self.after(0, lambda: self.output.mostrar(f"[{code}] {msg}"))

        threading.Thread(target=testar, daemon=True).start()


# ==============================
# TAB ARTISTAS POPULARES
# ==============================

class TabArtistasPopulares(tk.Frame):
    def __init__(self, master, output, **kw):
        super().__init__(master, bg=BG, **kw)
        self.output = output
        self._build()

    def _build(self):
        tk.Label(self, text="⭐ Artistas Populares", bg=BG, fg=WHITE,
                 font=(FONT, 18, "bold")).pack(anchor="w", padx=20, pady=(16, 8))

        tk.Label(self, text="Clica num artista para ver info e top músicas",
                 bg=BG, fg=GRAY, font=(FONT, 10)).pack(anchor="w", padx=20, pady=(0, 6))

        # Frame para botões de prévia (aparece acima dos cards)
        self.artist_buttons_frame = tk.Frame(self, bg=BG)
        self.artist_buttons_frame.pack(fill="x", padx=20, pady=(0, 6))

        # Canvas scrollável para os cards
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True, padx=20, pady=4)

        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        sb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.artistas_frame = tk.Frame(canvas, bg=BG)
        cwin = canvas.create_window((0, 0), window=self.artistas_frame, anchor="nw")
        self.artistas_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
            lambda e: canvas.itemconfig(cwin, width=e.width))

        artistas = [
            {"nome": "Kanye West",         "query": "Kanye West",       "emoji": "🌊"},
            {"nome": "Tyler, The Creator", "query": "Tyler The Creator","emoji": "🐝"},
            {"nome": "Kendrick Lamar",     "query": "Kendrick Lamar",   "emoji": "🦅"},
            {"nome": "Childish Gambino",   "query": "Childish Gambino", "emoji": "🎭"},
            {"nome": "Drake",              "query": "Drake",            "emoji": "🦉"},
            {"nome": "J. Cole",            "query": "J Cole",           "emoji": "📖"},
            {"nome": "Travis Scott",       "query": "Travis Scott",     "emoji": "🎢"},
            {"nome": "Frank Ocean",        "query": "Frank Ocean",      "emoji": "🌊"},
            {"nome": "SZA",               "query": "SZA",              "emoji": "🌸"},
            {"nome": "The Weeknd",         "query": "The Weeknd",       "emoji": "🌙"},
            {"nome": "21 Savage",          "query": "21 Savage",        "emoji": "🔱"},
            {"nome": "Playboi Carti",      "query": "Playboi Carti",    "emoji": "👹"},
        ]

        COLS = 4
        for i, artista in enumerate(artistas):
            r, c = divmod(i, COLS)
            card = tk.Frame(self.artistas_frame, bg=CARD, bd=0,
                            highlightbackground=GREEN, highlightthickness=1)
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")

            tk.Label(card, text=artista["emoji"], bg=CARD, fg=GREEN,
                     font=(FONT, 22)).pack(pady=(12, 2))
            tk.Label(card, text=artista["nome"], bg=CARD, fg=WHITE,
                     font=(FONT, 10, "bold"), wraplength=130).pack(pady=(0, 4), padx=6)

            _make_btn(card, "🔍 Info",
                      lambda q=artista["query"]: self._pesquisar_artista(q)).pack(pady=2, padx=8, fill="x")
            _make_btn(card, "▶ 5 Músicas",
                      lambda q=artista["query"]: self._ver_5_musicas(q)).pack(pady=2, padx=8, fill="x")
            _make_btn(card, "📋 Playlists",
                      lambda q=artista["query"], n=artista["nome"]: self._ver_playlists(q, n)).pack(pady=(2, 10), padx=8, fill="x")

        for c in range(COLS):
            self.artistas_frame.columnconfigure(c, weight=1)

    def _pesquisar_artista(self, query):
        self.output.mostrar(f"🔍 A pesquisar por '{query}'...")
        self.update()

        def buscar():
            code, resultado = sp_pesquisar_artistas(query, 1)
            self.after(0, lambda: self._mostrar_artista(code, resultado, query))

        threading.Thread(target=buscar, daemon=True).start()

    def _mostrar_artista(self, code, resultado, query):
        if code == 200 and resultado:
            a = resultado[0]
            seguidores = f"{a['seguidores']:,}" if a.get('seguidores') else "A carregar..."
            txt = f"🎤 {a['nome'].upper()}\n"
            txt += "═" * 50 + "\n\n"
            txt += f"👥 Seguidores: {seguidores}\n"
            if a.get('generos'):
                txt += f"🏷️ Géneros: {', '.join(a['generos'][:3])}\n"
            txt += f"🔗 {a['url']}\n\n"
            txt += "💡 Clica em '▶ 5 Músicas' para ouvir as top músicas!"
            self.output.mostrar(txt)

            # Se seguidores = 0, buscar o valor real
            if not a.get('seguidores'):
                self._buscar_seguidores_reais(a['id'], a['nome'])
        else:
            self.output.mostrar(f"[{code}] {resultado}")

    def _buscar_seguidores_reais(self, artista_id, nome):
        def buscar():
            try:
                import spotify_online as sp_mod
                code, token = sp_mod._obter_token()
                if code == 200:
                    import requests as req
                    r = req.get(f"https://api.spotify.com/v1/artists/{artista_id}",
                                headers={"Authorization": f"Bearer {token}"}, timeout=8)
                    if r.status_code == 200:
                        total = r.json().get("followers", {}).get("total", 0)
                        seg_txt = f"{total:,}" if total else "N/D"
                        atual = self.output._texto.get("1.0", "end")
                        novo = atual.replace("A carregar...", seg_txt)
                        self.after(0, lambda: self.output.mostrar(novo.rstrip("\n")))
            except Exception:
                pass
        threading.Thread(target=buscar, daemon=True).start()

    def _ver_5_musicas(self, query):
        self.output.mostrar(f"🎵 A carregar músicas de '{query}'...")
        self.update()

        def buscar():
            code, artista = sp_pesquisar_artistas(query, 1)
            if code == 200 and artista:
                a = artista[0]
                code2, musicas = get_musicas_artista(a['id'], 5)
                self.after(0, lambda: self._mostrar_5_musicas(code2, musicas, query))
            else:
                self.after(0, lambda: self.output.mostrar(f"[{code}] Artista não encontrado"))

        threading.Thread(target=buscar, daemon=True).start()

    def _mostrar_5_musicas(self, code, musicas, artista_nome):
        if code == 200:
            txt = f"TOP 5 MUSICAS -- {artista_nome.upper()}\n"
            txt += "=" * 60 + "\n\n"
            for i, m in enumerate(musicas[:5], 1):
                mins = m['duracao_ms'] // 60000
                secs = (m['duracao_ms'] // 1000) % 60
                txt += f"  {i}. {m['titulo']}\n"
                txt += f"     {m['album']}  {mins}:{secs:02d}"
                txt += "  preview ok\n" if m.get('preview_url') else "  (abre no Spotify)\n"
                txt += "\n"
            self.output.mostrar(txt)

            for widget in self.artist_buttons_frame.winfo_children():
                widget.destroy()
            tk.Label(self.artist_buttons_frame,
                     text=f"▶ Reproduzir — {artista_nome}",
                     bg=BG, fg=GREEN, font=(FONT, 10, "bold")).pack(anchor="w", pady=(4, 2))
            btn_row = tk.Frame(self.artist_buttons_frame, bg=BG)
            btn_row.pack(fill="x")
            for m in musicas[:5]:
                titulo_enc = m['titulo'].replace(' ', '+')
                artista_enc = artista_nome.replace(' ', '+')
                url_fallback = f"https://open.spotify.com/search/{artista_enc}+{titulo_enc}/tracks"
                url = m.get('preview_url') or url_fallback
                _make_btn(btn_row, f"▶ {m['titulo'][:24]}",
                          lambda u=url, t=m['titulo'], a=artista_nome: self._reproduzir(u, t, a)
                          ).pack(side="left", padx=3, pady=2)
        else:
            self.output.mostrar(f"[{code}] {musicas}")

    def _reproduzir(self, url, titulo, artista):
        app = self.winfo_toplevel()
        if hasattr(app, 'mini_player'):
            app.mini_player.set_music(titulo, artista, url, url)
        webbrowser.open(url)

    def _ver_playlists(self, query, nome):
        """Mostra 3 playlists temáticas com botão reproduzir playlist"""
        for widget in self.artist_buttons_frame.winfo_children():
            widget.destroy()

        playlists = [
            {"nome": f"🔥 {nome} – Top Hits",        "q": f"{query} top hits"},
            {"nome": f"🎧 {nome} – Best Of",          "q": f"{query} best songs"},
            {"nome": f"🌙 {nome} – Álbuns Essenciais","q": f"{query} essential albums"},
        ]

        txt = f"📋 PLAYLISTS — {nome.upper()}\n" + "═" * 55 + "\n\n"
        for i, pl in enumerate(playlists, 1):
            txt += f"  {i}. {pl['nome']}\n"
        txt += "\n▶ Clica em 'Reproduzir Playlist' para abrir no Spotify."
        self.output.mostrar(txt)

        tk.Label(self.artist_buttons_frame,
                 text=f"📋 Playlists — {nome}",
                 bg=BG, fg=GREEN, font=(FONT, 10, "bold")).pack(anchor="w", pady=(4, 2))
        for pl in playlists:
            row = tk.Frame(self.artist_buttons_frame, bg=BG)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=pl['nome'], bg=BG, fg=WHITE,
                     font=(FONT, 9), width=38, anchor="w").pack(side="left")
            q_enc = pl['q'].replace(' ', '+')
            url = f"https://open.spotify.com/search/{q_enc}/playlists"
            _make_btn(row, "▶ Reproduzir Playlist",
                      lambda u=url: webbrowser.open(u)).pack(side="left", padx=4)

    def _tocar_previa(self, preview_url):
        if not preview_url:
            messagebox.showinfo("Info", "Prévia não disponível para esta música", parent=self)
            return
        webbrowser.open(preview_url)


# ==============================
# HELPERS
# ==============================

def _make_btn(parent, text, command):
    btn = tk.Button(
        parent, text=text, command=command,
        bg=HOVER, fg=WHITE, font=(FONT, 9, "bold"),
        relief="flat", cursor="hand2", padx=10, pady=6,
        activebackground=GREEN, activeforeground=BLACK_TEXT
    )

    def on_enter(e): btn.config(bg=GREEN, fg=BLACK_TEXT)
    def on_leave(e): btn.config(bg=HOVER, fg=WHITE)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def _pedir_id(parent, label_txt, callback):
    win = tk.Toplevel()
    win.title(label_txt)
    win.configure(bg=BG)
    win.resizable(False, False)
    win.grab_set()

    tk.Label(win, text=label_txt, bg=BG, fg=GRAY,
             font=(FONT, 11)).pack(pady=(16, 6), padx=20)
    e = tk.Entry(win, bg=INPUT_BG, fg=WHITE, insertbackground=WHITE,
                 font=(FONT, 11), width=24, relief="flat", bd=6)
    e.pack(padx=20, pady=6)

    def ok():
        v = e.get().strip()
        win.destroy()
        if v:
            callback(v)

    tk.Button(win, text="OK", bg=GREEN, fg=BLACK_TEXT,
              font=(FONT, 10, "bold"), relief="flat",
              padx=16, pady=6, cursor="hand2", command=ok).pack(pady=(6, 16))
    e.bind("<Return>", lambda ev: ok())


def _handle(code, obj, win, output, fmt_ok):
    if code in (200, 201):
        win.destroy()
        output.mostrar(fmt_ok(obj))
    else:
        messagebox.showerror("Erro", f"[{code}] {obj}", parent=win)


# ==============================
# PLAYLISTS PRE-DEFINIDAS (CRUD)
# ==============================

_ID_PL_TOP    = "pl-spotify-tophits-001"
_ID_PL_BESTOF = "pl-spotify-bestof-002"
_ID_PL_ESSENC = "pl-spotify-essenc-003"
_ID_USER_SYS  = "usr-sistema-spotify-0"


def _inicializar_playlists_spotify():
    """
    Cria no playlists.json as 3 playlists pre-definidas do Spotify Manager.
    Usa persistencia direta (sem validacoes de URL do CRUD normal — dados internos).
    Tambem garante que o utilizador 'sistema' existe no utilizadores.json.
    """
    from utilizadores import carregar_utilizadores, guardar_utilizadores
    from Playlist import carregar_playlists, guardar_playlists
    from datetime import date

    # utilizador sistema
    utilizadores = carregar_utilizadores()
    if _ID_USER_SYS not in utilizadores:
        utilizadores[_ID_USER_SYS] = {
            "id_utilizador":      _ID_USER_SYS,
            "nome_exibicao":      "Spotify Manager",
            "nome_utilizador":    "sistema",
            "foto_perfil":        "https://open.spotify.com",
            "pais":               "PT",
            "data_nascimento":    "01/01/2000",
            "generos_preferidos": ["todos"],
            "data_registro":      date.today().strftime("%d/%m/%Y"),
            "estado_conta":       "ativo",
            "seguidores":         [],
            "seguidos":           [],
            "playlists_publicas": [_ID_PL_TOP, _ID_PL_BESTOF, _ID_PL_ESSENC],
            "historico_consumo":  [],
        }
        guardar_utilizadores(utilizadores)

    playlists = carregar_playlists()
    hoje = date.today().strftime("%d/%m/%Y")

    definicoes = [
        {
            "id":    _ID_PL_TOP,
            "nome":  "Spotify Top Hits",
            "desc":  "As musicas mais ouvidas do momento no Spotify",
            "query": "top hits 2024",
        },
        {
            "id":    _ID_PL_BESTOF,
            "nome":  "Spotify Best Of",
            "desc":  "As melhores musicas de todos os tempos",
            "query": "best songs all time",
        },
        {
            "id":    _ID_PL_ESSENC,
            "nome":  "Spotify Albuns Essenciais",
            "desc":  "Musicas dos albuns mais iconicos da historia",
            "query": "essential albums classics",
        },
    ]

    alterado = False
    for d in definicoes:
        if d["id"] not in playlists:
            playlists[d["id"]] = {
                "id_playlist":         d["id"],
                "nome_playlist":       d["nome"],
                "id_utilizador":       _ID_USER_SYS,
                "privacidade":         "publica",
                "lista_ids":           [],
                "descricao":           d["desc"],
                "capa_playlist":       "https://open.spotify.com",
                "data_criacao":        hoje,
                "seguidores_playlist": [],
                "ordem_musicas":       [],
                "flag_remocao":        False,
                "spotify_query":       d["query"],
            }
            alterado = True

    if alterado:
        guardar_playlists(playlists)


# ==============================
# APP PRINCIPAL
# ==============================

class SpotifyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spotify Manager")
        self.configure(bg=BG)
        self.geometry("1200x720")
        self.minsize(1000, 600)
        _inicializar_playlists_spotify()
        self._build()

    def set_status(self, msg):
        if hasattr(self, 'status_bar'):
            self.status_bar.config(text=msg)
            self.after(3000, lambda: self.status_bar.config(text="✅ Pronto"))

    def _build(self):
        header = tk.Frame(self, bg=SIDEBAR, height=60)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(header, text="  ♫  Spotify Manager",
                 bg=SIDEBAR, fg=GREEN,
                 font=(FONT, 16, "bold")).pack(side="left", padx=16)

        tk.Label(header, text="Abel Chongolola | GPSI 10A | N 01",
                 bg=SIDEBAR, fg=GRAY,
                 font=(FONT, 9)).pack(side="right", padx=16)

        self.status_bar = tk.Label(
            self, text="✅ Pronto", bg=SIDEBAR, fg=GRAY,
            font=(FONT, 9), anchor="w", padx=10
        )
        self.status_bar.pack(fill="x", side="bottom")

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        sidebar = tk.Frame(body, bg=SIDEBAR, width=180)
        sidebar.pack(fill="y", side="left")
        sidebar.pack_propagate(False)

        content = tk.Frame(body, bg=BG)
        content.pack(fill="both", expand=True, side="left")

        output = PainelOutput(content)
        output.pack(fill="both", expand=True, side="bottom", padx=12, pady=(0, 12))
        output.mostrar(
            "🎵 Bem-vindo ao Spotify Manager!\n\nSeleciona uma secção e uma ação para começar.\n\nDicas:\n• F1 - Utilizadores\n• F2 - Artistas\n• F3 - Músicas\n• F4 - Playlists\n• F5 - Spotify Online\n• F6 - Artistas Populares\n• Ctrl+L - Limpar output")

        self._tab_frame = tk.Frame(content, bg=BG)
        self._tab_frame.pack(fill="x", side="top")

        self._tabs = {}
        tab_classes = [
            ("👤 Utilizadores", TabUtilizadores),
            ("🎤 Artistas", TabArtistas),
            ("🎵 Musicas", TabMusicas),
            ("📀 Playlists", TabPlaylists),
            ("🌐 Spotify Online", TabSpotifyOnline),
            ("⭐ Artistas Populares", TabArtistasPopulares),
        ]
        for nome, cls in tab_classes:
            t = cls(self._tab_frame, output)
            self._tabs[nome] = t

        self._active_tab = None
        for nome in self._tabs:
            b = tk.Button(
                sidebar, text=nome,
                bg=SIDEBAR, fg=GRAY,
                font=(FONT, 11), relief="flat",
                cursor="hand2", anchor="w",
                padx=16, pady=12,
                command=lambda n=nome: self._show_tab(n)
            )
            b.pack(fill="x")
            self._tabs[nome]._sidebar_btn = b

        self.mini_player = MiniPlayer(self)

        self.bind("<F1>", lambda e: self._show_tab("👤 Utilizadores"))
        self.bind("<F2>", lambda e: self._show_tab("🎤 Artistas"))
        self.bind("<F3>", lambda e: self._show_tab("🎵 Musicas"))
        self.bind("<F4>", lambda e: self._show_tab("📀 Playlists"))
        self.bind("<F5>", lambda e: self._show_tab("🌐 Spotify Online"))
        self.bind("<F6>", lambda e: self._show_tab("⭐ Artistas Populares"))
        self.bind("<Control-l>", lambda e: output.limpar())
        self.bind("<Control-L>", lambda e: output.limpar())

        self._show_tab("👤 Utilizadores")

    def _show_tab(self, nome):
        if self._active_tab:
            self._tabs[self._active_tab].pack_forget()
            self._tabs[self._active_tab]._sidebar_btn.config(bg=SIDEBAR, fg=GRAY)

        self._active_tab = nome
        self._tabs[nome].pack(fill="x", side="top")
        self._tabs[nome]._sidebar_btn.config(bg=HOVER, fg=GREEN)
        self.set_status(f"📁 Aba {nome} selecionada")


if __name__ == "__main__":
    app = SpotifyApp()
    app.mainloop()
