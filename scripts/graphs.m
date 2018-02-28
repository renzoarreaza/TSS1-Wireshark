format long

close all; clear all;
clc;

%Changing to the directory in which this file is located
%(for the relative path below to work
if(~isdeployed)
  cd(fileparts(which(mfilename)));
end

setname = '../results/lunch.csv';
data = csvread(setname, 0,0);
% n = 100;

b = data(:,1);
g = data(:,2);
n = data(:,3);

[time, x] = size(data);
% figure('color','w')

figure; hold on
a1 = plot(1:time,b,'x'); M1 = "b";
hold on
a2 = plot(1:time,g,'o'); M2 = "g";
hold on
a3 = plot(1:time,n,'*'); M3 = "n";
legend([a1,a2,a3], [M1, M2, M3]);
set(gca, 'Yscale', 'log')
grid on
xlabel('time (min)')
ylabel('packets per minute')
title('PHY usage')


b_mod_dbpsk = data(:,4);
b_mod_dqpsk = data(:,5);
b_mod_bpsk = data(:,6);
b_mod_qpsk = data(:,7);

figure; hold on
a1 = plot(1:time,b_mod_dbpsk,'x'); M1 = "DBPSK";
hold on
a2 = plot(1:time,b_mod_dqpsk,'o'); M2 = "DQPSK";
hold on
a3 = plot(1:time,b_mod_bpsk,'*'); M3 = "BPSK";
hold on
a4 = plot(1:time,b_mod_qpsk,'^'); M4 = "QPSK";
legend([a1, a2, a3, a4], [M1, M2, M3, M4]);
set(gca, 'Yscale', 'log')
grid on
xlabel('time (min)')
ylabel('packets per minute')
title('modulation usage for 802.11b')

g_mod_bpsk = data(:,8);
g_mod_qpsk = data(:,9);
g_mod_16qam = data(:,10);
g_mod_64qam = data(:,11);

figure; hold on
a1 = plot(1:time,g_mod_bpsk,'x'); M1 = "BPSK";
hold on
a2 = plot(1:time,g_mod_qpsk,'o'); M2 = "QPSK";
hold on
a3 = plot(1:time,g_mod_16qam,'*'); M3 = "16-QAM";
hold on
a4 = plot(1:time,g_mod_64qam,'^'); M4 = "64-QAM";
legend([a1, a2, a3, a4], [M1, M2, M3, M4]);
set(gca, 'Yscale', 'log')
grid on
xlabel('time (min)')
ylabel('packets per minute')
title('modulation usage for 802.11g')

n_mod_bpsk = data(:,12);
n_mod_qpsk = data(:,13);
n_mod_16qam = data(:,14);
n_mod_64qam = data(:,15);
n_mod_asym = data(:,16);

figure; hold on
a1 = plot(1:time,n_mod_bpsk,'x'); M1 = "BPSK";
hold on
a2 = plot(1:time,n_mod_qpsk,'o'); M2 = "QPSK";
hold on
a3 = plot(1:time,n_mod_16qam,'*'); M3 = "16-QAM";
hold on
a4 = plot(1:time,n_mod_64qam,'^'); M4 = "64-QAM";
hold on
a5 = plot(1:time,n_mod_asym,'>'); M5 = "Asym";
legend([a1, a2, a3, a4, a5], [M1, M2, M3, M4, M5]);
set(gca, 'Yscale', 'log')
grid on
xlabel('time (min)')
ylabel('packets per minute')
title('modulation usage for 802.11n (2.4Ghz)')


b_rates = data(1,17:20);
b_rate_use = data(:,21:24);

figure; hold on
for i=1:4
    a(i) = plot(1:time, b_rate_use(:,i)); M(i) = b_rates(i) + "Mbps";
end
legend(a,M);
set(gca, 'Yscale', 'log')
grid on
xlabel('time (min)')
ylabel('packets per minute')
title('data rate usage for 802.11b')



g_rates = data(1,25:32);
g_rate_use = data(:,33:40);

figure; hold on
for i=1:8
    a(i) = plot(1:time, g_rate_use(:,i)); M(i) = g_rates(i) + "Mbps";
end
legend(a,M);
set(gca, 'Yscale', 'log')
grid on 
xlabel('time (min)')
ylabel('packets per minute')
title('data rate usage for 802.11g')
    
    

n_rate_num = data(:,41);
n_rate_num_max = max(data(:,41));

for i=1:time
    int = data(i, (42+n_rate_num(i)):(42+2*n_rate_num(i)-1));
    int(n_rate_num_max) = 0;
    if i ==1
        n_rate_use = int;
    else
        n_rate_use = [n_rate_use; int]; 
    end
end
n_rates = data(end, 42:(42+n_rate_num_max-1));
                 
figure; hold on
for i=1:n_rate_num_max
    a(i) = plot(1:time, n_rate_use(:,i)); M(i) = n_rates(i) + "Mbps";
end
legend(a,M);
set(gca, 'Yscale', 'log')
grid on 
xlabel('time (min)')
ylabel('packets per minute')
title('data rate usage for 802.11n (2.4ghz)')
            

            


