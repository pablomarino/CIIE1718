
# Tareas a llevar a cabo


## Jose
* ~~Hud~~
* ~~Mover character para la carpeta view~~
* ~~Mover menu para la carpeta~~
* ~~Creación de mapas desde fichero txt~~
* ~~Creación de enemigos desde fichero txt~~
* Impedir que jugador se salga de la pantalla en el eje x
* Mover enemigos

## Pablo
* ~~character corregir salto~~
* ~~character corregir scroll enemigo~~
* items

## Matías
* ~~director cargar menu~~
* empezar el juego con el menu, y cargar los niveles desde ahí
* transición entre fases

## Uxía
* memoria
* colisión jugador con enemigos

## Óscar
* ~~Audio~~
* Implementar ataque del jugador


<br><br><br><br><br><br><br>








## [CARPETA /bin](bin)

****

### [Assets](bin/assets)
* ~~Modificar el **sprite del personaje + archivo de coordenadas**~

### [Config](bin/config)
* ~~Añadir **VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR** a ['players.json'](bin/config/players.json), actualmente están en [Player.py](src/character/Player.py)~~

<br><br>

## [CARPETA /src](src)

****

### [GameManager](src/control/GameManager.py)
* ~~Función para añadir escenas a la pila~~
* Función para **eliminar escena de la pila**
* **Crear función changeScene()** que active un flag **change_scene**, que se comprobará en el bucle principal (mirar apuntes)
* **Crear función exitProgram()** que active un flag **exit_program**, que se comprobará en el bucle principal (mirar apuntes)
* **Eliminar** comprobación de pulsación de **tecla ESC** en el bucle principal **cuando alguien lo haya implementado ya en [GameLevel.py](src/control/GameLevel.py)**
> **Nota:** Quizás haga falta cambiar pila[0] por pila[len(self.pila)-1]

### [Fase](src/control/GameLevel.py)
* Añadir comprobación de **pulsación de tecla ESC**
* Modificar el método update() para llevar a cabo las pausas

### [DataRetriever](src/data/DataRetriever.py)
* Añadir **CargarImagen() y CargarArchivoCoordenadas()**, actualmente están en [GestorRecursos.py](src/character/GestorRecursos.py)

### [Personaje](src/character)
* ~~Modificar estructura de clases~~
* ~~Corregir problema de salto infinito~~
* ~~Cambiar **constructor** de [Character](src/character/Character.py) (self, data, id) y buscar los recursos a partir del id~~
* Crear **EnemyPlayer**, clase similar a player, pero con IA
* **Traducir** todas las clases
* Cuando el personaje **salta** permitir **moverse a los lados.**
* Crear una **nueva postura** del personaje que sea **FALLING** para tener una animación solo de caída, independiente de la animación de salto.


