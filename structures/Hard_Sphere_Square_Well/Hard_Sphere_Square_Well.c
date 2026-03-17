#include "Hard_Sphere_Square_Well.h"

/*
Function: Auxiliary function that computes for the FT of the perturbation potential -\beta u_p(k)
System: Square Well
Inputs:
  -T* = Dimensionless temperature / Domain (0:\infty)
  -lambda range of the well in terms of the diameter sigma (1:infty)
  -k: wave vector magnitude / type double / Domain [0:infty)
Outputs:
  --\beta u_p(k): FT of the perturbation well
*/

double sw_m_beta_uk( const double T, const double lambda, const double k ){
  double c_aux;
  double k2,lk,l5,l3,coslk,sinlk,sink,cosk;
  k2 = k * k;
  if (k > 0.0750) {
    lk = lambda * k ;
    sink  = gsl_sf_sin( k );
    cosk  = gsl_sf_cos( k );
    sinlk = gsl_sf_sin( lk );
    coslk = gsl_sf_cos( lk );
    c_aux = ((cosk - lambda * coslk) / k) + ((sinlk - sink) / k2) ;
    c_aux = c_aux / k ;
  }
  else {
    l3 = lambda * lambda * lambda;
    l5 = l3 * lambda * lambda;
    c_aux = (1.0/3.0) * (l3 - 1.0) - (1.0/30.0) * (l5 - 1.0) * k2;
  }
  //c_aux = 4.0 * M_PI * c_aux * (exp(1.0/T)-1.0);
  c_aux = 4.0 * M_PI * c_aux / T;
  return c_aux;
  }

/*
Function: FT Direct correlation function
System: Hard Sphere + Square Well
Approximation: Verlet-Weiss + Sharma-Sharma
Inputs:
  -phi: Volume fraction / type double / Domain (0:1)
  -T* = Dimensionless temperature / Domain (0:\infty)
  -lambda range of the well in terms of the diameter sigma / Domain (1:infty)
  -k: wave vector magnitude / type double / Domain [0:infty)
Outputs:
  -c: FT direct correlation / type double / Range NA
*/
double ck_hssw_vwsh( const double phi, const double T, const double lambda, const double k ) {
  double c, chs;
  chs = ck_hs_vw(phi,k);
  c = chs + sw_m_beta_uk( T, lambda, k );
  return c;
}

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
double is_hssw_vwsh( const double phi, const double T, const double lambda, const double k ){
  double is, phi_vw,chs;
  phi_vw = phi*(1.0-(phi/16.0)); 
  chs = ck_hs_vw(phi,k);
  is = (phi_vw*chs) + (phi * sw_m_beta_uk(T,lambda,k));
  is = 1.0 - 6.0 * is / M_PI;
  return is;
}

/*
Function: Static structure factor
System: Hard Sphere
Approximation: Mean Shperical Approximaiton (MSA)
Inputs:
  -phi: Volume fraction / type double / Domain (0:1)
  -k: wave vector magnitude / type double / Domain [0:infty)
Outputs:
  -s: Static structure factor / type double / Range [0:infty)
*/
double sk_hssw_vwsh( const double phi, const double T, const double lambda, const double k ){
  double s;
  s = 1.0 / is_hssw_vwsh(phi, T, lambda, k );
  return s;
}

double ISWS( double phi, double T, double d, double k) {
    double K = d / T;
    double n = (6.0 / M_PI) * phi;

    double a0 = (1 + 2 * phi) / pow((1 - phi), 2) - (12 * K * phi) / (1 - phi);
    double b0 = (-3 * phi) / (2 * pow((1 - phi), 2)) + (6 * K * phi) / (1 - phi);
    double c0 = (-1) / (2 * (1 - phi)) + K;

    double a1 = (6 * phi * (5 * phi - 2) - 72 * c0 * phi * phi * (1 - phi)) / pow((1 - phi), 2);
    double b1 = (9 * phi * (1 - 2 * phi) + 36 * c0 * phi * phi * (1 - phi)) / pow((1 - phi), 2);
    double c1 = (1 - 7 * phi + 12 * c0 * phi * (1 - phi)) / (2 * (1 - phi));

    double a = a0 + K * d * a1;
    double b = b0 + K * d * b1;
    double c = c0 + K * d * c1;
 
    double complex A = (cexp(I * d * k) * (24 * K * K * phi + d * d * k * (-I * k * k * (d * (a * d + 2 * b) + 2 * c) + 2 * k * (a * d + b) + 2 * I * a)) + 2 * I * d * d * k * (-a + k * (c * k + I * b)) + 4 * K * K * phi * (-6 + d * k * (d * k * (3 + I * d * k) - 6 * I))) / (2 * d * d * k * k * k * k);

    double complex B = (I * cexp(I * d * k) * (k * k * (d * (a * d + 2 * b) + 2 * c) + 2 * I * k * (a * d + b) - 2 * a) - I * cexp(I * k) * (k * k * (a + 2 * (b + c)) + 2 * I * k * (a + b) - 2 * a)) / (2 * k * k * k);

    double complex C = (cexp(I * k) * K * (12 * I * c0 * phi * (d * d * k * k - 2 * I * d * k + 2 * cexp(I * d * k) - 2) + I * d * (d + 2) * k * k - 2 * cexp(I * d * k) * (d * k + k + I) + 2 * k + 2 * I)) / (2 * d * k * k * k);

    double complex D = A + B + C;
    double complex Q = 1 - 2 * M_PI * n * D;
    double IS = creal(Q * conj(Q));
    //printf("Q = %.2f + %.2fi %1.9e \n", creal(Q), cimag(Q), k);
    return IS;
}


double sk_hssw_msa( const double phi, const double T, const double delta, const double k ){
  double s;
  s = 1.0 / ISWS(phi, T,delta, k);
  return s;
}


