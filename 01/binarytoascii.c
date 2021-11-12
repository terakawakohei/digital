#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define Pi 3.14159265358979

int main(int argc, char **argv)
{
    short check_flag_x, data_x, *inp_data_x;
    float check_flag_h, data_h, *inp_data_h;
    int i, size_data_x, size_data_h;
    FILE *file_x, *file_h, *outfile_x, *outfile_h, *amplitude_x, *outfile_y, *amplitude_h, *amplitude_y, *outfile_y_DFT;

    //ファイルが開けるか確認
    if ((file_x = fopen(argv[1], "rb")) == NULL)
    { // open the binary file.
        fprintf(stderr, "Cannot open file: %s\n", argv[1]);
        exit(EXIT_FAILURE);
    }
    if ((file_h = fopen(argv[2], "rb")) == NULL)
    { // open the binary file.
        fprintf(stderr, "Cannot open file: %s\n", argv[2]);
        exit(EXIT_FAILURE);
    }

    if ((outfile_x = fopen(argv[3], "w")) == NULL)
    {
        fprintf(stderr, "Cannot write file: %s\n", argv[3]);
        exit(EXIT_FAILURE);
    }
    if ((outfile_h = fopen(argv[4], "w")) == NULL)
    {
        fprintf(stderr, "Cannot write file: %s\n", argv[4]);
        exit(EXIT_FAILURE);
    }
    if ((amplitude_x = fopen(argv[5], "w")) == NULL)
    {
        fprintf(stderr, "Cannot write file: %s\n", argv[5]);
        exit(EXIT_FAILURE);
    }
    if ((outfile_y = fopen(argv[6], "w")) == NULL)
    {
        fprintf(stderr, "Cannot write file: %s\n", argv[6]);
        exit(EXIT_FAILURE);
    }
    if ((amplitude_h = fopen(argv[7], "w")) == NULL)
    {
        fprintf(stderr, "Cannot write file: %s\n", argv[7]);
        exit(EXIT_FAILURE);
    }
    if ((amplitude_y = fopen(argv[8], "w")) == NULL)
    {
        fprintf(stderr, "Cannot write file: %s\n", argv[8]);
        exit(EXIT_FAILURE);
    }
    if ((outfile_y_DFT = fopen(argv[9], "w")) == NULL)
    {
        fprintf(stderr, "Cannot write file: %s\n", argv[9]);
        exit(EXIT_FAILURE);
    }

    check_flag_x = 0;
    size_data_x = 0;

    while (1)
    {
        if (fread(&data_x, sizeof(short), 1, file_x) != 1) //file_x(inputfile)からshort単位で1このデータを読み込み、dataに格納。返り血は読み取った要素の数なので1になるはず)
        {
            check_flag_x = 1;
        }
        if (check_flag_x == 1)
            break;

        fprintf(outfile_x, "%d,%d\n", size_data_x, data_x); //outfileにdataを一つずつ書き出す

        size_data_x++;
    }
    check_flag_h = 0;
    size_data_h = 0;

    while (1)
    {
        if (fread(&data_h, sizeof(float), 1, file_h) != 1) //file_x(inputfile)からshort単位で1このデータを読み込み、dataに格納。返り血は読み取った要素の数なので1になるはず)
        {
            check_flag_h = 1;
        }
        if (check_flag_h == 1)
            break;

        fprintf(outfile_h, "%d,%f\n", size_data_h, data_h); //outfileにdataを一つずつ書き出す

        size_data_h++;
    }
    //  End.

    // Appendix.
    inp_data_x = malloc(sizeof(short) * size_data_x); // Allocate memory.
    inp_data_h = malloc(sizeof(float) * size_data_h); // Allocate memory.
    fseek(file_x, 0, SEEK_SET);                       // You can read the data file again.
    fseek(file_h, 0, SEEK_SET);

    for (i = 0; i < size_data_x; i++)
    {
        if (fread(&inp_data_x[i], sizeof(short), 1, file_x) != 1)
        {
            fprintf(stderr, "Error in input-file at file-x.\n");
            exit(-1);
        }
    }

    for (i = 0; i < size_data_h; i++)
    {
        if (fread(&inp_data_h[i], sizeof(float), 1, file_h) != 1)
        {
            fprintf(stderr, "Error in input-file at file-h.\n");
            exit(-1);
        }
        printf("%f\n", inp_data_h[i]);
    }

    //  End of Appendix.

    printf("datasize_x=%d\n", size_data_x);
    printf("datasize_h=%d\n", size_data_h);

    //x[n]の振幅スペクトルを求める

    int N = size_data_x;

    short X_r[N], X_i[N];
    short *x;
    float *h;

    x = inp_data_x;
    h = inp_data_h;

    printf("h=%f\n", h);

    for (int k = 0; k < N - 1; k++)
    {
        //初期化
        X_r[k] = 0;
        X_i[k] = 0;

        for (int n = 0; n < N - 1; n++)
        {
            X_r[k] += x[n] * cos(2 * Pi * k * n / N);
            X_i[k] += (-1) * x[n] * sin(2 * Pi * k * n / N);
        }
    }
    long X_abs[N];

    for (int k = 0; k < N - 1; k++)
    {
        X_abs[k] = 0;

        X_abs[k] = (long)sqrt(X_r[k] * X_r[k] + X_i[k] * X_i[k]);

        if (X_abs[k] > 5000)
        {
            printf("k=%d,X_abs=%d\n", k, X_abs[k]);
        }
        fprintf(amplitude_x, "%d,%d\n", k, X_abs[k]);
    }

    //畳み込みでy[n]を求める

    float y[N];
    short tmp;

    for (int n = 0; n < N - 1; n++)
    {

        y[n] = 0;
        for (int k = 0; k < 32; k++)
        {

            y[n] += h[k] * x[n - k];
        }
        tmp = (short)y[n];
        fwrite(&tmp, sizeof(short), 1, outfile_y);
    }

    //hの振幅スペクトルを求める

    float H_r[N], H_i[N];

    for (int k = 0; k < N - 1; k++)
    {
        //初期化
        H_r[k] = 0.0;
        H_i[k] = 0.0;
        if (k >= 31)
            h[k] = 0;

        for (int n = 0; n < N - 1; n++)
        {
            H_r[k] += h[n] * cos(2 * Pi * k * n / N);
            H_i[k] += (-1) * h[n] * sin(2 * Pi * k * n / N);
        }
    }
    float H_abs[N];

    for (int k = 0; k < N - 1; k++)
    {
        H_abs[k] = 0;

        H_abs[k] = (float)sqrt(H_r[k] * H_r[k] + H_i[k] * H_i[k]);

        fprintf(amplitude_h, "%d,%f\n", k, H_abs[k]);
    }

    //xとhにDFTを行い、周波数領域で畳み込みを行い逆DFTでyを求める

    float Y_r[N], Y_i[N];
    tmp = 0;

    for (int n = 0; n < N - 1; n++)
    {
        Y_r[n] = 0;
        Y_i[n] = 0;

        Y_r[n] = X_r[n] * H_r[n] - X_i[n] * H_i[n];
        Y_i[n] = X_r[n] * H_i[n] + X_i[n] * H_r[n];

        if (n < 20)
            printf("R=%f,I=%f\n", Y_r[n], Y_i[n]);
    }

    float Y_abs[N];

    for (int k = 0; k < N - 1; k++)
    {
        Y_abs[k] = 0;

        Y_abs[k] = (float)sqrt(Y_r[k] * Y_r[k] + Y_i[k] * Y_i[k]);

        fprintf(amplitude_y, "%d,%f\n", k, Y_abs[k]);
    }

    float y_DFT[N];
    for (int n = 0; n < N - 1; n++)
    {
        y_DFT[n] = 0;
        for (int k = 0; k < N - 1; k++)
        {

            y_DFT[n] += (Y_r[k] * cos(2 * Pi * k * n / N) - Y_i[k] * sin(2 * Pi * k * n / N));
        }

        tmp = (short)y_DFT[n] / N;

        fwrite(&tmp, sizeof(short), 1, outfile_y_DFT);
    }

    return EXIT_SUCCESS;
}