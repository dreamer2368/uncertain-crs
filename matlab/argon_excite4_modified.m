function crs = argon_excite4_modified(theta,E)
    F0 = theta(1); beta = theta(2);
    C1 = theta(3); alpha0 = theta(4);
    run constants;

    v2 = qe * E * 2.0 / me;
    beta2 = v2 / c0 / c0;
    rel_factor = log(beta2 ./ (1.0 - beta2) * mc2 / 2.0 / E0 * C1) - beta2;
    crs = 4. * pi * a0 * a0 * R0 ./ E * F0 / E0 .* rel_factor .* ( 1.0 - (E0./E).^alpha0 ) .^ beta;
end