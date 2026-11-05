/* What The Powder Toy's Posix platform files ask of libnix and it lacks:
 * execl(), for restarting after an update, which this build never does.
 * The AmiCradle Team. GPL 3 or later, like The Powder Toy. */
#include <errno.h>

int execl(const char *path, const char *arg, ...)
{
	(void)path;
	(void)arg;
	errno = ENOSYS;
	return -1;
}
