The Powder Toy for AmigaOS 3.x
==============================

The Powder Toy 100.1.400 (https://github.com/The-Powder-Toy/The-Powder-Toy,
GPL 3), the falling-sand physics sandbox: powders, liquids, gases, heat,
pressure, electricity and nearly two hundred elements to mix. For AmigaOS
3.x on a 68040 or 68060 with an FPU and an RTG screen, on OpenGPU's SDL 2.

Base: tag v100.1.400 (commit d768aeb89acad986bd252d7e904bf44bb374545f).
Branch team2/powdertoy-amiga.

Status: built, not yet run in the lab.


What you need
-------------

- A 68040 or 68060 with an FPU, AmigaOS 3.x, an RTG card (or the
  AmigaChrome lab). The simulation is heavy for a 68k: expect it slow.
- OpenGPU 0.6 or later: opengpu.library and LIBS:OpenGPU/SDL2.module
  (installed by OpenUp).
- About 5 MB of disk. The game's data (its font and pictures) is built in.


How to play
-----------

Open the ThePowderToy drawer and double-click ThePowderToy. Its settings
(powder.pref), saves and stamps are kept in the drawer.


Building
--------

GFOpenAmigaGCC 16.2.0-open4 or later, the OpenGPU developer kit, the
Team's static zlib, libpng and bzip2 (jsoncpp 1.9.6's sources are in
amiga/deps):

    make -f amiga/Makefile.amigaos -j2 dist \
         STOVE=/path/to/openamigagcc-16.2.0-open4 \
         NDK=/path/to/OpenNDK/Include_H SDL2KIT=/path/to/opengpu-sdk \
         DEPS=/path/to/m68k-amigaos

Meson is not run: amiga/gen.py makes the files it would generate
(Config.h, VcsTag.h, ElementNumbers.h, ToolNumbers.h and the built-in
resources) into build/amigaos/gen, and amiga/Makefile.amigaos has the
source lists. Output: build/amigaos/ThePowderToy (stripped; .debug beside
it); 'dist' makes dist/ThePowderToy/ and dist/ThePowderToy.info.


What was cut or changed
-----------------------

- No online saves, login or updates (Meson's http=false:
  requestmanager/Null.cpp). Local saves and stamps work.
- No Lua console scripts (lua=none: PlainCommandInterface.cpp).
- No Newtonian gravity: simulation/gravity/Null.cpp, upstream's own
  no-FFT gravity (its render tool uses it), so fftw3f is not needed. The
  gravity tools draw but do nothing.
- No platform clipboard (clipboard/Local.cpp: copy and paste work within
  the game).
- src/common/platform/Amiga.cpp in place of Null.cpp: the time from
  SDL_GetTicks(); the program's name as PROGDIR:powder.
- src/common/platform/Posix.cpp: Millisleep() with usleep() (libnix
  declares nanosleep() and usleep() for POSIX builds only).
  PosixProc.cpp: no realpath() in libnix. amiga/posix_extra.c: execl()
  fails (it is only for restarting after an update).
- src/simulation/Stickman.h: playerst is 4-byte aligned (m68k aligns int
  to 2 bytes; SnapshotDelta.cpp needs the struct in 32-bit words).
- src/PowderToySDL.cpp: no SDL_GL_LoadLibrary() workaround at exit (it is
  for OpenGL windows on Linux; no GL is linked here).
- src/PowderToy.cpp: main() first moves into the drawer and sets up the
  closing of the screens SDL2.module 0.6 can leave (amiga/amiga_start.c,
  amiga/amiga_screens.c). amiga/stack.c: 512 KB of stack.
- Threads (the game renders thumbnails and runs tasks on threads): the
  toolchain's libpthread; libatomic for 64-bit atomics.


Licences
--------

The Powder Toy: GPL 3 (LICENSE.txt in the drawer). jsoncpp: MIT (public
domain where that applies). The amiga/ files are the AmiCradle Team's,
GPL 3 or later.
