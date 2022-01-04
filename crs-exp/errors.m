clear all
close all
clc

refs = {'Chutjian1981','Buckman1983','Filipovic2000','Khakoo2004'};

idx=1;
lvls = [];
for k = 1:4
    if(k==1)
        for j=1:4
            filename = strcat('./crs.',refs{k},'.',num2str(j),'.txt');
            W{idx} = importdata(filename);
            lgs{idx} = strcat(refs{k});
            lvls = [lvls; j];
            idx = idx+1;
        end
    elseif(k==2)
        filename = strcat('./crs.',refs{k},'.1+3.txt');
        W{idx} = importdata(filename);
        lgs{idx} = strcat(refs{k},'-(1+3)');
        lvls = [lvls; 1];
        idx = idx+1;
    elseif(k==3)
        for j=1:3
            filename = strcat('./crs.',refs{k},'.',num2str(j),'.txt');
            W{idx} = importdata(filename);
            lgs{idx} = strcat(refs{k});
            lvls = [lvls; j];
            idx = idx+1;
        end
    elseif(k==4)
        filename = strcat('./crs.',refs{k},'.txt');
        temp = importdata(filename);
        for j=1:4
            W{idx} = [temp(:,1) temp(:,2*j:2*j+1)];
            lgs{idx} = strcat(refs{k});
            lvls = [lvls; j];
            idx = idx+1;
        end
    end
end

levels = {'$4s[3/2]^o_2$','$4s[3/2]^o_1$',"$4s'[3/2]^o_0$","$4s'[3/2]^o_1$"};
NW = length(W);
for lev = 1:4
    idx=1;
    lgd = {};
    figure(lev)
    for k=1:NW
        if(lvls(k)==lev)
            errorbar(W{k}(:,1),W{k}(:,2),W{k}(:,3),'o','linewidth',1);
            lgd{idx} = lgs{k};
            idx = idx+1;
            hold on
        end
    end
    hold off
    title(levels{lev},'interpreter','latex');
    xlabel('$E$ ($eV$)','interpreter','latex');
    ylabel('$\sigma^2$ ($m^2$)','interpreter','latex');
    h=legend(lgd);
    set(h,'interpreter','latex','fontsize',15);
    set(gca,'fontsize',20,'ticklabelinterpreter','latex','yscale','log','xscale','log');
end

% lgd={};
% idx=1;
% figure(5)
% for k=1:NW
%     if(lvls(k)==-1)
%         errorbar(W{k}(:,1),W{k}(:,2),W{k}(:,3),'o','linewidth',1);
%         lgd{idx} = lgs{k};
%         idx = idx+1;
%         hold on
%     end
% end
% hold off
% title('Total (metastable)','interpreter','latex');
% xlabel('$E$ ($eV$)','interpreter','latex');
% ylabel('$\sigma^2$ ($m^2$)','interpreter','latex');
% h=legend(lgd);
% set(h,'interpreter','latex','fontsize',15);
% set(gca,'fontsize',20,'ticklabelinterpreter','latex','yscale','log','xscale','log');

%%
close all
clear all
clc

refs = {'Chutjian1981','Schappe1994','Filipovic2000b','Khakoo2004'};
Nref = length(refs);

idx=1;
for k = 1:4
    filename = strcat('./excitation-level1/crs.',refs{k},'.txt');
    W{idx} = importdata(filename);
    lgs{idx} = strcat(refs{k});
    idx = idx+1;
end

idx=1;
lgd = {};
figure(1)
for k=1:Nref
    errorbar(W{k}(:,1),W{k}(:,2),W{k}(:,3),'o','linewidth',1);
    lgd{idx} = lgs{k};
    idx = idx+1;
    hold on
end
hold off
title('11.55eV','interpreter','latex');
xlabel('$E$ ($eV$)','interpreter','latex');
ylabel('$\sigma$ ($m^2$)','interpreter','latex');
h=legend(lgd);
set(h,'interpreter','latex','fontsize',20);
set(gca,'fontsize',20,'ticklabelinterpreter','latex','yscale','log','xscale','log');

