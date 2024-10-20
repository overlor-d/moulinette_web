D'accord ! Je vais t'expliquer en détail comment faire des requêtes avec SQLAlchemy dans un projet Flask, y compris comment ajouter des utilisateurs, récupérer des utilisateurs, et comment organiser tout cela de manière propre. Je vais aussi te montrer comment utiliser des méthodes dans la classe `User` pour mieux structurer tes requêtes.

### 1. **Concept général : Modèle et requêtes**

Avec SQLAlchemy, tu utilises un **modèle** (comme ta classe `User`) pour interagir avec la base de données. SQLAlchemy te permet de créer, récupérer, mettre à jour et supprimer des enregistrements dans la base de données à l'aide de la session de base de données (qui est gérée par SQLAlchemy).

### 2. **Ajout d'un utilisateur (INSERT)**

Pour ajouter un utilisateur à la base de données, tu dois :
- Créer une instance du modèle (`User` ici).
- L'ajouter à la session de base de données.
- Valider la session avec `commit()` pour sauvegarder les changements.

#### Exemple d'ajout d'utilisateur

Voici comment tu peux créer une route pour ajouter un utilisateur, comme tu l'as déjà vu précédemment :

```python
@app.route('/add_user/<username>/<email>/<int:age>')
def add_user(username, email, age):
    # Crée une nouvelle instance du modèle User
    new_user = User(username=username, email=email, age=age)

    # Ajoute cet utilisateur à la session
    bdd.session.add(new_user)

    # Valide (committe) la transaction dans la base de données
    bdd.session.commit()

    return f'User {username} added successfully with age {age}!'
```

#### Explication détaillée :
1. **`User(username=username, email=email, age=age)`** : Crée une instance de la classe `User` avec les valeurs fournies.
2. **`bdd.session.add(new_user)`** : Ajoute l'instance `new_user` à la session de base de données.
3. **`bdd.session.commit()`** : Sauvegarde les changements dans la base de données en validant la transaction.

### 3. **Récupérer des utilisateurs (SELECT)**

SQLAlchemy offre plusieurs façons de faire des requêtes pour récupérer des données. Voici les méthodes les plus courantes pour interroger la base de données :

#### 1. Récupérer un utilisateur par son **ID**

Tu peux récupérer un utilisateur en utilisant sa clé primaire (par exemple `id`) avec `bdd.session.get()` ou `bdd.session.query().get()`.

```python
@app.route('/get_user/<int:id>')
def get_user(id):
    user = User.query.get(id)  # Récupère l'utilisateur avec l'id spécifié
    if user:
        return f'User found: {user.username}, Email: {user.email}, Age: {user.age}'
    else:
        return 'User not found'
```

#### Explication :
1. **`User.query.get(id)`** : Utilise la méthode `.get()` pour récupérer directement l'utilisateur en fonction de son `id`. Cela renvoie `None` si aucun utilisateur n'est trouvé.

#### 2. Récupérer un utilisateur par **nom d'utilisateur (username)**

Tu peux aussi récupérer des utilisateurs en fonction d'autres colonnes en utilisant des filtres avec la méthode `.filter_by()` ou `.filter()`.

```python
@app.route('/get_user_by_username/<username>')
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()  # Récupère le premier utilisateur avec le username spécifié
    if user:
        return f'User found: {user.username}, Email: {user.email}, Age: {user.age}'
    else:
        return 'User not found'
```

#### Explication :
1. **`User.query.filter_by(username=username)`** : Utilise `.filter_by()` pour appliquer un filtre sur la colonne `username` et récupérer l'utilisateur correspondant.
2. **`.first()`** : Récupère le premier résultat trouvé. Si aucun utilisateur n'est trouvé, ça renverra `None`.

#### 3. Récupérer tous les utilisateurs (SELECT *)

Tu peux récupérer plusieurs utilisateurs ou tous les utilisateurs avec `.all()` :

```python
@app.route('/get_all_users')
def get_all_users():
    users = User.query.all()  # Récupère tous les utilisateurs
    if users:
        users_info = ', '.join([f'{user.username} ({user.email})' for user in users])
        return f'All users: {users_info}'
    else:
        return 'No users found'
```

#### Explication :
1. **`User.query.all()`** : Renvoie une liste contenant tous les enregistrements de la table `User`.

### 4. **Mettre à jour un utilisateur (UPDATE)**

Pour mettre à jour un utilisateur, tu dois :
1. Récupérer l'utilisateur que tu veux modifier.
2. Modifier les attributs de l'instance de l'utilisateur.
3. Commiter la session pour sauvegarder les changements.

#### Exemple de mise à jour :

```python
@app.route('/update_user/<int:id>/<new_email>/<int:new_age>')
def update_user(id, new_email, new_age):
    user = User.query.get(id)  # Récupère l'utilisateur avec l'id spécifié
    if user:
        user.email = new_email  # Modifie l'email
        user.age = new_age      # Modifie l'âge
        bdd.session.commit()    # Sauvegarde les changements
        return f'User {user.username} updated successfully'
    else:
        return 'User not found'
```

