
# Modificaciones del código

****

## [/bin](bin)

### [Assets](bin/assets)
* Modificar el sprite del personaje + archivo de coordenadas

### [Config](bin/config)
* Añadir VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR a ['players.json'](bin/config/players.json)

****

## [/src](src)

### [GameManager](src/control/GameManager.py)
* self.pila[len(self.pila)-1] en vez de pila[0]
* añadir función para cambiar de escena
	- flag para cambiar de escena a parte de flag para acabar ejecución programa
* Mover la comprobación de pulsación de tecla ESC para la propia fase, en el bucle principal solo debería tener comprobación del flag 'exit_program'
* Crear función de exitProgram() que se pueda llamar desde las distintas pantallas/fases
* ~~Función para apilar escenas~~

### [Fase](src/control/GameLevel.py)
* Añadir comprobación de pulsación de tecla quit()
* Modificar el método update() para llevar a cabo las pausas


### [DataRetriever](src/data/DataRetriever.py)
* Añadir CargarImagen y CargarArchivoCoordenadas

### [Personaje](src/character)
* ~~Modificar estructura de clases~~
* Cambiar constructor de [Character](src/character/Character.py) (self, data, id) y buscar los recursos a partir del id
* Crear EnemyPlayer, clase similar a player, pero con IA
* Traducir todas las clases


