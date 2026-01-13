import pygame
import sys
import random
import math
from random import randint, choice
from pygame.locals import *

# ainda nao ta bem as colisoes entre as bolas todas
# acabar class  def Modificar_bolas_com_toques():
#Modificar_bolas_com_toques() ❌ (INCOMPLETA) 

# Cores terminal
fundo_ciano = '\033[46m'
RED = "\033[1;31m"
FIM = "\033[0m"
GREN = '\033[32m'
YElOW = '\033[33m'
roxo = '\033[35m'
azul = '\033[34m'

# Cores 
BLACK = (0, 0, 0)
BLUE  = (0, 0, 255)
WHITE = (255, 255, 255)
COLORS = [
    (255, 0, 0),   # vermelho
    (0, 255, 0),   # verde
    (0, 0, 255),   # azul
    (255, 255, 0), # amarelo
    (255, 0, 255)  # magenta
]

pygame.init()

#largura da janela
surface_width  = 800
surface_height = 500


surface = pygame.display.set_mode((surface_width, surface_height))
pygame.display.set_caption("Jogo da Bola")


clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class Bola:
    id_counter = 0  # contador para atribuir ids as bolas 
    total_colisoes = 0  # Armazenar n de colisões
    colisoes_de_Bola_Normal_por_id = {}  #Armazenar colisões de bolas normais por id
    

    def __init__(self, x, y, cor, raio, move_x, move_y):
        self.id = Bola.id_counter
        Bola.id_counter += 1  

        self.x = x
        self.y = y
        self.cor = cor
        self.raio = raio
        self.move_x = move_x
        self.move_y = move_y

    def desenha(self, surface):
        pygame.draw.circle(surface, self.cor, (self.x, self.y), self.raio)

        # da o id da bola
        if self.id != "B_utilizador":#se o nome do id nao for o nome da bola do utilizador mostra o id porque eu nao queria que aparecesse
            texto = font.render(str(self.id), True, WHITE)
            text_rect = texto.get_rect(center=(self.x, self.y))  
            surface.blit(texto, text_rect) 

    def move(self, surface):
        
        self.x += self.move_x
        self.y += self.move_y
        # Chama a função para verificar se a bola toca nas bordas e se repuxa
        self.verifica_limites(surface)

    #---------------------------Colisão das bordas de jogo-------------------------
    def verifica_limites(self, surface):
        largura = surface.get_width()
        altura = surface.get_height()

        # Ve bordas laterais
        if self.x - self.raio <= 0:
            self.x = self.raio  # faz conque nao saia a bola pelo lado esquerdo
            self.move_x *= -1  # inverte horizontal
        elif self.x + self.raio >= largura:
            self.x = largura - self.raio  # faz conque nao saia a bola pelo lado direita
            self.move_x *= -1  

        # VE bordas inferiores e superiores
        if self.y - self.raio <= 0:
            self.y = self.raio  ## faz conque nao saia a bola pelo lado de cima
            self.move_y *= -1  #  inverte verticalmente
        elif self.y + self.raio >= altura:
            self.y = altura - self.raio  # faz conque nao saia a bola pelo lado inferior
            self.move_y *= -1  # Inverte verticalmente
    #--------------------------------------------------------------
    #--Verificar bolas para nao crir umas em cima das outras--#
    def nao_criar_bolas_em_cima_de_outras(raio, bolas):
        """
            Vai gar cordenadas(x,y) para uma bola nao ser sobreposta em outra
        """
        while True:
            x = random.randint(raio, surface_width - raio)
            y = random.randint(raio, surface_height - raio)
            sobrepoe = False

            for bola in bolas:
                # Formula para calcular a distanci entre os centros da nova bola e da bola existente 
                distancia = math.sqrt((x - bola.x) ** 2 + (y - bola.y) ** 2)
                if distancia <= (raio + bola.raio):
                    sobrepoe = True
                    break  

            if not sobrepoe:
                return x, y  # retorna as coordenadas se não houver sobreposição para criar a nova bola
    
    def Modificar_bolas_com_toques(bolas):
        """
            Modifica bolas normais com base nas colisões:
            - Divide em 2 se tiverem ≥ 20 colisões com outras bolas normais.
            - Desaparecem se tiverem ≥ 10 colisões com a bola do utilizador.
        """
        novas_bolas = []  # Lista para armazenar novas bolas criadas ao dividir
        for bola in bolas[:]:  # Iterar sobre uma copia da lista para evitar problemas ao modificar a lista original
            if isinstance(bola, BolaNormal):
                # verifica colisões com outras bolas normais
                if bola.colisoes >= 20:
                    # gera posiçoes para as novas bolas usando a função nao_criar_bolas_em_cima_de_outras
                    x1, y1 = Bola.nao_criar_bolas_em_cima_de_outras(bola.raio, bolas)
                    x2, y2 = Bola.nao_criar_bolas_em_cima_de_outras(bola.raio, bolas)
    
                    # cria as duas bolas agr com cordenadas certas em direções opostas
                    nova_bola_1 = BolaNormal(
                        x1, y1, bola.cor, bola.raio, -bola.move_x, bola.move_y
                    )
                    nova_bola_2 = BolaNormal(
                        x2, y2, bola.cor, bola.raio, bola.move_x, -bola.move_y
                    )
                    # .extend -> adiciona as novas bolas a lista de bolas
                    novas_bolas.extend([nova_bola_1, nova_bola_2])
                    bolas.remove(bola)  # Remove a bola original
    
                    #debug das bolas
                    print(roxo)
                    print(f"🔵 Bola {bola.id} dividida!")
                    print(f"Nova Bola 1 -> ID: {nova_bola_1.id}, Posição: ({nova_bola_1.x}, {nova_bola_1.y}), Direção: ({nova_bola_1.move_x}, {nova_bola_1.move_y})")
                    print(f"Nova Bola 2 -> ID: {nova_bola_2.id}, Posição: ({nova_bola_2.x}, {nova_bola_2.y}), Direção: ({nova_bola_2.move_x}, {nova_bola_2.move_y})")
                    print(FIM)

                # Verifica colisões com a bola do utilizador
                elif isinstance(bola, BolaNormal) and Bola.colisoes_de_Bola_Normal_por_id.get(bola.id, 0) >= 10:
                    # verifica se ha colisao que envolva a bola do utilizador
                    if "B_utilizador" in Bola.colisoes_de_Bola_Normal_por_id:
                        print(f"❌ Bola {bola.id} removida apos 10 colisões com a bola do utilizador.")
                        bolas.remove(bola)#remove bola 

        
        bolas.extend(novas_bolas)  # Adiciona as novas bolas à lista de bolas existentes
        return bolas
