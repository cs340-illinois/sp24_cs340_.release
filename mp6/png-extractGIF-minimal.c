/**
 * This file is a minimal implementation of the extractGIF part of MP2.
 * It will not pass most of MP2's tests, nor is it designed in a way
 * that could be used as a base for MP2 overall, but it will extract
 * "uiuc" blocks in well-formed PNG files.
 * 
 * We recommend using your own MP2 code, but if you didn't finish that
 * you can use this instead by copying it over ../mp2/png-extractGIF.c
 * 
 * Copyright ⓒ 2024 Luther Tychonievich. All rights reserved.
 * May be used as directed in the course numbered CS 340 at 
 * the University of Illinois Urbana-Champaign.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>

extern const int ERROR_INVALID_PARAMS;
extern const int ERROR_INVALID_FILE;
extern const int ERROR_INVALID_CHUNK_DATA;
extern const int ERROR_NO_UIUC_CHUNK;


typedef struct { char *data; unsigned len; } slice;

slice blockWithTitle(const char *fname, const char *title) {
  slice r = {NULL, -ERROR_INVALID_FILE};
  FILE *f = fopen(fname, "rb");
  if (!f) return r;
  
  unsigned char bytes[8];
  fread(bytes, 1, 8, f);
  if (memcmp(bytes,"\x89PNG\r\n\x1A\n",8)) { fclose(f); return r; }
  
  while (1) {
    char type[4];
    if(fread(&r.len, 4, 1, f) != 1) { r.len = -ERROR_INVALID_CHUNK_DATA; return r; }
    r.len = ntohl(r.len);
    if (fread(type, 1, 4, f) != 4) { r.len = -ERROR_INVALID_CHUNK_DATA; return r; }
    // should check for IEND block
    if (!strncmp(type, "IEND", 4)) {
      r.len = -ERROR_NO_UIUC_CHUNK;
      return r;
    } else if (strncmp(type, title, 4)) {
      // should check CRC, but instead ignoring it
      if (fseek(f, r.len+4, SEEK_CUR)) { r.len = -ERROR_INVALID_CHUNK_DATA; return r; }
      continue;
    } else {
      r.data = (char *)malloc(r.len);
      if (fread(r.data, 1, r.len, f) != r.len) { free(r.data); r.len = -ERROR_INVALID_CHUNK_DATA; r.data = NULL; }
      // should check CRC, but instead ignoring it
      return r;
    }
  }
}


int png_extractGIF(const char *png_filename, const char *gif_filename) {
  slice r = blockWithTitle(png_filename, "uiuc");
  if (r.len < 0) return -r.len;
  if (!r.data) return ERROR_NO_UIUC_CHUNK;
  FILE *out = fopen(gif_filename, "w");
  if (!out) return ERROR_INVALID_PARAMS;
  if (fwrite(r.data, r.len, 1, out) != 1) {
    free(r.data);
    return ERROR_INVALID_PARAMS;
  }
  fclose(out);
  free(r.data);
  return 0;
}
