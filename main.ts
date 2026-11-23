// "The World in One Day" — 23 November 2026 (Node 22, standard library only).
//
// Copies the pre-rendered front page (entry.png, drawn by render23.py with Pillow)
// to /output/entry.png, after validating the entry against the bounty limits:
//   - PNG or JPEG only (checked by magic bytes)
//   - at most 1,048,576 bytes
//   - at most 1024 x 1024 pixels (PNG IHDR / JPEG SOF dimensions)
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const MAX_BYTES = 1048576;
const MAX_DIMENSION = 1024;

const source = join(dirname(fileURLToPath(import.meta.url)), 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');

if (!existsSync(source)) {
  throw new Error(`entry image not found: ${source}`);
}

const bytes = readFileSync(source);
if (bytes.length > MAX_BYTES) {
  throw new Error(
    `entry image is ${bytes.length} bytes, over the ${MAX_BYTES} byte limit`,
  );
}

const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const jpegMagic = Buffer.from([0xff, 0xd8, 0xff]);

let format: string;
let width: number;
let height: number;

if (bytes.subarray(0, 8).equals(pngMagic)) {
  // PNG: width and height are big-endian uint32 at offsets 16 and 20 (IHDR).
  // Also confirm the first chunk really is IHDR, so a truncated or corrupt
  // header is rejected instead of being read as dimensions.
  if (bytes.subarray(12, 16).toString('ascii') !== 'IHDR') {
    throw new Error('malformed PNG: first chunk is not IHDR');
  }
  format = 'PNG';
  width = bytes.readUInt32BE(16);
  height = bytes.readUInt32BE(20);
} else if (bytes.subarray(0, 3).equals(jpegMagic)) {
  // JPEG: walk the markers until a Start Of Frame (baseline 0xC0 or
  // progressive 0xC2); its segment holds height then width, big-endian.
  format = 'JPEG';
  let offset = 2;
  let found = false;
  while (offset + 9 < bytes.length) {
    if (bytes[offset] !== 0xff) {
      throw new Error('malformed JPEG: expected a marker');
    }
    const marker = bytes[offset + 1];
    const length = bytes.readUInt16BE(offset + 2);
    if (marker === 0xc0 || marker === 0xc2) {
      height = bytes.readUInt16BE(offset + 5);
      width = bytes.readUInt16BE(offset + 7);
      found = true;
      break;
    }
    offset += 2 + length;
  }
  if (!found) {
    throw new Error('malformed JPEG: no Start Of Frame marker found');
  }
} else {
  throw new Error('entry image is neither PNG nor JPEG (bad magic bytes)');
}

if (width! > MAX_DIMENSION || height! > MAX_DIMENSION) {
  throw new Error(
    `entry image is ${width}x${height}, over the ${MAX_DIMENSION}x${MAX_DIMENSION} limit`,
  );
}

mkdirSync(outDir, { recursive: true });
writeFileSync(dest, bytes);
console.log(
  `wrote ${dest}: ${format} ${width}x${height}, ${bytes.length} bytes`,
);