#--------------------------------------------------------------
# Subclasse BolaNormal
class BolaNormal(Bola):
    def __init__(self, x, y, cor, raio, move_x, move_y):
        super().__init__(x, y, cor, raio, move_x, move_y)
        self.colisoes = 0  # Icontador de colisoes
        
    def colidir_com(self, outra):
        """
            Verifica se a bola normal colidiu com outra bola e conta as colisões.
        """
        distancia = math.sqrt((self.x - outra.x) ** 2 + (self.y - outra.y) ** 2)
        if distancia <= (self.raio + outra.raio):
            # incremeta o contador de colisoes
            Bola.total_colisoes += 1
            
            # ve se a chave  ja existe  no dicionario  e inicializa com 0 se nao existir
            if self.id not in Bola.colisoes_de_Bola_Normal_por_id:
                Bola.colisoes_de_Bola_Normal_por_id[self.id] = 0
            if outra.id not in Bola.colisoes_de_Bola_Normal_por_id:
                Bola.colisoes_de_Bola_Normal_por_id[outra.id] = 0
        
            # incremet o contador de colisoes individuais de cada bola envolvida na colisao
            Bola.colisoes_de_Bola_Normal_por_id[self.id] += 1
            Bola.colisoes_de_Bola_Normal_por_id[outra.id] += 1
            
            # atualiza o contador de colisoes de cada bola
            self.colisoes += 1
            outra.colisoes += 1
    
            # print
            print(RED)
            print(f"Bola {self.id} colisões: {self.colisoes}")
            print(f"Bola {outra.id} colisões: {outra.colisoes}")
            print(FIM)
            
            return True
        return False

    def tratar_colisao(self, outra):
        """
        Trocar as velocidades da bola CADA VEZ QUE TEM UMA COLISÃO
        """
        # se fgor a bola do utilizador nao vai mudar a sua direção quando colide com as normais 
        if self.id == "B_utilizador":
            self.move_x = outra.move_x
            self.move_y = outra.move_y
        else: #para bolas normais 
            self.move_x, outra.move_x = outra.move_x, self.move_x
            self.move_y, outra.move_y = outra.move_y, self.move_y

    def atualizar(self, surface, todas_bolas):
        """
        Atualiza a bola:
         - Move a bola
         - Verifica colisões com outras bolas
        """
        self.x += self.move_x
        self.y += self.move_y
        self.verifica_limites(surface)  

        # veerifica colisao com outras bolas
        for outra in todas_bolas:
            if outra is not self:  # validação para evitar colisão com ela mesma
                if isinstance(outra,(BolaUtilizador, BolaNormal)):  
                    if self.colidir_com(outra):# o -> 'and self.colidir_com(outra)' verifica se esta a colidir
                        self.x -= self.move_x
                        self.y -= self.move_y  
                        self.tratar_colisao(outra)
                        #self.colidir_bNormal_com_bola_utilizador(outra)
 

