#ifndef HARD_SPHERE_DOT_H    /* This is an "include guard" */
#define HARD_SPHERE_DOT_H    /* prevents the file from being included twice. */

/* Percus-Yevick approx Functions */
double ck_hs_py( const double phi, const double k );
double is_hs_py( const double phi, const double k );
double sk_hs_py( const double phi, const double k );

/* Percus-Yevick + Verlet Weis correction approx Functions */
double ck_hs_vw( const double phi, const double k );
double is_hs_vw( const double phi, const double k );
double sk_hs_vw( const double phi, const double k );

/* Percus-Yevick + Verlet Weis + blip function correction approx Functions */
double ck_hs_vw_blip( const double phi, const double T, const double k );
double is_hs_vw_blip( const double phi, const double T, const double k );
double sk_hs_vw_blip( const double phi, const double T, const double k );

#endif /* HARD_SPHERE_DOT_H */
