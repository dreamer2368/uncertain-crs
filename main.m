%% Momentum transfer - existing data and MERT theory
clear all
close all
clc

LXCats = {'Biagi','BSR','Hayashi','IST-Lisbon','Morgan','Phelps','Puech'};
Nsets = length(LXCats);

Exps = {'Gibson1996','Mielewska2004','Panajotovic1997','Srivastava1981'};
Nexps = length(Exps);

for k = 1:Nsets
    filename = strcat('./bolsig/crs/elastic-raw/',LXCats{k},'.raw.elastic.txt');
    elastic{k} = importdata(filename);
end

for k = 1:Nexps
    filename = strcat('./crs-exp/momentum/crs.',Exps{k},'.txt');
    el_exp{k} = importdata(filename);
end

f1 = figure(1);
Es = linspace(-3,2,200); Es = 10.^Es;
loglog(Es,MERT(Es),'-r','linewidth',2);
hold on
for k = [(1:Nsets-2) Nsets]
    s = scatter(elastic{k}(:,1),elastic{k}(:,2),'filled');%,'.','linewidth',2,'markersize',15);
    alpha(s,0.4);
end
for k = 1:Nexps
    s = scatter(el_exp{k}(:,1),el_exp{k}(:,2),'filled');%,'.','linewidth',2,'markersize',15);
    alpha(s,0.4);
end
hold off
% axis([1e-3 1e3 3e23 4e26]);
xlabel('$\epsilon$ ($eV$)','interpreter','latex');
ylabel('$\sigma_m(\epsilon)$ ($m^2$)','interpreter','latex');
% leg = {LXCats{1:Nsets-2} LXCats{Nsets}};
h=legend('MERT model','Datasets');
set(h,'interpreter','latex');
set(gca,'XScale','log','YScale','log','FontSize',20,'TickLabelInterpreter','latex');

%% ionization
clear all
close all
clc

E0 = 15.7596119;

Exps = {'Rapp1965','Straub1995','Wetzel1987'};
Nexps = length(Exps);

for k = 1:Nexps
    filename = strcat('./crs-exp/ionization/crs.',Exps{k},'.txt');
    ion_exp{k} = importdata(filename);
end

Nb = 1000;
fID = fopen('crs-Bayes1/crs.ionization.dat');
Aion = fread(fID,[3 Nb],'double')';
fclose(fID);

f1 = figure(1);
% Es = linspace(-3,2,200); Es = 10.^Es;
% loglog(Es,MERT(Es),'-r','linewidth',2);
% hold on
for k = 1:Nexps
    s = errorbar(ion_exp{k}(:,1)-E0,ion_exp{k}(:,2),ion_exp{k}(:,3),'.','linewidth',2,'markersize',10);
%     s = scatter(el_ion{k}(:,1),el_ion{k}(:,2),'filled');%,'.','linewidth',2,'markersize',15);
    aa = 0.5;
    set([s.Bar, s.Line], 'ColorType', 'truecoloralpha', 'ColorData', [s.Line.ColorData(1:3); 255*aa]);
    set(s.Cap, 'EdgeColorType', 'truecoloralpha', 'EdgeColorData', [s.Cap.EdgeColorData(1:3); 255*aa]);
    hold on
end
Ns = 300;
Es = linspace(-1,3,Ns);
Es = 10.^Es; Es = Es + E0;
for k = 1:Nb
    s=loglog(Es - E0,ion_BED(Aion(k,:),Es),'-','linewidth',3,'color',[0, 0, 1, 0.3]);
end
hold off
% axis([1e-3 1e3 3e23 4e26]);
xlabel('$\epsilon - \epsilon_{ion}$ ($eV$)','interpreter','latex');
ylabel('$\sigma_i(\epsilon)$ ($m^2$)','interpreter','latex');
leg = Exps;
leg{length(Exps)+1} = 'Sample models';
h=legend(leg);
set(h,'interpreter','latex');
set(gca,'XScale','log','YScale','log','FontSize',20,'TickLabelInterpreter','latex');

%% excitation level 4
clear all
close all
clc

E0 = 11.82807116;

Exps = {'Chutjian1981','Khakoo2004','Tsurubuchi1996','Li1988'};
Nexps = length(Exps);

for k = 1:Nexps
    filename = strcat('./crs-exp/excitation-level4/crs.',Exps{k},'.txt');
    exc_exp{k} = importdata(filename);