class BolaUtilizador(Bola):
    def __init__(self, x, y, cor, raio, velocidade, move_x, move_y):
        super().__init__(x, y, cor, raio, move_x, move_y)  
        self.velocidade = velocidade
        self.id = "B_utilizador"  # dar id unico a bola do utilizador
        self.colisoes = 0

    def Setas_cotrolo_do_utilizador(self, event):
        if event.type == KEYDOWN:  # Define a direção ao pressionar uma tecla
            if event.key == K_LEFT:
                self.move_x = -self.velocidade
                self.move_y = 0
            elif event.key == K_RIGHT:
                self.move_x = self.velocidade
                self.move_y = 0
            elif event.key == K_UP:
                self.move_x = 0
                self.move_y = -self.velocidade
            elif event.key == K_DOWN:
                self.move_x = 0
                self.move_y = self.velocidade

            ##print(RED)
            ##print(f"Jogador move_x: {self.move_x}, move_y: {self.move_y}")  # Debug
            ##print(FIM)
    
    def atualizar(self, surface, todas_bolas):
        """
            Atualiza a posição da bola e verifica colisões.
        """
        self.x += self.move_x
        self.y += self.move_y
        self.verifica_limites(surface)

        for outra in todas_bolas:
            if not isinstance(outra, Bola_Fantasma):  # Ignora bolas fantasmas
                distancia = math.sqrt((self.x - outra.x) ** 2 + (self.y - outra.y) ** 2)#formula para calcular a distancia entre o centro das bolas 
                
                if outra is not self and distancia <= (self.raio + outra.raio):  # Verifica se ouve colisao ou seja se for negativo o mnumero da distancia e porque ja se encontra a colidir
                    print(RED)
                    print(f" Colisão detectada entre {self.id} e {outra.id}")
                    print(FIM)  

                    self.x -= self.move_x
                    self.y -= self.move_y
                    
                    self.move_x = outra.move_x
                    self.move_y = outra.move_y

                    if isinstance(outra, BolaNormal):
                        print(RED)
                        print(f"Debug: Colisão com BolaNormal {outra.id}")  # debug temporário
                        self.raio = max(0, self.raio - 3)  # Reduz o raio da bola do utilizador
                        print(f"Debug: Novo raio da bola do utilizador: {self.raio}")
                        print(FIM)

                        # Verifica se o raio da bola do utilizador chegou a 0 se si perdeu sai do jogo 
                        if self.raio <= 0:
                            print("⚠️ A bola do utilizador perdeu o jogo! Raio chegou a 0.")
                            # pygame.quit()
                            # sys.exit()