#### Explication :
1. **`user.email = new_email`** : Modifie directement l'attribut `email` de l'utilisateur.
2. **`bdd.session.commit()`** : Valide et enregistre les modifications dans la base de données.

### 5. **Supprimer un utilisateur (DELETE)**

Pour supprimer un utilisateur de la base de données, il suffit de :
1. Récupérer l'utilisateur à supprimer.
2. Utiliser `bdd.session.delete()` pour le retirer de la session.
3. Commiter la session pour appliquer la suppression.

#### Exemple de suppression :

```python
@app.route('/delete_user/<int:id>')
def delete_user(id):
    user = User.query.get(id)  # Récupère l'utilisateur avec l'id spécifié
    if user:
        bdd.session.delete(user)  # Supprime l'utilisateur de la session
        bdd.session.commit()       # Valide la transaction (suppression)
        return f'User {user.username} deleted successfully'
    else:
        return 'User not found'
```

#### Explication :
1. **`bdd.session.delete(user)`** : Supprime l'utilisateur de la session de base de données.
2. **`bdd.session.commit()`** : Sauvegarde la suppression dans la base de données.

### 6. **Requêtes avancées avec `.filter()`**

Si tu veux faire des requêtes plus complexes, tu peux utiliser `.filter()` pour appliquer des conditions plus flexibles. Par exemple, si tu veux récupérer tous les utilisateurs de plus de 30 ans :

```python
@app.route('/users_above_age/<int:age>')
def users_above_age(age):
    users = User.query.filter(User.age > age).all()  # Récupère tous les utilisateurs avec un âge supérieur à celui spécifié
    if users:
        users_info = ', '.join([f'{user.username} ({user.age} ans)' for user in users])
        return f'Users above {age} years: {users_info}'
    else:
        return f'No users found above {age} years'
```

#### Explication :
- **`User.query.filter(User.age > age)`** : Utilise `.filter()` pour appliquer une condition sur l'âge des utilisateurs.

### 7. **Requêtes personnalisées avec des méthodes de classe**

Pour organiser ton code et rendre tes requêtes réutilisables, tu peux définir des **méthodes de classe** dans ton modèle `User`. Voici quelques exemples :

#### Exemple de méthodes de classe pour récupérer un utilisateur par email :

```python
class User(bdd.Model):
    id = bdd.Column(bdd.Integer, primary_key=True)
    username = bdd.Column(bdd.String(80), unique=True, nullable=False)
    email = bdd.Column(bdd.String(120), unique=True, nullable=False)
    age = bdd.Column(bdd.Integer)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()  # Requête pour trouver un utilisateur par email
```

#### Utilisation de la méthode dans une route :

```python
@app.route('/find_user_by_email/<email>')
def find_user_by_email(email):
    user = User.find_by_email(email)  # Appel de la méthode de classe pour trouver l'utilisateur
    if user:
        return f'User found: {user.username}, Age: {user.age}'
    else:
        return 'User not found'
```

### 8. **Gestion des transactions et des erreurs**

Il est important de gérer les erreurs lorsque tu manipules des données avec SQLAlchemy. Par exemple, si une insertion échoue ou une mise à jour génère une erreur, il est préférable d'annuler la transaction pour éviter des données corrompues.

#### Exemple de gestion des erreurs :

```python
from sqlalchemy.exc import SQLAlchemyError

@app.route('/add_user_safe/<username>/<email>/<int:age>')
def add_user_safe(username, email, age):
    try:
        new_user = User(username=username,

 email=email, age=age)
        bdd.session.add(new_user)
        bdd.session.commit()
        return f'User {username} added successfully'
    except SQLAlchemyError as e:
        bdd.session.rollback()  # Annule la transaction si une erreur survient
        return f'Error adding user: {str(e)}'
```

#### Explication :
- **`try` / `except SQLAlchemyError`** : Cela capture toutes les erreurs liées à SQLAlchemy et permet de gérer les exceptions.
- **`bdd.session.rollback()`** : Annule la transaction en cours si une erreur survient, ce qui évite les incohérences dans la base de données.

---

### Récapitulatif

1. **Ajouter un utilisateur** : Crée une instance, ajoute-la à la session, et commit.
2. **Récupérer des utilisateurs** : Utilise `query.get()` pour l'ID ou `filter_by()`/`filter()` pour d'autres colonnes.
3. **Mettre à jour un utilisateur** : Récupère l'utilisateur, modifie les attributs, et commit.
4. **Supprimer un utilisateur** : Récupère l'utilisateur, utilise `delete()`, et commit.
5. **Requêtes avancées** : Utilise `.filter()` pour des conditions complexes.
6. **Organisation** : Utilise des méthodes de classe pour encapsuler des requêtes.
7. **Gestion des erreurs** : Utilise `rollback()` pour annuler les transactions en cas d'erreur.

En suivant cette approche, tu pourras structurer et manipuler efficacement ta base de données avec Flask et SQLAlchemy.