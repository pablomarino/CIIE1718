
# Modificaciones del código

****

## /bin

### Assets
* Modificar el sprite del personaje + archivo de coordenadas

****

## /src

### GameManager
* self.pila[len(self.pila)-1] en vez de pila[0]
* añadir función para cambiar de escena
	- flag para cambiar de escena a parte de flag para acabar ejecución programa
* Mover la comprobación de pulsación de tecla ESC para la propia fase, en el bucle principal solo debería tener comprobación del flag 'exit_program'
* Crear función de exitProgram() que se pueda llamar desde las distintas pantallas/fases
* ~~Función para apilar escenas~~

### Fase
* Añadir comprobación de pulsación de tecla quit()
* Modificar el método update() para llevar a cabo las pausas


### Personaje
* ~~Modificar estructura de clases~~
	~~- Sprite~~
	~~- MiSprite~~
	~~- Personaje~~
	~~- Jugador~~