class Bola_Fantasma(Bola):
    id_fantasma_counter = 0
    def __init__(self, x, y, cor, raio, move_x, move_y):
        
        super().__init__(x, y, cor, raio, move_x, move_y)
        self.id = "B_Fantasma"
        # id especifico para bolas fantasmas: "F" + numero da bola
        self.id = f"F{Bola_Fantasma.id_fantasma_counter}"
        # Incrementa o contador de bolas fantasmas
        Bola_Fantasma.id_fantasma_counter += 1
        self.bolas_colididas = set()  # Conjunto para armazenar IDs de bolas colididas
        self.colisoes = 0 # Adiciona o atributo colisoes para compatibilidade
        # Lista de nomes de arquivos de imagens que vao ser usadas para as bolas fantasmas
        self.image_B_fantasma_files = [
            "ghost_ball.png",#  -> Imagem padrão
            "ghost_ball_amarelo.png",
            "ghost_ball_azul.png",
            "ghost_ball_vermelho.png",
            "ghost_ball_verde.png",
            "ghost_ball_roxo.png"
        ]
        # Dicionario para armazenar as imagens carregadas
        self.images = {}

        # Carrega todas as imagens
        for img_file in self.image_B_fantasma_files:
            try:
                img = pygame.image.load(img_file).convert_alpha()
                img = pygame.transform.scale(img, (raio*2, raio*2))
                self.images[img_file] = img
                print(GREN)
                print(f"Imagem {img_file} carregada com sucesso para bola {self.id}") # debug para verificar se as imagens foram carregadas corretamente
                print(FIM)
            except Exception as e:
                print(RED)
                print(f"Erro ao carregar imagem {img_file}: {e}")
                print(FIM)
        print("\n")
        self.current_image_key = list(self.images.keys())[0]
    
    def desenha(self, surface):
        """
            Sobrescreve o método desenha da classe base para usar a imagem
            Calcula a posição para centralizar a imagem no ponto (x, y)
            Calcula a posição para centralizar a imagem
        """

        pos_x = int(self.x - self.raio)
        pos_y = int(self.y - self.raio)
        
        # Redimensiona a imagem atual para o tamanho atual da bola
        current_img = self.images[self.current_image_key]
        current_img = pygame.transform.scale(current_img, (int(self.raio*2), int(self.raio*2)))
        surface.blit(current_img, (pos_x, pos_y))
        # Desenha o ID da bola sobre a imagem
        if self.id == "B_Fantasma":
            texto = font.render(str(self.id), True, BLACK)
            text_rect = texto.get_rect(center=(self.x, self.y))
            surface.blit(texto, text_rect)

    def criar_bola_fantasma_30s(bolas):
        """
            Cria uma nova bola fantasma dew 30 em 30 segundos
            da return ao valores para criar a nova bola
            valores que vao para o main do jogo
        """
        raio = random.randint(10, 20)
        x, y = Bola.nao_criar_bolas_em_cima_de_outras(raio, bolas)
        cor =  (255, 255, 255) # Branco para se diferenciar
        move_x = random.choice([-3, -2, -1, 1, 2, 3])
        move_y = random.choice([-3, -2, -1, 1, 2, 3])
        
        return Bola_Fantasma(x, y, cor, raio, move_x, move_y)
    
    def colidir_com_bola_fantasma(self, outra_fantasma,bolas):
        """
            Quando colide com outra bola fantasma, ambas diminuem de tamanho e invertem direçao
        """
    
        distancia = math.sqrt((self.x - outra_fantasma.x) ** 2 + (self.y - outra_fantasma.y) ** 2)#formula
        if distancia <= (self.raio + outra_fantasma.raio):#distancia for negativa colisao esta a acontecer
            # Ambas diminuem de tamanho em 1 pixel a cada colisao entre B_Fantasma e B_Fantasma
            self.raio = max(0, self.raio - 1)
            outra_fantasma.raio = max(0, outra_fantasma.raio - 1)

            # Ambas invertem direção
            self.move_x *= -1
            self.move_y *= -1
            outra_fantasma.move_x *= -1
            outra_fantasma.move_y *= -1

            # Remove bolas com raio zero
            if self.raio <= 0:
                print(RED)
                print(f"Bola fantasma {self.id} foi removida.")
                print(FIM)
                bolas.remove(self)

            if outra_fantasma.raio <= 0:
                print(RED)
                print(f"Bola fantasma {outra_fantasma.id} foi removida.")
                print(FIM)
                bolas.remove(outra_fantasma)

            print(GREN)
            print(f"Bolas fantasmas {self.id} e {outra_fantasma.id} colidiram. Novo raio: {self.raio} e {outra_fantasma.raio}")
            print(FIM)

    def colidir_com_bola_normal(self, bola_normal):
        distancia = math.sqrt((self.x - bola_normal.x) ** 2 + (self.y - bola_normal.y) ** 2)#formula
        if distancia <= (self.raio + bola_normal.raio):#distancia for negativa colisao esta a acontecer
            if bola_normal not in self.bolas_colididas: # Verifica se a bola normal já não foi colidida comfantasma  assim so muda de cor 1 vez a cala colisao
                self.bolas_colididas.add(bola_normal)# como nao esta na lista da add a bola 

                # Troca a imagem
                image_keys = list(self.images.keys())
                current_index = image_keys.index(self.current_image_key)
                next_index = (current_index + 1) % len(image_keys)
                self.current_image_key = image_keys[next_index]

                print(f"Bola fantasma {self.id} mudou de imagem apos colidir com bola normal {bola_normal.id}.")
        else:
            # Remove do set se já não está a colidir
            if bola_normal in self.bolas_colididas:
                self.bolas_colididas.remove(bola_normal)

    def colidir_com_bola_utilizador(self, bola_utilizador):
        """
            Sempre que a bola toca numa bola fantasma, a bola fantasma
	        diminui 5 de raio ( ou menos, se o seu raio for menor que 5 ), e a bola do utilizador aumenta nesse mesmo valor. 
	        A bola do utilizador muda de direção após a colisão, mas a fantasma não.
        """
        distancia = math.sqrt((self.x - bola_utilizador.x) ** 2 + (self.y - bola_utilizador.y) ** 2)#formula
        if distancia <= (self.raio + bola_utilizador.raio):#distancia for negativa colisao esta a acontecer
            if bola_utilizador not in self.bolas_colididas:#e o mesmo caso de cima def colidir_com_bola_normal();
                self.bolas_colididas.add(bola_utilizador)#da add a lista

                # calculça a redução de raio da bola fantasma
                diminuir = min(5, self.raio)
                self.raio -= diminuir
                bola_utilizador.raio += diminuir  # Aumenta o raio da bola do utilizador com o mesmo valor que a B_F perdeu

                # garante que o raio da bola do utilizador não ultrapasse 35
                bola_utilizador.raio = min(bola_utilizador.raio, 35)

                # Muda a direção da bola do utilizador
                #B_utilizador toca e a outra repele
                bola_utilizador.move_x *= -0.5
                bola_utilizador.move_y *= -0.5

                # Debug
                print(f"Bola fantasma {self.id} colidiu com bola do utilizador. Novo raio: {self.raio}")
                print(f"Bola do utilizador agora tem raio {bola_utilizador.raio}.")
        
        else:
            # Remove do conjunto se as bolas não estiverem mais em contato
            if bola_utilizador in self.bolas_colididas:
                self.bolas_colididas.remove(bola_utilizador)
            
    def atualizar(self, surface, bolas=None):
        self.x += self.move_x
        self.y += self.move_y
        self.verifica_limites(surface)

        # Verifica colisões com outras bolas
        if bolas:
            for bola in bolas[:]:   #Iterar sobre uma copia da lista para evitar problemas ao modificar a lista original
                if isinstance(bola, Bola_Fantasma) and bola is not self:
                    self.colidir_com_bola_fantasma(bola, bolas)

                elif isinstance(bola, BolaNormal):
                    self.colidir_com_bola_normal(bola)
                
                elif isinstance(bola, BolaUtilizador):
                    self.colidir_com_bola_utilizador(bola)

