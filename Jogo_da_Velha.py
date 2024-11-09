import pygame
import sys

# Inicializar o Pygame
pygame.init()

# Configurações de tela
TELA_LARGURA = 600
TELA_ALTURA = 600
COR_FUNDO = (50, 50, 50)
COR_LINHA = (230, 230, 230)
COR_X = (255, 100, 100)
COR_O = (100, 200, 255)
COR_VITORIA = (0, 255, 100)
COR_DESTAQUE = (0, 0, 0)
LINHA_LARGURA = 15

# Configurações de fonte
FONTE = pygame.font.SysFont('arial', 80, bold=True)
FONTE_VITORIA = pygame.font.SysFont('arial', 60, bold=True)

# Classe base para jogadores
class Jogador:
    def __init__(self, simbolo, cor):
        self.simbolo = simbolo
        self.cor = cor
    
    def get_simbolo(self):
        return self.simbolo

    def get_cor(self):
        return self.cor

# Jogador X e Jogador O herdam da classe Jogador
class JogadorX(Jogador):
    def __init__(self):
        super().__init__('X', COR_X)

class JogadorO(Jogador):
    def __init__(self):
        super().__init__('O', COR_O)

# Classe Tabuleiro
class Tabuleiro:
    def __init__(self):
        self.tabuleiro = [[None] * 3 for _ in range(3)]
    
    def get_tabuleiro(self):
        return self.tabuleiro

    def set_posicao(self, linha, coluna, simbolo):
        self.tabuleiro[linha][coluna] = simbolo
    
    def verificar_vitoria(self):
        # Verificar linhas, colunas e diagonais
        for row in range(3):
            if self.tabuleiro[row][0] == self.tabuleiro[row][1] == self.tabuleiro[row][2] and self.tabuleiro[row][0] is not None:
                return self.tabuleiro[row][0], [(row, 0), (row, 1), (row, 2)]

        for col in range(3):
            if self.tabuleiro[0][col] == self.tabuleiro[1][col] == self.tabuleiro[2][col] and self.tabuleiro[0][col] is not None:
                return self.tabuleiro[0][col], [(0, col), (1, col), (2, col)]

        if self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] and self.tabuleiro[0][0] is not None:
            return self.tabuleiro[0][0], [(0, 0), (1, 1), (2, 2)]

        if self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0] and self.tabuleiro[0][2] is not None:
            return self.tabuleiro[0][2], [(0, 2), (1, 1), (2, 0)]

        # Verificar empate
        if all(all(celula is not None for celula in linha) for linha in self.tabuleiro):
            return "Empate", []

        return None, []

# Classe JogoDaVelha
class JogoDaVelha:
    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.jogador_atual = JogadorX()
        self.vencedor = None
        self.jogo_terminado = False
        self.mostrar_vencedor_tempo = 0
    
    def alternar_jogador(self):
        if isinstance(self.jogador_atual, JogadorX):
            self.jogador_atual = JogadorO()
        else:
            self.jogador_atual = JogadorX()

    def jogar(self, linha, coluna):
        if self.tabuleiro.get_tabuleiro()[linha][coluna] is None and not self.jogo_terminado:
            self.tabuleiro.set_posicao(linha, coluna, self.jogador_atual.get_simbolo())
            vencedor, coordenadas_vitoria = self.tabuleiro.verificar_vitoria()
            if vencedor:
                self.vencedor = vencedor
                self.jogo_terminado = True
                self.mostrar_vencedor_tempo = pygame.time.get_ticks()
            else:
                self.alternar_jogador()

    def reiniciar(self):
        self.tabuleiro = Tabuleiro()
        self.jogador_atual = JogadorX()
        self.vencedor = None
        self.jogo_terminado = False

# Funções para desenhar
def desenhar_tabuleiro():
    tela.fill(COR_FUNDO)
    for i in range(1, 3):
        pygame.draw.line(tela, COR_LINHA, (0, 200 * i), (TELA_LARGURA, 200 * i), LINHA_LARGURA)
        pygame.draw.line(tela, COR_LINHA, (200 * i, 0), (200 * i, TELA_ALTURA), LINHA_LARGURA)

def desenhar_pecas(jogo):
    for row in range(3):
        for col in range(3):
            simbolo = jogo.tabuleiro.get_tabuleiro()[row][col]
            if simbolo == 'X':
                desenhar_x(col * 200, row * 200)
            elif simbolo == 'O':
                desenhar_o(col * 200, row * 200)

def desenhar_x(x, y):
    offset = 50
    pygame.draw.line(tela, COR_X, (x + offset, y + offset), (x + 200 - offset, y + 200 - offset), LINHA_LARGURA)
    pygame.draw.line(tela, COR_X, (x + offset, y + 200 - offset), (x + 200 - offset, y + offset), LINHA_LARGURA)

def desenhar_o(x, y):
    pygame.draw.circle(tela, COR_O, (x + 100, y + 100), 70, LINHA_LARGURA)

def mostrar_vencedor(vencedor):
    destaque = pygame.Surface((TELA_LARGURA, TELA_ALTURA))
    destaque.set_alpha(200)
    destaque.fill(COR_DESTAQUE)
    tela.blit(destaque, (0, 0))
    texto = FONTE_VITORIA.render(f"{vencedor} Venceu!" if vencedor != "Empate" else "Empate!", True, COR_LINHA)
    tela.blit(texto, (TELA_LARGURA // 2 - texto.get_width() // 2, TELA_ALTURA // 2 - texto.get_height() // 2))

# Configurar a tela
tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
pygame.display.set_caption("Jogo da Velha Estilizado")

# Loop principal do jogo
jogo = JogoDaVelha()
rodando = True
while rodando:
    desenhar_tabuleiro()
    desenhar_pecas(jogo)

    if jogo.jogo_terminado:
        mostrar_vencedor(jogo.vencedor)
        if pygame.time.get_ticks() - jogo.mostrar_vencedor_tempo > 3000:  # Desaparece após 3 segundos
            jogo.reiniciar()

    pygame.display.update()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN and not jogo.jogo_terminado:
            x, y = evento.pos
            linha = y // 200
            coluna = x // 200
            jogo.jogar(linha, coluna)

pygame.quit()
sys.exit()