idx=1;
lgd = {};
E1 = 11.55;
figure(2)
for k=1:Nref
    errorbar(log(W{k}(:,1)-E1),log(W{k}(:,2)),log(1+W{k}(:,3)./W{k}(:,2)),'o','linewidth',1);
    lgd{idx} = lgs{k};
    idx = idx+1;
    hold on
end
hold off
title('11.55eV','interpreter','latex');
xlabel('$\log(E-E_1)$','interpreter','latex');
ylabel('$\log(\sigma)$','interpreter','latex');
h=legend(lgd);
set(h,'interpreter','latex','fontsize',20);
set(gca,'fontsize',20,'ticklabelinterpreter','latex');

filename = strcat('./excitation-level1/krig.variogram.model.txt');
krig_model = importdata(filename);
filename = strcat('./excitation-level1/krig.variogram.empirical.txt');
krig_emp = importdata(filename);
figure(3)
plot(krig_emp(:,1),krig_emp(:,2),'o','linewidth',2);
hold on
plot(krig_model(:,1),krig_model(:,2),'-','linewidth',2);
hold off
xlabel('$r$','interpreter','latex');
ylabel('$E[(Z(x+r)-Z(x))^2]$','interpreter','latex');
h=legend('Sample','Model');
set(h,'interpreter','latex','fontsize',20);
set(gca,'fontsize',20,'ticklabelinterpreter','latex');

filename = strcat('./excitation-level1/crs.krig.txt');
W_krig = importdata(filename);

idx=1;
lgd = {};
figure(4)
for k=1:Nref
    errorbar(log(W{k}(:,1)-E1),log(W{k}(:,2)),log(1+W{k}(:,3)./W{k}(:,2)),'o','linewidth',1);
    lgd{idx} = lgs{k};
    idx = idx+1;
    hold on
end
plot(W_krig(:,1),W_krig(:,2),'-k','linewidth',2);
lgd{idx} = 'Kriged prior';
idx = idx+1;
patch([W_krig(:,1)' fliplr(W_krig(:,1)')],[W_krig(:,2)'-3*W_krig(:,3)' fliplr(W_krig(:,2)'+3*W_krig(:,3)')],...
        'b','edgecolor','none');
alpha(0.1);
lgd{idx} = '99\% confidence';
idx = idx+1;
hold off
title('11.55eV','interpreter','latex');
xlabel('$\log(E-E_1)$','interpreter','latex');
ylabel('$\log(\sigma)$','interpreter','latex');
h=legend(lgd);
set(h,'interpreter','latex','fontsize',20);
set(gca,'fontsize',20,'ticklabelinterpreter','latex');
xlim([-4 5]);

idx=1;
lgd = {};
figure(5)
for k=1:Nref
    errorbar(W{k}(:,1),W{k}(:,2),W{k}(:,3),'o','linewidth',1);
    lgd{idx} = lgs{k};
    idx = idx+1;
    hold on
end
plot(exp(W_krig(:,1))+E1,exp(W_krig(:,2)),'-k','linewidth',2);
lgd{idx} = 'Kriged prior';
idx = idx+1;
patch([exp(W_krig(:,1)')+E1 fliplr(exp(W_krig(:,1)')+E1)],exp([W_krig(:,2)'-3*W_krig(:,3)' fliplr(W_krig(:,2)'+3*W_krig(:,3)')]),...
        'b','edgecolor','none');
alpha(0.1);
lgd{idx} = '99\% confidence';
idx = idx+1;
patch([exp(W_krig(:,1)')+E1 fliplr(exp(W_krig(:,1)')+E1)],exp([W_krig(:,2)'-W_krig(:,3)' fliplr(W_krig(:,2)'+W_krig(:,3)')]),...
        'r','edgecolor','none');
alpha(0.1);
lgd{idx} = '68\% confidence';
idx = idx+1;
hold off
title('11.55eV','interpreter','latex');
xlabel('$E$ ($eV$)','interpreter','latex');
ylabel('$\sigma$ ($m^2$)','interpreter','latex');
h=legend(lgd);
set(h,'interpreter','latex','fontsize',20);
set(gca,'fontsize',20,'ticklabelinterpreter','latex','xscale','log','yscale','log');
axis([1e1 1.5e2 1e-25 1e-20]);