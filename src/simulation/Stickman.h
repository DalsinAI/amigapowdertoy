#pragma once

constexpr auto MAX_FIGHTERS = 100;
#ifdef __amigaos__
// m68k aligns int to 2 bytes; SnapshotDelta.cpp needs a size in 32-bit words
struct alignas(4) playerst
#else
struct playerst
#endif
{
	char comm;           //command cell
	char pcomm;          //previous command
	int elem;            //element power
	float legs[16];      //legs' positions
	float accs[8];       //accelerations
	char spwn;           //if stick man was spawned
	unsigned int frames; //frames since last particle spawn - used when spawning LIGH
	bool rocketBoots;
	bool fan;
	int spawnID;         //id of the SPWN particle that spawns it
};
