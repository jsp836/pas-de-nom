<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Défends le Coffre !</title>
    <style>
        body {
            background-color: #111;
            color: #fff;
            text-align: center;
            font-family: sans-serif;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
        canvas {
            background-color: #1e1e1e;
            display: block;
            margin: 0 auto;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
    </style>
</head>
<body>

    <h2 style="margin: 5px 0;">🕹️ Défends le Coffre ! (Version Mobile)</h2>
    <p style="margin: 5px 0; font-size: 14px;">Touche l'écran pour déplacer le carré vert vers ton doigt !</p>
    
    <canvas id="jeuCanvas" width="1200" height="800"></canvas>

    <script>
        const canvas = document.getElementById("jeuCanvas");
        const ctx = canvas.getContext("2d");

        // Variables du jeu
        let hp_coffre = 100;
        let argent = 0;
        let vague_actuelle = 1;
        let etat_jeu = "JEU"; // JEU, MAGASIN, GAMEOVER

        // Configuration du joueur (Perso Vert)
        let joueur_x = 965;
        let joueur_y = 500;
        let joueur_vitesse = 6;
        let joueur_largeur = 70;
        let joueur_hauteur = 70;

        // Cible pour le déplacement tactile
        let cible_x = joueur_x;
        let cible_y = joueur_y;

        // Gestion du tactile / Clic Souris
        function gererAction(clientX, clientY) {
            const rect = canvas.getBoundingClientRect();
            // Convertit les coordonnées de l'écran par rapport au canvas 1200x800
            cible_x = (clientX - rect.left) * (canvas.width / rect.width) - joueur_largeur/2;
            cible_y = (clientY - rect.top) * (canvas.height / rect.height) - joueur_hauteur/2;
        }

        canvas.addEventListener("mousedown", (e) => gererAction(e.clientX, e.clientY));
        canvas.addEventListener("touchstart", (e) => {
            gererAction(e.touches[0].clientX, e.touches[0].clientY);
        });

        // Boucle principale du jeu
        function update() {
            if (etat_jeu === "JEU") {
                // Déplacement fluide vers la cible tactile
                let dx = cible_x - joueur_x;
                let dy = cible_y - joueur_y;
                let distance = Math.sqrt(dx * dx + dy * dy);

                if (distance > joueur_vitesse) {
                    joueur_x += (dx / distance) * joueur_vitesse;
                    joueur_y += (dy / distance) * joueur_vitesse;
                }

                // Gestion des murs
                if (joueur_x < 0) joueur_x = 0;
                if (joueur_x > 1200 - joueur_largeur) joueur_x = 1200 - joueur_largeur;
                if (joueur_y < 0) joueur_y = 0;
                if (joueur_y > 800 - joueur_hauteur) joueur_y = 800 - joueur_hauteur;
            }

            dessiner();
            requestAnimationFrame(update);
        }

        // Dessin des graphismes (équivalent de tes pygame.draw.rect)
        function dessiner() {
            // Fond
            ctx.fillStyle = "#1e1e1e";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            if (etat_jeu === "JEU") {
                // Dessiner les chemins gris de ton code
                ctx.fillStyle = "#3c3c3c";
                ctx.fillRect(0, 0, 200, 400);
                ctx.fillRect(200, 200, 75, 200);
                ctx.fillRect(275, 0, 200, 400);
                ctx.fillRect(475, 0, 75, 200);
                ctx.fillRect(550, 0, 200, 400);
                ctx.fillRect(750, 300, 100, 100);
                ctx.fillRect(0, 750, 200, 400);
                ctx.fillRect(200, 810, 75, 200);

                // Coffre (Jaune)
                ctx.fillStyle = "#ffff00";
                ctx.fillRect(850, 300, 300, 400);

                // Joueur (Vert)
                ctx.fillStyle = "#00ff00";
                ctx.fillRect(joueur_x, joueur_y, joueur_largeur, joueur_hauteur);
                
                // Interface HP / Vague
                ctx.fillStyle = "#fff";
                ctx.font = "24px sans-serif";
                ctx.fillText("HP Coffre: " + hp_coffre, 20, 40);
                ctx.fillText("Vague: " + vague_actuelle, 20, 70);
            }
        }

        // Lancement du jeu
        update();
    </script>
</body>
</html>
