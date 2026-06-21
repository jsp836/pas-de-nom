import pygame
import sys
import asyncio

# Initialisation de Pygame
pygame.init()

# Taille fixe stable et standard (Le HTML s'occupe de l'étirer sans écran noir)
LARGEUR = 1920
HAUTEUR = 1080
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Défends le Coffre !")
horloge = pygame.time.Clock()

# Variables du jeu
hp_coffre = 100
argent = 0
vague_actuelle = 1
etat_jeu = "JEU" 

# --- CONFIGURATION DE TON PERSO VERT ---
joueur_largeur = 70   
joueur_hauteur = 70   
joueur_x = LARGEUR // 2 - joueur_largeur // 2        
joueur_y = HAUTEUR // 2 - joueur_hauteur // 2 + 200 # Pop un peu sous le coffre       
joueur_vitesse = 10    

# Position des boutons (En haut à droite)
btn_fs_rect = pygame.Rect(LARGEUR - 260, 20, 160, 50)
btn_q_rect = pygame.Rect(LARGEUR - 80, 20, 60, 50)

async def main():
    global joueur_x, joueur_y, etat_jeu, argent, vague_actuelle, hp_coffre
    
    # Permet de communiquer avec le navigateur pour la croix et le plein écran
    from js import window, document
    
    while True:
        # 1. Événements (Souris, Croix, Plein écran)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                # Clic sur la croix rouge
                if btn_q_rect.collidepoint(pos):
                    window.close()
                    window.location.href = "about:blank"
                # Clic sur le bouton Plein Écran
                elif btn_fs_rect.collidepoint(pos):
                    if not document.fullscreenElement:
                        document.documentElement.requestFullscreen()
                    else:
                        document.exitFullscreen()

        # 2. Logique (Contrôles au CLAVIER)
        if etat_jeu == "JEU":
            touches = pygame.key.get_pressed()
            
            if touches[pygame.K_LEFT]:  joueur_x -= joueur_vitesse
            if touches[pygame.K_RIGHT]: joueur_x += joueur_vitesse
            if touches[pygame.K_UP]:    joueur_y -= joueur_vitesse
            if touches[pygame.K_DOWN]:  joueur_y += joueur_vitesse
            
            # Murs du jeu
            if joueur_x < 0: joueur_x = 0
            if joueur_x > LARGEUR - joueur_largeur: joueur_x = LARGEUR - joueur_largeur
            if joueur_y < 0: joueur_y = 0
            if joueur_y > HAUTEUR - joueur_hauteur: joueur_y = HAUTEUR - joueur_hauteur

        # 3. Affichage (Dessins et Couleurs)
        fenetre.fill((30, 30, 30)) # Fond gris foncé
        
        if etat_jeu == "JEU":
            # --- DESSIN DES 4 DIAGONALES EN GRIS PROPRE ---
            # Pygame trace des lignes parfaites avec une épaisseur de 120 pixels
            couleur_chemin = (60, 60, 60)
            largeur_ligne = 120
            
            # Diagonale 1 : Haut-Gauche vers Bas-Droite
            pygame.draw.line(fenetre, couleur_chemin, (0, 0), (LARGEUR, HAUTEUR), largeur_ligne)
            # Diagonale 2 : Haut-Droite vers Bas-Gauche
            pygame.draw.line(fenetre, couleur_chemin, (LARGEUR, 0), (0, HAUTEUR), largeur_ligne)
            
            # --- LE COFFRE AU CENTRE (Jaune parfait) ---
            taille_coffre = 160
            centre_x = LARGEUR // 2 - taille_coffre // 2
            centre_y = HAUTEUR // 2 - taille_coffre // 2
            pygame.draw.rect(fenetre, (255, 255, 0), (centre_x, centre_y, taille_coffre, taille_coffre))
            
            # --- TON PERSO (Vert parfait) ---
            pygame.draw.rect(fenetre, (0, 255, 0), (joueur_x, joueur_y, joueur_largeur, joueur_hauteur))
            
            # --- INTERFACE (Boutons Plein écran et Croix) ---
            pygame.draw.rect(fenetre, (50, 50, 50), btn_fs_rect, border_radius=8)
            pygame.draw.rect(fenetre, (200, 50, 50), btn_q_rect, border_radius=8)
            
            # Textes sur les boutons
            police = pygame.font.SysFont("sans-serif", 30)
            txt_fs = police.render("Plein Ecran", True, (255, 255, 255))
            txt_q = police.render("X", True, (255, 255, 255))
            fenetre.blit(txt_fs, (LARGEUR - 240, 32))
            fenetre.blit(txt_q, (LARGEUR - 60, 32))

        pygame.display.flip()
        horloge.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
