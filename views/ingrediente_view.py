from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from controler.ingrediente_controler import IngredienteController
controller = IngredienteController()
ingredientes = controller.select_ingrediente()

for ingrediente in ingredientes:
    print(ingrediente.nome)
