# Aylmer Repair — site de démonstration Odoo

Le dépôt contient le prototype autonome et le module Odoo 20.0 `aylmer_repair_demo`. Une fois le module ajouté à l’instance et installé, il sert la page depuis Odoo Website à `/aylmer-repair-demo` et ajoute un lien dans le menu du site.

## Aperçu local

Ouvrir `index.html` dans un navigateur. Les interactions sont gérées en JavaScript sans dépendances ni serveur.

## Prototype autonome

Ouvrir `index.html` dans un navigateur. Les interactions sont gérées en JavaScript sans dépendances ni serveur.

## Connexion et limites actuelles

- Les exemples de produits, prix, clients, stocks, étapes, dépôts et dossiers sont fictifs.
- Le vérificateur de location calcule une estimation locale; il ne réserve pas d’équipement.
- Les boutons des scénarios font progresser des données d’illustration; ils ne créent pas encore de documents dans Odoo.
- Le schéma Shopify–Odoo illustre un flux à valider. Il ne représente pas un connecteur installé.
- Le module relie la page au site Odoo Website et son bouton de contact au formulaire Odoo existant. Les données publiques actuelles de la boutique (catalogue générique) ne sont pas reprises dans les exemples du prototype.

L’instance cible est Odoo 20.0. Le module est préparé localement sur la branche `dev`. L’URL fournie pointe vers la branche Odoo.sh `develop`; le module n’a pas été déployé ni installé dans la base, et cette différence de branche doit être résolue avant l’activation. L’installation requiert une session administrateur Odoo.
