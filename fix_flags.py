Import os
Import sys
Import subprocess
Import shutil
Import string
Import json
Import re
Import collections
Import copy
Import tempfile
Import glob
Import fnmatch
Import math
Import traceback

Import click
Import semantic_version

Import SCons.Errors

Import platformio
from SCons.Script import Import

# Получаем текущее окружение сборки PlatformIO
Import("env")

# 1. Исправляем ошибку ассемблера (удаляем -mlongcalls только для .asm)
def fix_asm_flags(env):
    # Клонируем флаги для ассемблера, убирая -mlongcalls
    If "-mlongcalls" in env.get("ASFLAGS", []):
        New_asflags = [f for f in env["ASFLAGS"] if f != "-mlongcalls"]
        Env.Replace(ASFLAGS=new_asflags)

# Добавляем хук сборки, который сработает перед компиляцией файлов
env.AddPreAction("$BUILD_DIR/src/bios.asm.o", fix_asm_flags)

# 2. Исправляем конфликт SPIRAM (CONFIG_SPIRAM_SUPPORT)
# Удаляем старый макрос из глобальных флагов, если он там есть
if "CPPDEFINES" in env:
    # Фильтруем кортежи или строки макросов
    Env["CPPDEFINES"] = [d for d in env["CPPDEFINES"] if d != "CONFIG_SPIRAM_SUPPORT" and (not isinstance(d, tuple) or d[0] != "CONFIG_SPIRAM_SUPPORT")]
