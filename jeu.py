import pygame
import sys
import asyncio  # Obligatoire pour que le jeu ne freeze pas sur internet !

# Initialisation de Pygame
pygame.init()
fenetre = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Défends le Coffre !")
horloge = pygame.time.Clock()

# Variables du jeu
hp_coffre = 100
argent = 0
vague_actuelle = 1
degats_joueur = 10
etat_jeu = "JEU" 

# --- CONFIGURATION DE TON PERSO VERT ---
joueur_x = 965        
joueur_y = 500        
joueur_vitesse = 6    
joueur_largeur = 70   
joueur_hauteur = 70   

# Fonction principale adaptée pour le Web (async)
async def main():
    global joueur_x, joueur_y, etat_jeu, argent, vague_actuelle, hp_coffre
    
    while True:
        # 1. Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if etat_jeu == "MAGASIN":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if argent >= 10:
                        hp_coffre += 20
                        argent -= 10
                        etat_jeu = "JEU" 
                        vague_actuelle += 1
            
            # Déplacement tactile rudimentaire pour téléphone (clic/touche l'écran)
            if event.type == pygame.MOUSEBUTTONDOWN and etat_jeu == "JEU":
                souris_x, souris_y = pygame.mouse.get_pos()
                # Le perso se déplace vers le point touché
                if souris_x < joueur_x: joueur_x -= 30
                if souris_x > joueur_x: joueur_x += 30
                if souris_y < joueur_y: joueur_y -= 30
                if souris_y > joueur_y: joueur_y += 30

        # 2. Logique du jeu selon l'état actuel
        if etat_jeu == "JEU":
            # Contrôles clavier (restent actifs pour le PC)
            touches = pygame.key.get_pressed()
            if touches[pygame.K_LEFT]:  joueur_x -= joueur_vitesse
            if touches[pygame.K_RIGHT]: joueur_x += joueur_vitesse
            if touches[pygame.K_UP]:    joueur_y -= joueur_vitesse
            if touches[pygame.K_DOWN]:  joueur_y += joueur_vitesse
            
            # --- GESTION DES MURS (Ajustée aux dimensions 1200x800 de ta fenêtre) ---
            if joueur_x < 0: joueur_x = 0
            if joueur_x > 1200 - joueur_largeur: joueur_x = 1200 - joueur_largeur
            if joueur_y < 0: joueur_y = 0
            if joueur_y > 800 - joueur_hauteur: joueur_y = 800 - joueur_hauteur

            vague_terminee = False 
            if vague_terminee:
                argent += hp_coffre * 0.5 
                etat_jeu = "MAGASIN"
                
            if hp_coffre <= 0:
                etat_jeu = "GAMEOVER"

        # 3. Affichage (Dessin)
        fenetre.fill((30, 30, 30)) 
        
        if etat_jeu == "JEU":
            # Chemins
            pygame.draw.rect(fenetre, (60, 60, 60), (0, 0, 200, 400))
            pygame.draw.rect(fenetre, (60, 60, 60), (200, 200, 75, 200))
            pygame.draw.rect(fenetre, (60, 60, 60), (275, 0, 200, 400))
            pygame.draw.rect(fenetre, (60, 60, 60), (475, 0, 75, 200))
            pygame.draw.rect(fenetre, (60, 60, 60), (550, 0, 200, 400))
            pygame.draw.rect(fenetre, (60, 60, 60), (750, 300, 100, 100))
            
            pygame.draw.rect(fenetre, (60, 60, 60), (0, 750, 200, 400))
            pygame.draw.rect(fenetre, (60, 60, 60), (200, 810, 75, 200))
            
            # Coffre (Jaune)
            pygame.draw.rect(fenetre, (255, 255, 0), (850, 300, 300, 400))
            
            # Ton perso (Vert)
            pygame.draw.rect(fenetre, (0, 255, 0), (joueur_x, joueur_y, joueur_largeur, joueur_hauteur))
            
        elif etat_jeu == "MAGASIN":
            pass
            
        elif etat_jeu == "GAMEOVER":
            pass

        pygame.display.flip()
        horloge.tick(60)
        await asyncio.sleep(0)  # Laisse le navigateur respirer et évite le freeze !

# Lancement du programme
asyncio.run(main())