def interface_vitoria(surface):
    """
    Exibe a interface de vitória.
    """
    while True:
        surface.fill(BLACK)
        titulo = font.render("WIN! WIN! WIN! WIN! WIN! WIN! WIN! WIN! WIN! WIN!", True, WHITE)
        instrucoes = font.render("Pressione [ENTER] para voltar ao menu", True, WHITE)

        surface.blit(titulo, (surface_width // 2 - titulo.get_width() // 2, 200))
        surface.blit(instrucoes, (surface_width // 2 - instrucoes.get_width() // 2, 300))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_RETURN:  # Enter para voltar ao menu
                return

def interface_derrota(surface):
    """
        Exibe a interface de derrota.
    """
    while True:
        surface.fill(BLACK)
        titulo = font.render("LOST! LOST! LOST! LOST! LOST! LOST! LOST! LOST!", True, WHITE)
        instrucoes = font.render("Pressione [ENTER] para voltar ao menu", True, WHITE)

        surface.blit(titulo, (surface_width // 2 - titulo.get_width() // 2, 200))
        surface.blit(instrucoes, (surface_width // 2 - instrucoes.get_width() // 2, 300))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_RETURN:  # Enter para voltar ao menu
                return
            
def menu(surface):
    """
        Exibe o menu inicial com as opções "Jogar" e "Sair".
        Retorna True se o jogador escolher "Jogar", False se escolher "Sair".
    """

    surface.fill(BLACK)
    titulo = font.render("Jogo da Bola", True, WHITE)
    jogar_texto = font.render("Pressione [1] para Jogar", True, WHITE)
    sair_texto = font.render("Pressione [2] para Sair", True, WHITE)
    
    surface.blit(titulo, (surface_width // 2 - titulo.get_width() // 2, 150))
    surface.blit(jogar_texto, (surface_width // 2 - jogar_texto.get_width() // 2, 250))
    surface.blit(sair_texto, (surface_width // 2 - sair_texto.get_width() // 2, 300))

    pygame.display.update()
    while True:  
    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_1:  
                    return True
                elif event.key == K_2:  
                    return False          

#--------------------- Main --------------------------
def main():
    estado = "menu" #variavel para o menu

    while True:
        if estado == "menu":
            jogar = menu(surface)
            if jogar:
                estado = "jogo"
            else:
                pygame.quit()
                sys.exit()

        elif estado == "jogo":
            game_over = False#var para acabar com o jogo
            tempo_inicial = pygame.time.get_ticks()#inicia o relogio usado no jogo
            CRIAR_BOLA_FANTASMA_EVENT = pygame.USEREVENT + 1
            pygame.time.set_timer(CRIAR_BOLA_FANTASMA_EVENT, 30000) #realiza o evento de criar bola fantasma a cada 30 segundos

            bolas = []
            #cria 5 bolas normais
            for i in range(5):
                raio = random.randint(10, 20)
                x, y = BolaNormal.nao_criar_bolas_em_cima_de_outras(raio, bolas)
                cor = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
                move_x = random.choice([-3, -2, -1, 1, 2, 3])
                move_y = random.choice([-3, -2, -1, 1, 2, 3])
                bola_obj = BolaNormal(x, y, cor, raio, move_x, move_y)
                bolas.append(bola_obj)

            #Criar 3 bolas fantasma
            for i in range(3):
                nova_bola_fantasma = Bola_Fantasma.criar_bola_fantasma_30s(bolas)
                bolas.append(nova_bola_fantasma)

            # Inicializa a bola do utilizador movendo-se para cima com velocidade 3 
            velocidade_inicial = 3
            move_x_inicial = 0  # Sem movimento horizontal
            move_y_inicial = -velocidade_inicial  # Movimento para cima (negativo no eixo Y)

            #jogador = BolaUtilizador(surface_width // 2, surface_height // 2, WHITE, 15, velocidade_inicial, move_x_inicial, move_y_inicial)
            x, y = Bola.nao_criar_bolas_em_cima_de_outras(12, bolas)
            jogador = BolaUtilizador(x, y, WHITE, 12, velocidade_inicial, move_x_inicial, move_y_inicial)#cria bola do utilizador e atribui a var jogador que vai usada em baixo
            bolas.append(jogador)# da add a bola do utilizador a lista das bolas existentes no jogo

            #clico principal do jogo
            while not game_over:
                tempo_decorrido = (pygame.time.get_ticks() - tempo_inicial) // 1000
                bolas = Bola.Modificar_bolas_com_toques(bolas)

                #eventos que podem acontecer no jogo
                #keydown -> tecla pressionada
                for event in pygame.event.get():
                    if event.type == QUIT:
                        game_over = True
                    if event.type == KEYDOWN and event.key == K_ESCAPE:
                        game_over = True
                    if event.type == KEYDOWN:#evento de velocidade da bola
                        #aumenta ou diminui a velocidade da bola do utilizador no terminal e variaveis
                        if event.key == K_v:
                            if jogador.velocidade < 5:
                                jogador.velocidade += 1
                                print(f"Velocidade aumentada para: {jogador.velocidade}")
                        elif event.key == K_b:
                            if jogador.velocidade > 1:
                                jogador.velocidade -= 1
                                print(f"Velocidade diminuida para: {jogador.velocidade}")
                        #aumenta graficamente a velocidade
                        if jogador.move_x:
                            jogador.move_x = jogador.velocidade * (1 if jogador.move_x > 0 else -1)
                        if jogador.move_y:
                            jogador.move_y = jogador.velocidade * (1 if jogador.move_y > 0 else -1)
                        jogador.Setas_cotrolo_do_utilizador(event)
                    #----------------------------------------------------
                    elif event.type == CRIAR_BOLA_FANTASMA_EVENT:#evento feito para criar bola fantasma
                        nova_bola_fantasma = Bola_Fantasma.criar_bola_fantasma_30s(bolas)
                        bolas.append(nova_bola_fantasma)
                        print(f"⚪👻 Bola Fantasma criada em {nova_bola_fantasma.x}, {nova_bola_fantasma.y}")

                # Verifica se ainda existem bolas normais
                if not any(isinstance(bola, BolaNormal) for bola in bolas):
                    # print(" WIN !!! \nTodas as bolas normais foram removidas. \nFim do jogo! :)")
                    interface_vitoria(surface)
                    estado = "menu"
                    break
                
                # Verifica se o jogador perdeu
                if jogador.raio <= 0:
                    interface_derrota(surface)
                    estado = "menu"
                    break

                surface.fill(BLACK)

                # Lista para armazenar bolas a serem removidas
                bolas_para_remover = []

                # Atualiza e desenha bolas
                for bola in bolas:
                    if isinstance(bola, BolaUtilizador):
                        bola.atualizar(surface, bolas)
                    else:
                        bola.atualizar(surface, bolas)
                    bola.desenha(surface)

                # Mostrar velocidade da bola do utilizador
                velocidade_mostrada = False
                for bola in bolas:
                    if isinstance(bola, BolaUtilizador):
                        velocidade_da_bola_ecra = font.render(f"Velocidade -> {bola.velocidade} ", True, WHITE)
                        tempo_x = surface_width - velocidade_da_bola_ecra.get_width() - 10  
                        surface.blit(velocidade_da_bola_ecra, (tempo_x, 10))

                        velocidade_mostrada = True
                        break  # Só precisamos encontrar uma vez a bola do utilizador
                    
                # jogador.atualizar(surface)

                # Timer - Sempre exibido independentemente das bolas
                tempo_texto = font.render(f"Timer -> {tempo_decorrido} s", True, WHITE)
                surface.blit(tempo_texto, (10, 10))

                # Atualiza a tela
                pygame.display.update()
                clock.tick(60)
                
            estado = "menu"  # Retorna ao menu após o jogo acabar
    

if __name__ == "__main__":
    main()