#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "../../structures/Hard_Sphere/Hard_Sphere.h"
#include "../../structures/Hard_Sphere_Double_Yukawa/Hard_Sphere_Double_Yukawa.h"

// Definición de modelos de potencial
typedef enum {
    MODELO_YUKAWA = 1,
    MODELO_HS = 2,
    MODELO_YUKAWA_ATRACTIVO = 3,
    MODELO_DOBLE_YUKAWA = 4,
    MODELO_HS_VW = 5,
    MODELO_WCA = 6
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
    double Tf;     // Fluid Temperature (used for WCA/Blip)
} Parametros;

// Declaración de funciones físicas simuladas (a sustituir por la paquetería real)
double calcular_Sq_Yukawa(double q, double phi, double carga, double sigma) {
    double q_scaled = q * sigma;
    return 1.0 + (phi * carga) * sin(q_scaled) / q_scaled; 
}

double calcular_Sq_HS(double q, double phi, double sigma) {
    double q_scaled = q * sigma;
    return sk_hs_py(phi, q_scaled);
}


// Función principal
int main(int argc, char *argv[]) {
    // Variables para el parseo de argumentos
    Parametros params = {MODELO_YUKAWA, 0.1, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0}; 
    char *input_file = NULL;

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--modelo") == 0 && i + 1 < argc) {
            if (strcmp(argv[i+1], "yukawa") == 0) params.modelo = MODELO_YUKAWA;
            else if (strcmp(argv[i+1], "hs") == 0) params.modelo = MODELO_HS;
            else if (strcmp(argv[i+1], "yukawa_atractivo") == 0) params.modelo = MODELO_YUKAWA_ATRACTIVO;
            else if (strcmp(argv[i+1], "doble_yukawa") == 0) params.modelo = MODELO_DOBLE_YUKAWA;
            else if (strcmp(argv[i+1], "hs_vw") == 0) params.modelo = MODELO_HS_VW;
            else if (strcmp(argv[i+1], "wca") == 0) params.modelo = MODELO_WCA;
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
        } else if (strcmp(argv[i], "--Tf") == 0 && i + 1 < argc) {
            params.Tf = atof(argv[++i]);
        } else if (strcmp(argv[i], "--input") == 0 && i + 1 < argc) {
            input_file = argv[++i];
        }
    }

    if (input_file == NULL) {
        fprintf(stderr, "Error: Debe especificar el archivo de entrada con --input <archivo>\n");
        return 1;
    }

    FILE *fp = fopen(input_file, "r");
    if (!fp) {
        fprintf(stderr, "Error abriendo archivo input: %s\n", input_file);
        return 1;
    }

    int q_size = 0;
    double q_val;
    while (fscanf(fp, "%lf", &q_val) == 1) {
        q_size++;
    }
    
    double *q_exp = (double*)malloc(q_size * sizeof(double));
    rewind(fp);
    for(int i = 0; i < q_size; i++) {
        fscanf(fp, "%lf", &q_exp[i]);
    }
    fclose(fp);

    for (int i = 0; i < q_size; i++) {
        double sq_calc = 0.0;
        
        if (params.modelo == MODELO_YUKAWA) {
            sq_calc = calcular_Sq_Yukawa(q_exp[i], params.phi, params.carga, params.sigma);
        } else if (params.modelo == MODELO_HS) {
            sq_calc = calcular_Sq_HS(q_exp[i], params.phi, params.sigma);
        } else if (params.modelo == MODELO_YUKAWA_ATRACTIVO) {
            sq_calc = sk_dble_yukawa_vwsh(params.phi, params.Ta, 0.0, params.za, 0.0, q_exp[i] * params.sigma);
        } else if (params.modelo == MODELO_DOBLE_YUKAWA) {
            sq_calc = sk_dble_yukawa_vwsh(params.phi, params.Ta, params.Tr, params.za, params.zr, q_exp[i] * params.sigma);
        } else if (params.modelo == MODELO_HS_VW) {
            sq_calc = sk_hs_vw(params.phi, q_exp[i] * params.sigma);
        } else if (params.modelo == MODELO_WCA) {
            sq_calc = sk_hs_vw_blip(params.phi, params.Tf, q_exp[i] * params.sigma);
        }

        printf("%lf\n", sq_calc);
    }

    free(q_exp);
    return 0;
}
