import pygame
import sys
import asyncio

# Initialisation de Pygame
pygame.init()

# On utilise une taille fixe standard que le HTML va adapter proprement sans écran noir
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
joueur_x = 1400        
joueur_y = 500        
joueur_vitesse = 12    
joueur_largeur = 70   
joueur_hauteur = 70   

# Cible pour le tactile
cible_x = joueur_x
cible_y = joueur_y
mode_tactile = False

# Position des boutons virtuels (en haut à droite)
btn_fullscreen_rect = pygame.Rect(LARGEUR - 260, 20, 160, 50)
btn_quitter_rect = pygame.Rect(LARGEUR - 80, 20, 60, 50)

async def main():
    global joueur_x, joueur_y, etat_jeu, argent, vague_actuelle, hp_coffre, cible_x, cible_y, mode_tactile
    
    # Importation dynamique pour interagir avec le navigateur depuis Python
    from js import window, document
    
    while True:
        # 1. Gestion des événements (Clavier, Souris, Tactile)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Clic ou Touche sur l'écran
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN, pygame.FINGERMOTION):
                mode_tactile = True
                
                # Récupération des coordonnées x, y
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos_x, pos_y = event.pos
                else:
                    # Pour les mobiles (coordonnées normalisées de 0 à 1)
                    pos_x = int(event.x * LARGEUR)
                    pos_y = int(event.y * HAUTEUR)
                
                # Vérification des boutons
                if btn_quitter_rect.collidepoint(pos_x, pos_y):
                    window.close()
                    window.location.href = "about:blank"
                elif btn_fullscreen_rect.collidepoint(pos_x, pos_y):
                    if not document.fullscreenElement:
                        document.documentElement.requestFullscreen()
                    else:
                        document.exitFullscreen()
                else:
                    # Si on ne clique pas sur un bouton, on déplace le joueur
                    cible_x = pos_x - joueur_largeur // 2
                    cible_y = pos_y - joueur_hauteur // 2

        # 2. Logique de déplacement
        if etat_jeu == "JEU":
            touches = pygame.key.get_pressed()
            
            # Si on utilise le clavier, on coupe le mode tactile
            if touches[pygame.K_LEFT] or touches[pygame.K_RIGHT] or touches[pygame.K_UP] or touches[pygame.K_DOWN]:
                mode_tactile = False

            if mode_tactile:
                # Déplacement tactile fluide
                dx = cible_x - joueur_x
                let_dy = cible_y - joueur_y
                distance = (dx**2 + let_dy**2)**0.5
                if distance > joueur_vitesse:
                    joueur_x += (dx / distance) * joueur_vitesse
                    joueur_y += (let_dy / distance) * joueur_vitesse
            else:
                # Déplacement au Clavier
                if touches[pygame.K_LEFT]:  joueur_x -= joueur_vitesse
                if touches[pygame.K_RIGHT]: joueur_x += joueur_vitesse
                if touches[pygame.K_UP]:    joueur_y -= joueur_vitesse
                if touches[pygame.K_DOWN]:  joueur_y += joueur_vitesse
            
            # Murs
            if joueur_x < 0: joueur_x = 0
            if joueur_x > LARGEUR - joueur_largeur: joueur_x = LARGEUR - joueur_largeur
            if joueur_y < 0: joueur_y = 0
            if joueur_y > HAUTEUR - joueur_hauteur: joueur_y = HAUTEUR - joueur_hauteur

        # 3. Affichage (Dessin)
        fenetre.fill((30, 30, 30)) 
        
        if etat_jeu == "JEU":
            # Chemins gris
            pygame.draw.rect(fenetre, (60, 60, 60), (0, 100, 400, 200))
            pygame.draw.rect(fenetre, (60, 60, 60), (400, 100, 200, 600))
            pygame.draw.rect(fenetre, (60, 60, 60), (600, 500, 600, 200))
            
            # Coffre (Jaune)
            pygame.draw.rect(fenetre, (255, 255, 0), (1200, 400, 250, 400))
            
            # Ton perso (Vert)
            pygame.draw.rect(fenetre, (0, 255, 0), (joueur_x, joueur_y, joueur_largeur, joueur_hauteur))
            
            # Dessin des boutons d'interface (Plein écran et Croix)
            pygame.draw.rect(fenetre, (50, 50, 50), btn_fullscreen_rect, border_radius=8)
            pygame.draw.rect(fenetre, (200, 50, 50), btn_quitter_rect, border_radius=8)
            
            # Textes simples sur les boutons (en blanc)
            police = pygame.font.SysFont("sans-serif", 30)
            texte_fs = police.render("Plein Ecran", True, (255, 255, 255))
            texte_q = police.render("X", True, (255, 255, 255))
            fenetre.blit(texte_fs, (LARGEUR - 240, 32))
            fenetre.blit(texte_q, (LARGEUR - 60, 32))

        pygame.display.flip()
        horloge.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
