import bpy  # type: ignore
import json
import sys

def generate_3d_model(json_path):
    # 1. Limpiar la escena por defecto
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, do_operators=True)

    # 2. Leer los datos de componentes (de dónde vendría el output de la IA)
    with open(json_path, 'r') as f:
        componentes = json.load(f)

    z_offset = 0 # Usado para apilar los objetos

    # 3. Generar cada componente
    for i, comp in enumerate(componentes):
        l, a, e = comp['dimensiones_cm']
        
        # Crear un cubo simple
        bpy.ops.mesh.primitive_cube_add(size=1)
        obj = bpy.context.object
        
        # Escalar al tamaño (L x A x E). Los valores de CM se convierten a metros.
        obj.scale = (l / 100, a / 100, e / 100) 
        
        # Mover para apilarlos o colocarlos en el origen.
        # Aquí los apilamos para simpleza.
        obj.location.z = z_offset + (e / 100) / 2
        z_offset += e / 100
        
        # Nombrar el objeto y añadir metadata
        obj.name = comp['nombre']
        
        # Añadir un material básico
        mat = bpy.data.materials.new(name=f"Material_{comp['material']}")
        mat.diffuse_color = (i * 0.2, 1 - i * 0.2, 0.5, 1) # Color simple
        obj.data.materials.append(mat)
    
    # 4. Guardar el archivo .blend final
    output_path = json_path.replace(".json", ".blend")
    bpy.ops.wm.save_as_mainfile(filepath=output_path)
    
    print(f"[BLENDER] Modelo 3D real generado en: {output_path}")


# ----------------------------------------------------
# Lógica de Ejecución (cuando Blender llama a este script)
# ----------------------------------------------------

try:
    # Capturamos el argumento pasado por la línea de comandos de Blender
    # El archivo JSON simulado debe ser el primer argumento después de --
    json_path = sys.argv[-1] 
    
    # Esto ejecuta la función principal de generación
    generate_3d_model(json_path)
    
except Exception as e:
    print(f"[ERROR BLENDER] Fallo en la generación 3D: {e}")