end

Nb = 1000;
fID = fopen('crs-Bayes1/crs.excitation.level4.dat');
Aexc = fread(fID,[2 Nb],'double')';
fclose(fID);

f1 = figure(1);
% Es = linspace(-3,2,200); Es = 10.^Es;
% loglog(Es,MERT(Es),'-r','linewidth',2);
% hold on
for k = 1:Nexps
    s = errorbar(exc_exp{k}(:,1)-E0,exc_exp{k}(:,2),exc_exp{k}(:,3),'.','linewidth',2,'markersize',10);
    aa = 0.5;
    set([s.Bar, s.Line], 'ColorType', 'truecoloralpha', 'ColorData', [s.Line.ColorData(1:3); 255*aa]);
    set(s.Cap, 'EdgeColorType', 'truecoloralpha', 'EdgeColorData', [s.Cap.EdgeColorData(1:3); 255*aa]);
    hold on
end
Ns = 300;
Es = linspace(0,3,Ns);
Es = 10.^Es; Es = Es + E0;
for k = 1:30
    s=loglog(Es - E0,excite_resonance(Aexc(k,:),Es),'-','linewidth',3,'color',[0, 0, 1, 0.1]);
end
hold off
% axis([1e-3 1e3 3e23 4e26]);
xlabel('$\epsilon - \epsilon_{exc}$ ($eV$)','interpreter','latex');
ylabel('$\sigma_e(\epsilon)$ ($m^2$)','interpreter','latex');
title('$11.82eV$','interpreter','latex');
leg = Exps;
leg{length(Exps)+1} = 'Sample models';
h=legend(leg);
set(h,'interpreter','latex');
set(gca,'XScale','log','YScale','log','FontSize',20,'TickLabelInterpreter','latex');

%% model functions

function crs = MERT(E)
% Argon momentum transfer cross section based on MERT model by Haddad &
% O'Malley (1982).
    a0 = 5.29177e-11;
    qe = 1.60217662e-19;
    me = 9.10938356e-31;
    hbar = 6.62607004e-34 / 2.0 / pi;
    alpha0 = 11.08;
    Efromk2 = hbar * hbar / 2.0 / me / qe / a0 / a0 ;

    A = -1.489; D = 65.0; F = -82.9; E1 = 0.881;

    k = sqrt( E / Efromk2 );
    crs = zeros('like',E);

    eta0 =  - A * ( 1. + 4. / 3. * alpha0 * k .* k .* log(k) ) - pi / 3. * alpha0 * k + D * k.^2 + F * k.^3;
    eta0 = atan(eta0 .* k);

    eta1 = pi / 15. * alpha0 * k .* ( 1. - sqrt(E/E1) );
    eta1 = atan(eta1 .* k);

    crs = crs + sin(eta0 - eta1).^2;
    for L = 1:20
        eta0 = eta1;
        L1 = L+1;
        eta1 = pi * alpha0 * k / (2.*L1 + 3.) / (2.*L1 + 1.) / (2.*L1 - 1.);
        eta1 = atan(eta1 .* k);

        crs = crs + L1 * sin(eta0 - eta1).^2;
    end
    crs = crs * 4. * pi ./ k ./ k * a0 * a0;
end

function crs = ion_BED(theta,E)
    a = theta(1); b = theta(2); c = theta(3);
    a0 = 5.29177e-11;
    E0 = 15.7596119;

    t = E / E0;

    crs = 4. * pi * a0 * a0 ./ t .* ( a * log(t) + b .* (1. - 1. ./ t) + c * log(t) ./ (t + 1.) );
end

function crs = excite_resonance(theta,E)
    F0 = theta(1); beta = theta(2);
    qe = 1.60217662e-19;
    me = 9.10938356e-31;
    a0 = 5.29177e-11;
    R0 = 13.605693122994;
    c0 = 2.99792458e8;
    E0 = 11.82807116;
    mc2 = me * c0 * c0 / qe;

    v2 = qe * E * 2.0 / me;
    beta2 = v2 / c0 / c0;
    rel_factor = log(beta2 ./ (1.0 - beta2) * mc2 / 2.0 / E0) - beta2;
    crs = 4. * pi * a0 * a0 * R0 ./ E * F0 / E0 .* rel_factor .* ( 1.0 - (E0./E) ) .^ beta;
end