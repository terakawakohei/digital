#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define Pi 3.14159265358979

int length;
float *data;
int samp_freq;

int next; //異なる関数からdataに連続して書き込めるよう、dataの最後の位置を記録しておく

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

//write()関数
//書き込む時間の長さ:timeと書き込む周波数:fを引数にもつ
//グローバル変数のdataに書き込み、終了時には同じくグローバル変数で用意したnextに書き込み終了位置を記す
void write(float time, float f)
{

    double a = 2000;
    int scale_length = (int)(time * samp_freq);
    int end = next;

    for (int n = next + 1; n < scale_length + next; n++)
    {
        data[n] = a * sin(2.0 * Pi * f * n / samp_freq);
        end++;
    }

    printf("f=%f,next=%d,end=%d\n", f, next, end);

    next = end + 1;
}
//write_overtone()関数
//書き込む時間の長さ:timeと書き込む周波数:fを引数にもつ
//グローバル変数のdataに書き込み、終了時には同じくグローバル変数で用意したnextに書き込み終了位置を記す
//オルガンのような音色
void write_overtone(float time, float f)
{

    double a = 2000;
    int scale_length = (int)(time * samp_freq);
    int end = next;

    for (int n = next + 1; n < scale_length + next; n++)
    {
        data[n] = a * (0.5 * sin(2.0 * Pi * f * n / samp_freq) + 0.1 * sin(2.0 * Pi * f * 2 * n / samp_freq) + 0.4 * sin(2.0 * Pi * f * 3 * n / samp_freq));
        end++;
    }

    // printf("f=%f,next=%d,end=%d\n", f, next, end);

    next = end + 1;
}
//write_overtone2()関数
//書き込む時間の長さ:timeと書き込む周波数:fを引数にもつ
//グローバル変数のdataに書き込み、終了時には同じくグローバル変数で用意したnextに書き込み終了位置を記す
//レトロゲームのような音色
void write_overtone2(float time, float f)
{

    double a = 2000;
    int scale_length = (int)(time * samp_freq);
    int end = next;

    for (int n = next + 1; n < scale_length + next; n++)
    {
        data[n] = a * (0.1 * sin(2.0 * Pi * f * n / samp_freq) + 0.2 * sin(2.0 * Pi * f * 2 * n / samp_freq) + 0.7 * sin(2.0 * Pi * f * 3 * n / samp_freq));
        end++;
    }

    // printf("f=%f,next=%d,end=%d\n", f, next, end);

    next = end + 1;
}

int main(int argc, char **argv)
{
    int n;
    short tmp;
    float time;
    double a, f0;

    samp_freq = 44110; // Hz
    time = 18;         // second、
    a = 2000;
    f0 = 500; // Hz

    length = (int)(time * samp_freq);
    data = calloc(length, sizeof(float));

    //各音階の周波数を用意
    double C4 = 261.63;
    double C_4 = 277.18;
    double D4 = 293.66;
    double D_4 = 311.13;
    double E4 = 329.63;
    double F4 = 349.23;
    double F_4 = 369.99;
    double G4 = 392.00;
    double G_4 = 415.30;
    double A4 = 440.00;
    double A_4 = 466.16;
    double B4 = 493.88;

    double B3 = 254.178;
    double A3 = 226.446;

    next = 0;

    //音の切れ目はwrite(t, 0);で表現

    write(0.3, G4); //き
    write(0.3, C4); //み
    write(0.3, D4); //と
    write(0.5, E4); //で

    write(0.05, 0);

    write(0.7, E4); //あ

    write(0.07, 0);

    write(0.3, D4); //あ
    write(0.1, 0);
    write(0.3, E4); //た

    write(0.1, 0);

    write(0.5, F4); //き
    write(0.05, 0);
    write(0.7, E4); //せ

    write(0.2, 0);

    write(0.2, C4); //き

    write(0.2, 0);

    write(0.4, C4); //が

    write(0.8, 0);

    write_overtone(0.3, A4); //こ

    write_overtone(0.4, 0);

    write_overtone(0.3, A4); //の

    write_overtone(0.4, 0);

    //む

    write_overtone(0.3, C4); //ね
    write_overtone(0.15, 0);
    write_overtone(0.3, D4); //に

    write_overtone(0.2, 0);

    write_overtone(0.2, A4); //あ
    write_overtone(0.2, 0);
    write_overtone(0.1, A4); //ふ
    write_overtone(0.3, 0);
    write_overtone(0.1, G4); //れ
    write_overtone(0.3, 0);
    write_overtone(0.1, E4); //て
    write_overtone(0.3, 0);
    write_overtone(0.7, G4); //る

    write_overtone2(0.2, F4); //き
    write_overtone2(0.2, 0);
    write_overtone2(0.2, G4); //と
    write_overtone2(0.1, 0);
    write_overtone2(0.4, A4); //い
    write_overtone2(0.2, 0);
    write_overtone2(0.2, D4); //ま
    write_overtone2(0.1, 0);
    write_overtone2(0.2, D4); //は
    write_overtone2(0.3, 0);
    write_overtone2(0.2, G4); //じ
    write_overtone2(0.1, 0);
    write_overtone2(0.4, G4); //ゆ
    write_overtone2(0.1, 0);
    write_overtone2(0.2, C4); //う
    write_overtone2(0.1, 0);
    write_overtone2(0.2, C4); //に

    write(0.2, 0);

    write_overtone2(0.2, C4); //そ
    write_overtone2(0.1, 0);
    write_overtone2(0.2, B3); //ら
    write_overtone2(0.1, 0);
    write_overtone2(0.4, A3); //も
    write_overtone2(0.1, 0);
    write_overtone2(0.2, B3); //と
    write_overtone2(0.1, 0);
    write_overtone2(0.5, C4); //べ
    write_overtone2(0.1, 0);
    write_overtone2(0.2, E4); //る
    write_overtone2(0.1, 0);
    write_overtone2(0.2, C4); //は
    write_overtone2(0.1, 0);
    write_overtone2(0.7, D4); //ず

    //実行時に与えた引数をファイルネームとして書き込む
    write_wav(argv[1]);
}