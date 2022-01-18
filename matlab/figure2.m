%%
close all
clear all
clc

run constants;

LXCats = {'BSR'};
Nsets = length(LXCats);

for k = 1:Nsets
    filename = strcat('../bolsig/crs/excitation-level4/crs.',LXCats{k},'.txt');
    excite{k} = importdata(filename);
end

refs = {'Chutjian1981','Schappe1994','Li1988','Khakoo2004','Tsurubuchi1996'};
Nref = length(refs);

idx=1;
for k = 1:Nref
    filename = strcat('../crs-exp/excitation-level4/crs.',refs{k},'.txt');
    W{idx} = importdata(filename);
    lgs{idx} = strcat(refs{k});
    idx = idx+1;
end

filename = strcat('../crs-exp/excitation-level4/crs.krig.txt');
W_krig = importdata(filename);

filename = strcat('../crs-exp/excitation-level4/crs.krig.withBSR.txt');
W_krig_BSR = importdata(filename);

fID = fopen('../crs-Bayes1/crs.excitation.level4.dat');
Bayes = fread(fID,'double');
Bayes = reshape(Bayes',[2,10528])';
fclose(fID);

fID = fopen('../crs-Bayes1/crs.excitation.level4.withBSR.modified.dat');
BayesBSR = fread(fID,'double');
BayesBSR = reshape(BayesBSR',[4,4224])';
fclose(fID);

idx=1;
lgd = {};
figure(1)
for k=1:Nref
    errorbar(W{k}(:,1)-E0,W{k}(:,2),W{k}(:,3),'o','linewidth',1);
    lgd{idx} = lgs{k};
    idx = idx+1;
    hold on
end
plot(W_krig(:,1)-E0,W_krig(:,2),'-k','linewidth',2);
lgd{idx} = 'Posterior mean';
idx = idx+1;
patch([W_krig(:,1)' fliplr(W_krig(:,1)')]-E0,[W_krig(:,2)'./(W_krig(:,3).^2)' fliplr(W_krig(:,2)'.*(W_krig(:,3).^2)')],...
        'b','edgecolor','none');
alpha(0.1);
lgd{idx} = '95\% confidence';
idx = idx+1;
hold off
title(strcat(num2str(E0),'eV'),'interpreter','latex');
xlabel('$\epsilon-\epsilon_{ex}$ ($eV$)','interpreter','latex');
ylabel('$\sigma$ ($m^2$)','interpreter','latex');
h=legend(lgd);
set(h,'interpreter','latex','fontsize',15);
set(gca,'fontsize',20,'ticklabelinterpreter','latex','yscale','log','xscale','log');

figure(2)
hist3(Bayes,'Nbins',30*[1 1],'CdataMode','auto','edgecolor','none');
axis([1.8 3.4 0.5 2.4]);
view([0 0 1]);
xlabel('$F_0$','interpreter','latex');
ylabel('$\beta$','interpreter','latex');
set(gca,'fontsize',20,'ticklabelinterpreter','latex');

Nsample = 1000;
idxes = randi(size(Bayes,1),Nsample,1);
Etest = linspace(0,3,100);
Etest = 10.0.^Etest + E0;

figure(3)
for k=1:Nref
    errorbar(W{k}(:,1)-E0,W{k}(:,2),W{k}(:,3),'o','linewidth',2);
    lgd{idx} = lgs{k};
    idx = idx+1;
    hold on
end
% color = [255 165 0]/255;
color = [0 0 1];
for k = 1:Nsample
    crs_sample = argon_excite4(Bayes(k,:),Etest);
    loglog(Etest-E0,crs_sample,'-','color',[color 0.003],'linewidth',10);
end
hold off
xlabel('$\epsilon-\epsilon_{ex}$ ($eV$)','interpreter','latex');
ylabel('$\sigma$ ($m^2$)','interpreter','latex');
ylim([1e-23 1e-20]);
set(gca,'fontsize',20,'ticklabelinterpreter','latex','yscale','log','xscale','log');

Nw = [3,5,10,30,50,100,300,500,1000,3000,5000,10000];
likelihoods = [ -2.42780269  -3.21454378  -7.05433508 -11.97617027 -14.3455731 -17.26745923 -20.66484693 -21.71895476 -22.74802511 -23.77969443 -24.1139435  -24.48084445];
figure(4)
semilogx(Nw,likelihoods,'o','linewidth',2);
ylabel('$\log P(\sigma_*\vert\vec{\sigma}_m,\vec{\epsilon}_m,\epsilon_*)$','interpreter','latex');
xlabel('$N$','interpreter','latex');
set(gca,'fontsize',20,'ticklabelinterpreter','latex');

idx=1;
lgd = {};
figure(5)
for k=1:Nref
    errorbar(W{k}(:,1)-E0,W{k}(:,2),W{k}(:,3),'o','linewidth',1);
    lgd{idx} = lgs{k};
    idx = idx+1;
    hold on
end
plot(excite{1}(:,1)-E0,excite{1}(:,2),'x','linewidth',2);
lgd{idx} = 'BSR';
idx = idx+1;
plot(W_krig_BSR(:,1)-E0,W_krig_BSR(:,2),'-k','linewidth',2);
lgd{idx} = 'Posterior mean';
idx = idx+1;
patch([W_krig_BSR(:,1)' fliplr(W_krig_BSR(:,1)')]-E0,[W_krig_BSR(:,2)'./(W_krig_BSR(:,3).^2)' fliplr(W_krig_BSR(:,2)'.*(W_krig_BSR(:,3).^2)')],...
        'b','edgecolor','none');
alpha(0.1);
lgd{idx} = '95\% confidence';
idx = idx+1;
hold off
title(strcat(num2str(E0),'eV'),'interpreter','latex');
xlabel('$\epsilon-\epsilon_{ex}$ ($eV$)','interpreter','latex');
ylabel('$\sigma$ ($m^2$)','interpreter','latex');
h=legend(lgd);
set(h,'interpreter','latex','fontsize',15);
set(gca,'fontsize',20,'ticklabelinterpreter','latex','yscale','log','xscale','log');

Nsample = 1000;
idxes = randi(size(BayesBSR,1),Nsample,1);
Etest = linspace(-4,3,100);
Etest = 10.0.^Etest + E0;

figure(6)
for k=1:Nref
    errorbar(W{k}(:,1)-E0,W{k}(:,2),W{k}(:,3),'o','linewidth',2);
    lgd{idx} = lgs{k};
    idx = idx+1;
    hold on
end
plot(excite{1}(:,1)-E0,excite{1}(:,2),'x','linewidth',2);
% color = [255 165 0]/255;
color = [0 0 1];
for k = 1:Nsample
    crs_sample = argon_excite4_modified(BayesBSR(k,:),Etest);
    loglog(Etest-E0,crs_sample,'-','color',[color 0.003],'linewidth',10);
end
hold off
xlabel('$\epsilon-\epsilon_{ex}$ ($eV$)','interpreter','latex');
ylabel('$\sigma$ ($m^2$)','interpreter','latex');
ylim([1e-23 3e-21]);
set(gca,'fontsize',20,'ticklabelinterpreter','latex','yscale','log','xscale','log');