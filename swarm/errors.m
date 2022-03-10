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

fID = fopen('../bolsig/forward-propagate/data-quartz/transport300K.muN.dat');
W300 = fread(fID,'double')';
W300 = reshape(W300,[100,floor(length(W300)/100)]);
fclose(fID);
E300 = linspace(log(1e-4),log(500),100)';
E300 = exp(E300);

fID = fopen('../bolsig/forward-propagate/data-quartz/transport77K.muN.dat');
W77 = fread(fID,'double')';
W77 = reshape(W77,[30,floor(length(W77)/30)]);
fclose(fID);
E77 = linspace(log(1e-4),log(1e-2),30)';
E77 = exp(E77);

fID = fopen('../bolsig/forward-propagate/data-quartz/transport90K.muN.dat');
W90 = fread(fID,'double')';
W90 = reshape(W90,[40,floor(length(W90)/40)]);
fclose(fID);
E90 = linspace(log(1e-4),log(1e-1),40)';
E90 = exp(E90);

NW = length(W);
figure(1)
for k=1:NW
%     if(k==idx1)
%         errorbar(W{k}(:,1),W{k}(:,2),W{k}(:,3),'o','linewidth',1,'markersize',50);
%     else
    errorbar(W{k}(:,1),W{k}(:,2),W{k}(:,3),'o','linewidth',1);
%     end
    hold on
end
for k = 1:72
    loglog(E300,W300(:,k).*E300/1e21,'-','color',[0 0 0 0.05],'linewidth',2);
    hold on
end
% for k = 1:72
%     loglog(E77,W77(:,k).*E77/1e21,'-','color',[1 0 0 0.05],'linewidth',2);
% end
% for k = 1:72
%     loglog(E90,W90(:,k).*E90/1e21,'-','color',[0 0 1 0.05],'linewidth',2);
% end
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

fID = fopen('../bolsig/forward-propagate/data-quartz/transport300K.muN.dat');
mu300 = fread(fID,'double')';
mu300 = reshape(mu300,[100,floor(length(mu300)/100)]);
fclose(fID);
fID = fopen('../bolsig/forward-propagate/data-quartz/transport300K.DLN.dat');
DL300 = fread(fID,'double')';
DL300 = reshape(DL300,[100,floor(length(DL300)/100)]);
fclose(fID);
E300 = linspace(log(1e-4),log(500),100)';
E300 = exp(E300);

fID = fopen('../bolsig/forward-propagate/data-quartz/transport77K.muN.dat');
mu77 = fread(fID,'double')';
mu77 = reshape(mu77,[30,floor(length(mu77)/30)]);
fclose(fID);
fID = fopen('../bolsig/forward-propagate/data-quartz/transport77K.DLN.dat');
DL77 = fread(fID,'double')';
DL77 = reshape(DL77,[30,floor(length(DL77)/30)]);
fclose(fID);
E77 = linspace(log(1e-4),log(1e-2),30)';
E77 = exp(E77);

fID = fopen('../bolsig/forward-propagate/data-quartz/transport90K.muN.dat');
mu90 = fread(fID,'double')';
mu90 = reshape(mu90,[40,floor(length(mu90)/40)]);
fclose(fID);
fID = fopen('../bolsig/forward-propagate/data-quartz/transport90K.DLN.dat');
DL90 = fread(fID,'double')';
DL90 = reshape(DL90,[40,floor(length(DL90)/40)]);
fclose(fID);
E90 = linspace(log(1e-4),log(1e-1),40)';
E90 = exp(E90);

NDLmu = length(DLmu);
figure(2)
for k = 1:72
    loglog(E300,DL300(:,k)./mu300,'-','color',[0 0 1 0.01],'linewidth',2);
    hold on
end
for k = 1:72
    loglog(E77,DL77(:,k)./mu77,'-','color',[0 1 0 0.01],'linewidth',2);
    hold on
end
for k = 1:72
    loglog(E90,DL90(:,k)./mu90,'-','color',[1 0 0 0.01],'linewidth',2);
    hold on
end
for k=1:NDLmu
    errorbar(DLmu{k}(:,1),DLmu{k}(:,2),DLmu{k}(:,3),'o','linewidth',1);
    hold on
end
hold off
xlabel('$E$ ($Td$)','interpreter','latex');
ylabel('$D_L/\mu$ ($V$)','interpreter','latex');
% h=legend(lgs);
% set(h,'interpreter','latex','fontsize',15);
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

fID = fopen('../bolsig/forward-propagate/data-quartz/transport300K.muN.dat');
mu300 = fread(fID,'double')';
mu300 = reshape(mu300,[100,floor(length(mu300)/100)]);
fclose(fID);
fID = fopen('../bolsig/forward-propagate/data-quartz/transport300K.DTN.dat');
DT300 = fread(fID,'double')';
DT300 = reshape(DT300,[100,floor(length(DT300)/100)]);
fclose(fID);
E300 = linspace(log(1e-4),log(500),100)';
E300 = exp(E300);

