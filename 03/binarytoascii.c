#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
  float check_flag, data, *inp_data;
  int i, size_data;
  FILE *ifp, *outfile;

  if ((ifp = fopen(argv[1], "rb")) == NULL)
  { // open the binary file.
    fprintf(stderr, "Cannot open file: %s\n", argv[1]);
    exit(EXIT_FAILURE);
  }

  if ((outfile = fopen(argv[2], "w")) == NULL)
  {
    fprintf(stderr, "Cannot write file: %s\n", argv[2]);
    exit(EXIT_FAILURE);
  }

  check_flag = 0;
  size_data = 0;

  while (1)
  {
    if (fread(&data, sizeof(float), 1, ifp) != 1)
    {
      check_flag = 1;
    }
    if (check_flag == 1)
      break;

    if (size_data % 2 == 1)
    {
      fprintf(outfile, "%f\n", data);
    }
    else
    {
      fprintf(outfile, "%f,", data);
    }

    size_data++;
  }
  //  End.

  // Appendix.
  inp_data = malloc(sizeof(short) * size_data); // Allocate memory.
  fseek(ifp, 0, SEEK_SET);                      // You can read the data file again.

  for (i = 0; i < size_data; i++)
  {
    if (fread(&inp_data[i], sizeof(short), 1, ifp) != 1)
    {
      fprintf(stderr, "Error in input-file.\n");
      exit(-1);
    }
  }
  //  End of Appendix.

  return EXIT_SUCCESS;
}