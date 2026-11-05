import os
import sys

# Получаем текущее окружение сборки PlatformIO
from SCons.Script import Import

Import("env")

# 1. Исправляем ошибку ассемблера (удаляем -mlongcalls только для файла bios.asm)
def fix_asm_flags(env):
    if "ASFLAGS" in env:
        new_asflags = [f for f in env["ASFLAGS"] if f != "-mlongcalls"]
        env.Replace(ASFLAGS=new_asflags)

# Добавляем хук сборки, который сработает перед компиляцией bios.asm
env.AddPreAction("$BUILD_DIR/src/bios.asm.o", fix_asm_flags)

# 2. Исправляем конфликт SPIRAM (CONFIG_SPIRAM_SUPPORT)
if "CPPDEFINES" in env:
    env["CPPDEFINES"] = [d for d in env["CPPDEFINES"] if d != "CONFIG_SPIRAM_SUPPORT" and (not isinstance(d, tuple) or d[0] != "CONFIG_SPIRAM_SUPPORT")]
    
