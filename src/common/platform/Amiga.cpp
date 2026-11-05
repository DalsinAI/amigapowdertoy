// AmigaOS 3.x: common/platform/Null.cpp, plus the time and the program's
// name (Linux.cpp has them from clock_gettime() and /proc). The AmiCradle
// Team. GPL 3 or later, like The Powder Toy.
#include "Platform.h"
#include "Config.h"
#include <SDL.h>
#include <cstdio>

namespace Platform
{
void OpenURI(ByteString uri)
{
	fprintf(stderr, "cannot open URI: not implemented\n");
}

bool CanUpdate()
{
	return false;
}

void SetupCrt()
{
}

long unsigned int GetTime()
{
	return SDL_GetTicks();
}

ByteString ExecutableNameFirstApprox()
{
	return ByteString("PROGDIR:") + APPEXE;
}
}
