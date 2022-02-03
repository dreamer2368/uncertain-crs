clear all
close all
clc

u0 = 2;
x = [0; 0];
y = u0 * [1; -1];
s1 = 0.5; s2 = 0.5;

nk = 1000;
K = linspace(0,10,nk);
logP = zeros(nk,1);
S = logP;
ym = logP; vm = logP;
for n = 1:nk
    cov = [K(n) + s1 K(n); K(n) K(n) + s2];
    Kp = K(n) * [1; 1];
    ym(n) = Kp' * (cov\y);
    vm(n) = K(n) - Kp' * ( cov\Kp );

%     logP(n) = - 0.5 * y' * (cov \ y) - log(2.0*pi) - 0.5 * log(det(cov));
%     S(n) = - logP(n) * exp(logP(n));
end

figure(1)
plot(K,ym,'-k');
figure(2)
plot(K,vm,'-k');
% figure(1)
% plot(K,S,'-r');
% 
% figure(2)
% plot(K,logP,'-r');

% [M, I] = max(S);
% K(I)

% Y = linspace(-3*u0, 3*u0, nk);
% pp = exp()
% figure(2)