fID = fopen('../bolsig/forward-propagate/data-quartz/transport77K.muN.dat');
mu77 = fread(fID,'double')';
mu77 = reshape(mu77,[30,floor(length(mu77)/30)]);
fclose(fID);
fID = fopen('../bolsig/forward-propagate/data-quartz/transport77K.DTN.dat');
DT77 = fread(fID,'double')';
DT77 = reshape(DT77,[30,floor(length(DT77)/30)]);
fclose(fID);
E77 = linspace(log(1e-4),log(1e-2),30)';
E77 = exp(E77);

fID = fopen('../bolsig/forward-propagate/data-quartz/transport90K.muN.dat');
mu90 = fread(fID,'double')';
mu90 = reshape(mu90,[40,floor(length(mu90)/40)]);
fclose(fID);
fID = fopen('../bolsig/forward-propagate/data-quartz/transport90K.DTN.dat');
DT90 = fread(fID,'double')';
DT90 = reshape(DT90,[40,floor(length(DT90)/40)]);
fclose(fID);
E90 = linspace(log(1e-4),log(1e-1),40)';
E90 = exp(E90);

NDTmu = length(DTmu);
figure(2)
for k = 1:72
    loglog(E300,DT300(:,k)./mu300,'-','color',[0 0 1 0.01],'linewidth',2);
    hold on
end
for k = 1:72
    loglog(E77,DT77(:,k)./mu77,'-','color',[0 1 0 0.01],'linewidth',2);
    hold on
end
for k = 1:72
    loglog(E90,DT90(:,k)./mu90,'-','color',[1 0 0 0.01],'linewidth',2);
    hold on
end
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

fID = fopen('../bolsig/forward-propagate/data-quartz/rate300K.muN.dat');
mu300 = fread(fID,'double')';
mu300 = reshape(mu300,[40,floor(length(mu300)/40)]);
fclose(fID);

fID = fopen('../bolsig/forward-propagate/data-quartz/rate300K.ion.dat');
k300 = fread(fID,'double')';
k300 = reshape(k300,[40,floor(length(k300)/40)]);
fclose(fID);
E300 = linspace(log(1e0),log(500),40)';
E300 = exp(E300);

Naion = length(aion);
figure(2)
for k = 1:72
    loglog(E300,k300(:,k)./(mu300(:,k).*E300/1e21),'-','color',[0 0 1 0.05],'linewidth',2);
%     loglog(E300,(mu300(:,k).*E300/1e21),'-r');
    hold on
end
for k=1:Naion
    errorbar(aion{k}(:,1),aion{k}(:,2),aion{k}(:,3),'o','linewidth',1);
    hold on
end
hold off
xlabel('$E$ ($Td$)','interpreter','latex');
ylabel('$\alpha_{ion}/N$ ($m^2$)','interpreter','latex');
h=legend(lgs);
ylim([1e-25 1e-19]);
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

fID = fopen('../bolsig/forward-propagate/data/rate300K.muN.dat');
mu300 = fread(fID,'double')';
mu300 = reshape(mu300,[40,floor(length(mu300)/40)]);
fclose(fID);

fID = fopen('../bolsig/forward-propagate/data/rate300K.1s5.dat');
k300 = fread(fID,'double')';
k300 = reshape(k300,[40,floor(length(k300)/40)]);
fclose(fID);
E300 = linspace(log(1e0),log(500),40)';
E300 = exp(E300);

% Naion = length(aion);
k=1;
figure(2)
errorbar(aex1{k}(:,1),aex1{k}(:,2),aex1{k}(:,3),'o','linewidth',1);
hold on
errorbar(aex2{k}(:,1),aex2{k}(:,2),aex2{k}(:,3),'o','linewidth',1);
errorbar(aex3{k}(:,1),aex3{k}(:,2),aex3{k}(:,3),'o','linewidth',1);
errorbar(aex4{k}(:,1),aex4{k}(:,2),aex4{k}(:,3),'o','linewidth',1);

for k = 1:2
    loglog(E300,k300(:,k)./(mu300(:,k)/1e21),'-','linewidth',2);
%     loglog(E300,(mu300(:,k).*E300/1e21),'-r');
end

hold off
xlabel('$E$ ($Td$)','interpreter','latex');
ylabel('$\alpha_{ex}/N$ ($m^2$)','interpreter','latex');
% ylim([1e-23 1e-20]);
h=legend('$1s_5$','$1s_4$','$1s_3$','$1s_2$','$1s_5$, Biagi','$1s_5$, BSR');
set(h,'interpreter','latex','fontsize',20);
set(gca,'fontsize',20,'ticklabelinterpreter','latex','yscale','log','xscale','log');

% figure(3)
% for k = 1:2
% %     loglog(E300,k300(:,k)./(mu300(:,k).*E300/1e21),'-k');
%     loglog(E300,(mu300(:,k).*E300/1e21),'-r');
% end