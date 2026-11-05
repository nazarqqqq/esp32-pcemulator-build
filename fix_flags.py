import os

# Получаем текущее окружение сборки PlatformIO
from SCons.Script import Import

Import("env")

# Функция исправления флагов теперь принимает все обязательные параметры SCons
def fix_asm_flags(target, source, env):
    if "ASFLAGS" in env:
        # Полностью очищаем -mlongcalls из флагов ассемблера для bios.asm
        new_asflags = [f for f in env["ASFLAGS"] if f != "-mlongcalls"]
        env.Replace(ASFLAGS=new_asflags)

# Добавляем хук перед сборкой конкретного объекта bios.asm.o
env.AddPreAction("$BUILD_DIR/src/bios.asm.o", fix_asm_flags)

# Исправляем конфликт SPIRAM (CONFIG_SPIRAM_SUPPORT) в глобальных макросах
if "CPPDEFINES" in env:
    env["CPPDEFINES"] = [d for d in env["CPPDEFINES"] if d != "CONFIG_SPIRAM_SUPPORT" and (not isinstance(d, tuple) or d[0] != "CONFIG_SPIRAM_SUPPORT")]
    
