clear all
close all
clc

refs = {'AlAminLucas1987','GoldenFisher1961','Kruithof1940','KucukarpaciLucas1981','MilloyCrompton1977','NakamuraKurachi1988','PackPhelps1961','Robertson1977','RobertsonRee1972','Specht1980','Tachibana1986'};

idx=1;
for k = [4,6,7,8]
    if(k<7)
        filename = strcat('./W.',refs{k},'.txt');
        W{idx} = importdata(filename);
        lgs{idx} = refs{k};
    elseif(k==7)
        filename = strcat('./W.',refs{k},'.77.txt');
        W{idx} = importdata(filename);
        lgs{idx} = strcat(refs{k},'-77K');
        idx = idx+1;
        filename = strcat('./W.',refs{k},'.300.txt');
        W{idx} = importdata(filename);
        lgs{idx} = strcat(refs{k},'-300K');
    elseif(k==8)
        filename = strcat('./W.',refs{k},'.293.txt');
        W{idx} = importdata(filename);
        lgs{idx} = strcat(refs{k},'-293K');
        idx1 = idx;
        idx = idx+1;
        filename = strcat('./W.',refs{k},'.90.txt');
        W{idx} = importdata(filename);
        lgs{idx} = strcat(refs{k},'-90K');
    end
    idx = idx+1;
end

NW = length(W);
figure(1)
for k=1:NW
    if(k==idx1)
        errorbar(W{k}(:,1),W{k}(:,2),W{k}(:,3),'o','linewidth',1,'markersize',50);
    else
        errorbar(W{k}(:,1),W{k}(:,2),W{k}(:,3),'o','linewidth',1);
    end
    hold on
end
hold off
xlabel('$E$ ($Td$)','interpreter','latex');
ylabel('$W=\mu E$ ($m/s$)','interpreter','latex');
h=legend(lgs);
set(h,'interpreter','latex','fontsize',15);
set(gca,'fontsize',20,'ticklabelinterpreter','latex','yscale','log','xscale','log');

%%
clear all
close all
clc

refs = {'AlAminLucas1987','GoldenFisher1961','Kruithof1940','KucukarpaciLucas1981','MilloyCrompton1977','NakamuraKurachi1988','PackPhelps1961','Robertson1977','RobertsonRee1972','Specht1980','Tachibana1986'};

idx=1;
for k = [4,6,9]
    if(k<9)
        filename = strcat('./DLmu.',refs{k},'.txt');
        DLmu{idx} = importdata(filename);
        lgs{idx} = refs{k};
    elseif(k==9)
        filename = strcat('./DLmu.',refs{k},'.700.txt');
        DLmu{idx} = importdata(filename);
        lgs{idx} = strcat(refs{k},'-700Torr');
        idx = idx+1;
        filename = strcat('./DLmu.',refs{k},'.800.txt');
        DLmu{idx} = importdata(filename);
        lgs{idx} = strcat(refs{k},'-800Torr');
    end
    idx = idx+1;
end

NDLmu = length(DLmu);
figure(2)
for k=1:NDLmu
    errorbar(DLmu{k}(:,1),DLmu{k}(:,2),DLmu{k}(:,3),'o','linewidth',1);
    hold on
end
hold off
xlabel('$E$ ($Td$)','interpreter','latex');
ylabel('$D_L/\mu$ ($V$)','interpreter','latex');
h=legend(lgs);
set(h,'interpreter','latex','fontsize',15);
set(gca,'fontsize',20,'ticklabelinterpreter','latex','yscale','log','xscale','log');

%%
clear all
close all
clc

refs = {'AlAminLucas1987','GoldenFisher1961','Kruithof1940','KucukarpaciLucas1981','MilloyCrompton1977','NakamuraKurachi1988','PackPhelps1961','Robertson1977','RobertsonRee1972','Specht1980','Tachibana1986'};

idx=1;
for k = [1,5]
    filename = strcat('./DTmu.',refs{k},'.txt');
    DTmu{idx} = importdata(filename);
    lgs{idx} = refs{k};
    idx = idx+1;
end

NDTmu = length(DTmu);
figure(2)
for k=1:NDTmu
    errorbar(DTmu{k}(:,1),DTmu{k}(:,2),DTmu{k}(:,3),'o','linewidth',1);
    hold on
end
hold off
xlabel('$E$ ($Td$)','interpreter','latex');
ylabel('$D_T/\mu$ ($V$)','interpreter','latex');
h=legend(lgs);
set(h,'interpreter','latex','fontsize',15);
set(gca,'fontsize',20,'ticklabelinterpreter','latex','yscale','log','xscale','log');

%%
clear all
close all
clc

refs = {'AlAminLucas1987','GoldenFisher1961','Kruithof1940','KucukarpaciLucas1981','MilloyCrompton1977','NakamuraKurachi1988','PackPhelps1961','Robertson1977','RobertsonRee1972','Specht1980','Tachibana1986'};

idx=1;
for k = [2,3,10]
    filename = strcat('./aion.',refs{k},'.txt');
    aion{idx} = importdata(filename);
    lgs{idx} = refs{k};
    idx = idx+1;
end

Naion = length(aion);
figure(2)
for k=1:Naion
    errorbar(aion{k}(:,1),aion{k}(:,2),aion{k}(:,3),'o','linewidth',1);
    hold on
end
hold off
xlabel('$E$ ($Td$)','interpreter','latex');
ylabel('$\alpha_{ion}/N$ ($m^2$)','interpreter','latex');
h=legend(lgs);
set(h,'interpreter','latex','fontsize',15);
set(gca,'fontsize',20,'ticklabelinterpreter','latex','yscale','log','xscale','log');

%%
clear all
close all
clc

refs = {'AlAminLucas1987','GoldenFisher1961','Kruithof1940','KucukarpaciLucas1981','MilloyCrompton1977','NakamuraKurachi1988','PackPhelps1961','Robertson1977','RobertsonRee1972','Specht1980','Tachibana1986'};

idx=1;
for k = [11]
    if (k==11)
        filename = strcat('./aex1.',refs{k},'.txt');
        aex1{idx} = importdata(filename);
        filename = strcat('./aex2.',refs{k},'.txt');
        aex2{idx} = importdata(filename);
        filename = strcat('./aex3.',refs{k},'.txt');
        aex3{idx} = importdata(filename);
        filename = strcat('./aex4.',refs{k},'.txt');
        aex4{idx} = importdata(filename);
        lgs{idx} = refs{k};
    end
    idx = idx+1;
end

% Naion = length(aion);
k=1;
figure(2)
errorbar(aex1{k}(:,1),aex1{k}(:,2),aex1{k}(:,3),'o','linewidth',1);
hold on
errorbar(aex2{k}(:,1),aex2{k}(:,2),aex2{k}(:,3),'o','linewidth',1);
errorbar(aex3{k}(:,1),aex3{k}(:,2),aex3{k}(:,3),'o','linewidth',1);
errorbar(aex4{k}(:,1),aex4{k}(:,2),aex4{k}(:,3),'o','linewidth',1);
hold off
xlabel('$E$ ($Td$)','interpreter','latex');
ylabel('$\alpha_{ex}/N$ ($m^2$)','interpreter','latex');
h=legend('$1s_5$','$1s_4$','$1s_3$','$1s_2$');
set(h,'interpreter','latex','fontsize',20);
set(gca,'fontsize',20,'ticklabelinterpreter','latex','yscale','log','xscale','log');