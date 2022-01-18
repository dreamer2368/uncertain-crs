clear all
close all
clc

%% generate data

N = 30; L=0.4; noise = 0.7;
x = linspace(0,1,N)';
y = sin(2*pi*x/L) .* ( 1 + noise * randn(N,1) );
ymean = mean(y); ydev = y - ymean;
xd2 = kron(x,ones(1,length(x))) - kron( ones(length(x),1), x' );
xd2 = xd2 .^ 2;

figure(1)
plot(x,y,'x');

%% checking gradient
theta_ref = [1; 0.1];
[f,g] = log_likelihood_with_grad(theta_ref, xd2, ydev);
% K = kernel(x,x,theta_ref);
%%
gg = g' * g;

Nt = 20;
ak = linspace(-12,2,Nt); ak = 10.^ak;
ak = ak / sqrt(gg);
ek = zeros(Nt,1); gradk = ek;
for k = 1:Nt
    thetak = theta_ref + g * ak(k);
    fk = log_likelihood_with_grad(thetak, xd2, ydev);
    gradk(k) = (fk - f) / ak(k);
    ek(k) = abs( gradk(k) - gg ) / abs(gg);
end

figure(1)
loglog(ak, ek,'o');

%% functions

function [f,g] = log_likelihood_with_grad(theta, xd2, ydev)

    expTerm = exp( - xd2 / theta(2) );
    K = theta(1) * expTerm;
    temp1 = K \ ydev;
    f = - 0.5 * ydev' * temp1;

    g = zeros(2,1);
    g(1) = - 0.5 * ydev' * ( - K \ (expTerm * temp1) );
    g(2) = - 0.5 * ydev' * ( - K \ ( (-xd2/theta(2)/theta(2).*expTerm) * temp1 ) );
end

function K = kernel(x,x2,theta)
    var = theta(1); scale = theta(2);
%     K = sparse(zeros(length(x),length(x2)));
    xd = kron(x,ones(1,length(x2))) - kron( ones(length(x),1), x2' );
    K = var * exp( - xd.^2 / scale );
end