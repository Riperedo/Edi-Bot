#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "../../structures/Hard_Sphere/Hard_Sphere.h"
#include "../../structures/Hard_Sphere_Double_Yukawa/Hard_Sphere_Double_Yukawa.h"

// Definición de modelos de potencial (ejemplo simplificado, expandible)
typedef enum {
    MODELO_YUKAWA = 1,
    MODELO_HS = 2,
    MODELO_YUKAWA_ATRACTIVO = 3,
    MODELO_DOBLE_YUKAWA = 4
} ModeloPotencial;

// Estructura para los parámetros del ajuste
typedef struct {
    ModeloPotencial modelo;
    double phi;
    double carga;  // Usado para Yukawa
    double sigma;  // Factor de escala (mapping del q)
    double Ta;     // Dimensioneless attractive temperature
    double Tr;     // Dimensioneless repulsive temperature
    double za;     // Range of attraction parameter
    double zr;     // Range of repulsion parameter
} Parametros;

// Declaración de funciones físicas simuladas (a sustituir por la paquetería real)
// Actualmente retornan una simulación sencilla de S(q) para poder probar el pipeline
double calcular_Sq_Yukawa(double q, double phi, double carga, double sigma) {
    // ESTO ES UN PLACEHOLDER MATEMATICO. 
    // Aquí deberá ir el enlace real a la librería de ecuaciones integrales SCGLE/MSA etc.
    double q_scaled = q * sigma;
    // Función oscilatoria de prueba simulando un S(q) genérico:
    return 1.0 + (phi * carga) * sin(q_scaled) / q_scaled; 
}

double calcular_Sq_HS(double q, double phi, double sigma) {
    // USANDO CÓDIGO FÍSICO REAL DESDE /structures
    double q_scaled = q * sigma;
    return sk_hs_py(phi, q_scaled);
}


// Función principal
int main(int argc, char *argv[]) {
    // Variables para el parseo de argumentos
    Parametros params = {MODELO_YUKAWA, 0.1, 1.0, 1.0}; // Valores default
    char *input_file = NULL;

    // Parseo por línea de comandos: 
    // Ejemplo: ./calcula_Sq --modelo yukawa --phi 0.15 --carga 3.2 --sigma 50.0 --input q_temp.txt
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--modelo") == 0 && i + 1 < argc) {
            if (strcmp(argv[i+1], "yukawa") == 0) params.modelo = MODELO_YUKAWA;
            else if (strcmp(argv[i+1], "hs") == 0) params.modelo = MODELO_HS;
            else if (strcmp(argv[i+1], "yukawa_atractivo") == 0) params.modelo = MODELO_YUKAWA_ATRACTIVO;
            else if (strcmp(argv[i+1], "doble_yukawa") == 0) params.modelo = MODELO_DOBLE_YUKAWA;
            i++;
        } else if (strcmp(argv[i], "--phi") == 0 && i + 1 < argc) {
            params.phi = atof(argv[++i]);
        } else if (strcmp(argv[i], "--carga") == 0 && i + 1 < argc) {
            params.carga = atof(argv[++i]);
        } else if (strcmp(argv[i], "--sigma") == 0 && i + 1 < argc) {
            params.sigma = atof(argv[++i]);
        } else if (strcmp(argv[i], "--Ta") == 0 && i + 1 < argc) {
            params.Ta = atof(argv[++i]);
        } else if (strcmp(argv[i], "--Tr") == 0 && i + 1 < argc) {
            params.Tr = atof(argv[++i]);
        } else if (strcmp(argv[i], "--za") == 0 && i + 1 < argc) {
            params.za = atof(argv[++i]);
        } else if (strcmp(argv[i], "--zr") == 0 && i + 1 < argc) {
            params.zr = atof(argv[++i]);
        } else if (strcmp(argv[i], "--input") == 0 && i + 1 < argc) {
            input_file = argv[++i];
        }
    }

    if (input_file == NULL) {
        fprintf(stderr, "Error: Debe especificar el archivo de entrada con --input <archivo>\n");
        return 1;
    }

    // Leemos los q_exp del archivo generado por Python
    FILE *fp = fopen(input_file, "r");
    if (!fp) {
        fprintf(stderr, "Error abriendo archivo input: %s\n", input_file);
        return 1;
    }

    int q_size = 0;
    double q_val;
    // Contamos primero el tamaño
    while (fscanf(fp, "%lf", &q_val) == 1) {
        q_size++;
    }
    
    // Asignamos memoria
    double *q_exp = (double*)malloc(q_size * sizeof(double));
    rewind(fp);
    for(int i = 0; i < q_size; i++) {
        fscanf(fp, "%lf", &q_exp[i]);
    }
    fclose(fp);

    // Calculamos e imprimimos directamente a stdout S(q_calc)
    // El formato limpio es necesario para que Python pueda parsearlo fácilmente
    for (int i = 0; i < q_size; i++) {
        double sq_calc = 0.0;
        
        if (params.modelo == MODELO_YUKAWA) {
            sq_calc = calcular_Sq_Yukawa(q_exp[i], params.phi, params.carga, params.sigma);
        } else if (params.modelo == MODELO_HS) {
            sq_calc = calcular_Sq_HS(q_exp[i], params.phi, params.sigma);
        } else if (params.modelo == MODELO_YUKAWA_ATRACTIVO) {
            // El modelo atractivo apaga las repulsiones enviando Tr=0 y zr=0.
            sq_calc = sk_dble_yukawa_vwsh(params.phi, params.Ta, 0.0, params.za, 0.0, q_exp[i] * params.sigma);
        } else if (params.modelo == MODELO_DOBLE_YUKAWA) {
            sq_calc = sk_dble_yukawa_vwsh(params.phi, params.Ta, params.Tr, params.za, params.zr, q_exp[i] * params.sigma);
        }

        printf("%lf\n", sq_calc);
    }

    free(q_exp);
    return 0;
}
