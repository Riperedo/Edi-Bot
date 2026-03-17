#include <stdio.h>
#include <math.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_sf_trig.h>

/*
Function: Inverse of static structure factor
System: Hard Sphere
Approximation: Percus Yevick
Inputs:
  -phi: Volume fraction / type double / Domain (0:1)
  -k: wave vector magnitude / type double / Domain [0:infty)
Outputs:
  -is: Inverse of static structure factor / type double / Range (0:infty)
*/
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

double ISSHS_MC(double k, double tau, double phi) {
    double lm1,lm2,c,b,a,discriminant;
    c = (1.0 + 0.5 * phi) / pow((1.0 - phi), 2);
    b = (phi / (1.0 - phi)) + tau;
    a = phi / 12.0;

    discriminant = b * b - 4.0 * a * c;
    lm1 = (b + sqrt(discriminant)) / (2.0 * a);
    lm2 = (b - sqrt(discriminant)) / (2.0 * a);
    
    double lambda = fmin(lm1, lm2);
    double sigma = 1.0;
    double mu = lambda * phi * (1.0 - phi);
    
    double A = 0.5 * (1.0 + 2.0 * phi - mu) / pow((1.0 - phi), 2);
    double B = sigma * (-3.0 * phi + mu) / (2.0 * pow((1.0 - phi), 2));

    double cosk = cos(k);
    double sink = sin(k);

    double alpha = 1.0 - ((12.0 * phi) / pow(k, 3)) * (2.0 * A * (k * cosk - sink) + (B / sigma) * k * (cosk - 1.0) + (lambda * pow(k, 2) / 12.0) * sink);
    double beta = (12.0 * phi / pow(k, 3)) * (2.0 * A * (k * sink + cosk - 1.0 - pow(k, 2) / 2.0) + (B / sigma) * k * (sink - k) + (lambda * pow(k, 2) / 12.0) * (1.0 - cosk));

    double is = pow(alpha, 2) + pow(beta, 2);
    return is;
}


/*
Function: Static structure factor
System: Hard Sphere
Approximation: Percus Yevick
Inputs:
  -phi: Volume fraction / type double / Domain (0:1)
  -k: wave vector magnitude / type double / Domain [0:infty)
Outputs:
  -s: Static structure factor / type double / Range [0:infty)
*/
double sk_shs_py( const double phi,const double tau ,const double k ){
  double s;
  s = 1.0 / ISSHS_MC(k, tau, phi);
  return s;
}

/*
Function: FT Direct correlation function
System: Hard Sphere
Approximation: Percus Yevick + Verlet Weis
Ref: doi=10.1103/PhysRevA.5.939
Inputs:
  -phi: Volume fraction / type double / Domain (0:1)
  -k: wave vector magnitude / type double / Domain [0:infty)
Outputs:
  -c: FT direct correlation / type double / Range NA
*/
