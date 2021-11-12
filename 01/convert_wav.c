#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define Pi 3.14159265358979

int length;
float *data;
int samp_freq;

void write_wav(char *filename)
{
    short tmp_short;
    int i;
    char s[4];
    short channel, var_short;
    int x, file_size;
    FILE *file_output;

    // file open
    if ((file_output = fopen(filename, "wb")) == NULL)
    {
        fprintf(stderr, "Cannot write %s\n", filename);
        exit(-1);
    }
    // output header info.
    s[0] = 'R';
    s[1] = 'I';
    s[2] = 'F';
    s[3] = 'F';
    fwrite(s, 1, 4, file_output);

    // filesize
    x = length * 2 + 36; // 16 bit = 2 byte
    fwrite(&x, 4, 1, file_output);

    // WAVE
    s[0] = 'W';
    s[1] = 'A';
    s[2] = 'V';
    s[3] = 'E';
    fwrite(s, 1, 4, file_output);

    // chunkID
    s[0] = 'f';
    s[1] = 'm';
    s[2] = 't';
    s[3] = ' ';
    fwrite(s, 1, 4, file_output);

    //
    x = 16;
    fwrite(&x, 4, 1, file_output);

    //
    tmp_short = 1;
    fwrite(&tmp_short, 2, 1, file_output);

    //
    channel = 1;
    fwrite(&channel, 2, 1, file_output);

    //
    fwrite(&samp_freq, 4, 1, file_output);

    //
    x = 2 * channel * samp_freq;
    fwrite(&x, 4, 1, file_output);

    //
    var_short = 2 * channel;
    fwrite(&var_short, 2, 1, file_output);

    // bit/sample
    var_short = 16;
    fwrite(&var_short, 2, 1, file_output);

    //
    s[0] = 'd';
    s[1] = 'a';
    s[2] = 't';
    s[3] = 'a';
    fwrite(s, 1, 4, file_output);

    //
    file_size = length * 2 * channel;
    fwrite(&file_size, 4, 1, file_output);

    // end of header info.
    //これまでで44byteの書き込みが行われているはず、そうでなければエラー
    if (ftell(file_output) != 44)
    {
        fprintf(stderr, "%s: wav header error.\n", filename);
    }

    // output data.
    for (i = 0; i < length; i++)
    {
        tmp_short = (short)data[i];
        fwrite(&tmp_short, sizeof(short), 1, file_output);
    }

    fclose(file_output);

    return;
}

int main(int argc, char **argv)
{

    float check_flag, *inp_data;
    int size_data;
    FILE *input_file;

    if ((input_file = fopen(argv[2], "rb")) == NULL)
    { // open the binary file.
        fprintf(stderr, "Cannot open file: %s\n", argv[2]);
        exit(EXIT_FAILURE);
    }
    check_flag = 0;
    size_data = 0;

    while (1)
    {
        if (fread(&inp_data, sizeof(float), 1, input_file) != 1) //file_x(inputfile)からshort単位で1このデータを読み込み、dataに格納。返り血は読み取った要素の数なので1になるはず)
        {
            check_flag = 1;
        }
        if (check_flag == 1)
            break;

        size_data++;
    }

    int n;
    short tmp;
    float time;
    double a, f0;

    samp_freq = 8000; // Hz
    time = 2;         // second
    a = 1000;
    f0 = 500; // Hz

    length = (int)(time * samp_freq);
    data = calloc(length, sizeof(float));

    float tmp_double;
    for (n = 0; n < length; n++)
    {

        data[n] = (short)inp_data[n];
    }
    //実行時に与えた引数をファイルネームとして書き込み開始
    write_wav(argv[1]);
}