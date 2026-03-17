#ifndef STICKY_HARD_SPHERE_DOT_H    /* This is an "include guard" */
#define STICKY_HARD_SPHERE_DOT_H    /* prevents the file from being included twice. */

/* Percus-Yevick approx Functions */
double ISSHS_MC(double k, double τ, double ϕ);
double sk_shs_py( const double phi,const double tau ,const double k );

#endif /* STICKY_HARD_SPHERE_DOT_H */
