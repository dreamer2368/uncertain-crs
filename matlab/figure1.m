clear all
close all
clc

N = 300;
x = linspace(-3,3,N); dx = x(2) - x(1);
x1 = -0.1; x2 = 0.1;
s1 = 0.1; s2 = 0.1;

p1 = 1 / sqrt(2*pi) / s1 * exp( - (x-x1).^2 / 2 / s1 / s1 );
p2 = 1 / sqrt(2*pi) / s2 * exp( - (x-x2).^2 / 2 / s2 / s2 );

p1p2 = p1 .* p2; p1p2 = p1p2 / sum(p1p2) / dx;

xs = 0.5 * (x1 + x2);
ss = sqrt( 0.5 * (s1*s1 + s2*s2) + (0.5*(x2-x1)).^2 );
ps = 1 / sqrt(2*pi) / ss * exp( - (x-xs).^2 / 2 / ss / ss );

figure(1)
% plot(x,0.5 * (p1 + p2),'-k','linewidth',1);
plot(x,0.5 * p1,'-k','linewidth',1);
hold on
plot(x,p1p2,'-r','linewidth',1);
plot(x,p1.*p2,'--g','linewidth',2);
plot(x,0.5 * p2,'-k','linewidth',1);
hold off
axis([-3 3 -0.5 6]);
xlabel('$\theta$','interpreter','latex');
ylabel('$P(\theta)$','interpreter','latex');
h = legend('$\frac{P_1}{2}$, $\frac{P_2}{2}$','$\sim P_1\times P_2$','$P_1\times P_2$');
set(h,'interpreter','latex');
set(gca,'fontsize',25,'ticklabelinterpreter','latex');

figure(2)
plot(x,0.5 * (p1 + p2),'-k','linewidth',1);
hold on
plot(x,p1p2,'-r','linewidth',1);
plot(x,ps,'-b','linewidth',1);
hold off
axis([-3 3 -0.5 6]);
xlabel('$\theta$','interpreter','latex');
ylabel('$P(\theta)$','interpreter','latex');
h = legend('$\frac{P_1 + P_2}{2}$','$\sim P_1\times P_2$','$P_N$');
set(h,'interpreter','latex');
set(gca,'fontsize',25,'ticklabelinterpreter','latex');