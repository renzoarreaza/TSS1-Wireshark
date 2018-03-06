%% User nust provide the name of the files to be analized. One file per mac address
%% Each file will generate 3 graphs.
%% 1.Total frames per modulation vs Time
%% 2. Percentage of frames per modulation vs Sector. Percentages are calculated per sector.
%% 3. Percentage of frames per Data Rate vs Sector. Percentages are calculated per sector.
%% Each file is analized in 3 intervals of time (3 sectors)
%% User must provide the maximum time for each sector.
%% The interval of time is calculated from the maximum time of the previous sector until the maximum time ingressed by the user
%% User must provide time within the range of the test. If a time value is outside the range, no graph will be generated for that sector

clear variables;
close all;

time_sector1 = str2double(inputdlg("Enter maximum time for the first sector (min)"));
time_sector2 = str2double(inputdlg("Enter maximum time for the second sector (min)"));
time_sector3 = str2double(inputdlg("Enter maximum time for the third sector (min)"));


%% Reading Table
while true

clearvars -except time_sector1 time_sector2 time_sector3
    
msg = inputdlg("Enter the name of the file or 'q' to exit: ");
if msg{1} == 'q'
    break
end
try
table1 = readtable(msg{:});
catch
    warning("File name not valid")
    continue
end

table1.datarate = round(table1.datarate,1);
table1 = sortrows(table1, {'time','modulation', 'total'});
modulation = {'64QAM', '16QAM', 'QPSK', 'BPSK'};

%% Total Frames - Modulation vs Time
figure;
hold on;
title('Changing Distance');
ylabel('# frames');
xlabel('t (min)')

ss = table1.time(end);
for i = 1:ss
    for j = 1:4
        z = sum(table1.total(table1.time == i & strcmp(table1.modulation, modulation{j})));
        time1((i -1) * 4 + j) = i;
        modulation1{(i - 1) * 4 + j} = modulation{j};
        total1((i - 1) * 4 + j) = z;
    end
end
table2 = table(time1', modulation1', total1', 'VariableNames', {'time', 'modulation', 'total'});
for j = 1:4
    plot(table2.time(strcmp(table2.modulation, modulation{j})), table2.total(strcmp(table2.modulation, modulation{j})), '--')
end
legend(modulation{:})
hold off;

%% Get Sectors
sectors = 3;

sector1 = table1(table1.time <= time_sector1, :);
sector2 = table1(table1.time > time_sector1 & table1.time <= time_sector2, :);
sector3 = table1(table1.time > time_sector2 & table1.time <= time_sector3, :);

total_sector1 = sum(sector1.total);
total_sector2 = sum(sector2.total);
total_sector3 = sum(sector3.total);

%% Bar Frames per sector
figure;
hold on;
title('% Frames per Sector');
ylabel('Frames per Sector (%)');
xlabel('Modulation');

bar_frames_sector = zeros(sectors, 4);

for i= 1:4
    bar_frames_sector(1, i) = sum(sector1.total(strcmp(sector1.modulation, modulation{i})))/total_sector1 * 100;
    bar_frames_sector(2, i) = sum(sector2.total(strcmp(sector2.modulation, modulation{i})))/total_sector2 * 100;
    bar_frames_sector(3, i) = sum(sector3.total(strcmp(sector3.modulation, modulation{i})))/total_sector3 * 100;
end

c = categorical({strcat('0 to ',num2str(time_sector1), ' min'),strcat(num2str(time_sector1),' to  ',num2str(time_sector2), ' min'),strcat(num2str(time_sector2),' to  ',num2str(time_sector3), ' min')});
bar(c, bar_frames_sector)
legend('64QAM', '16QAM', 'QPSK', 'BPSK')
hold off;

%% Bar - Data Rate - Modulation Subplots per sector
figure;

x1 = unique(sector1.datarate);
for i = 1:size(x1, 1)
    y1(i) = sum(sector1.total(x1(i) == sector1.datarate))/total_sector1 * 100;
end
subplot(3,1,1);
bar(x1, y1);
title({'% Frames vs Data Rate' ; strcat('Sector1: From 0 to ',num2str(time_sector1), ' min')});


x2 = unique(sector2.datarate);
for i = 1:size(x2, 1)
    y2(i) = sum(sector2.total(x2(i) == sector2.datarate))/total_sector2 * 100;
end
subplot(3,1,2);
bar(x2, y2);
title(strcat('Sector 2: From ', num2str(time_sector1),' to  ',num2str(time_sector2), ' min'));
ylabel('Frames (%)');

x3 = unique(sector3.datarate);
for i = 1:size(x3, 1)
    y3(i) = sum(sector3.total(x3(i) == sector3.datarate))/total_sector3 * 100;
end
subplot(3,1,3);
bar(x3, y3);
title(strcat('Sector 3: From ', num2str(time_sector2),' to  ',num2str(time_sector3), ' min'));
xlabel('Data Rate (Mbit/s)');

end




