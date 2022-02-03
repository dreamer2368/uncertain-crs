clear all
close all
clc

run constants;

fID = fopen('../bolsig/xx.dat');
xx = fread(fID,'single');
xx = reshape(xx,[100 100]);
fclose(fID);

fID = fopen('../bolsig/ss.dat');
ss = fread(fID,'single');
ss = reshape(ss,[100 100]);
fclose(fID);

fID = fopen('../bolsig/pp.dat');
pp = fread(fID,'single');
pp = reshape(pp,[100 100]);
fclose(fID);

fID = fopen('../bolsig/BSR.excite.4.dat');
BSR = fread(fID,'single');
BSR = reshape(BSR,[2 325])';
fclose(fID);

refs = {'Chutjian1981','Schappe1994','Li1988','Khakoo2004','Tsurubuchi1996'};
Nref = length(refs);

idx=1;
for k = 1:Nref
    filename = strcat('../crs-exp/excitation-level4/crs.',refs{k},'.txt');
    W{idx} = importdata(filename);
    lgs{idx} = strcat(refs{k});
    idx = idx+1;
end

figure(1)
surf(xx,ss,log(pp),'edgecolor','none');
hold on
for k=1:Nref
%     errorbar(W{k}(:,1)-E0,W{k}(:,2),W{k}(:,3),'x','linewidth',1);
    plot3(W{k}(:,1)-E0,W{k}(:,2),W{k}(:,3)+10,'.r','markersize',10,'linewidth',2);
    lgd{idx} = lgs{k};
    idx = idx+1;
end
plot3(BSR(:,1),BSR(:,2),10*ones(325,1),'.r','markersize',10,'linewidth',2)
hold off
% contour(xx,ss,pp);
set(gca,'XScale','log','YScale','log')
view([0 0 1]);
axis([min(min(xx)) max(max(xx)) min(min(ss)) max(max(ss))]);