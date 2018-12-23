clc;
clear;
sensor_number = input('Please input the sensor number (2 or 3):');

if sensor_number ~= 2 && sensor_number ~= 3
    fprintf('The sensor number is 2 or 3 only \n');
    disp('Please Run the Program again and input number again');
    return 
end

if sensor_number == 2
    disp('2 sensors for GDP measure only');
end

if sensor_number == 3
    disp('3 sensors:')
    disp('2 sensors for GDP measure, 1 sensor for GDP growth (Extra Part)');
end

gdp = [1.057, 0.967, 0.905, 0.788, 0.778, 0.862, 0.939, 1.061, 1.115, 1.078, 1.164, 1.266, 1.49, 1.772, 2.074, 2.239, 2.218, 1.961, 1.939, 2.02, 2.009, 2.184, 2.36, 2.456, 2.571, 2.557, 2.739, 2.797, 2.856, 2.835, 3.031, 3.109, 3.188, 3.383, 3.53, 3.734, 3.977, 4.239, 4.355, 4.569, 4.713, 4.722, 4.878, 5.134, 5.424, 5.396, 5.385, 5.675, 5.937, 6.267, 6.466, 6.45, 6.618, 6.491, 6.792, 7.285, 7.594, 7.861, 8.133, 8.475, 8.786, 8.955, 8.948, 9.267, 9.521, 9.905, 10.175, 10.561, 11.035, 11.526, 12.066, 12.56, 12.682, 12.909, 13.271, 13.774, 14.234, 14.614, 14.874, 14.83, 14.419, 14.784, 15.021, 15.355, 15.612, 16.013, 16.472, 16.716, 17.093];
gdp_growth = [0, -8.5, -6.4, -0.129, -1.3, 10.8, 8.9, 12.9, 5.1, -3.3, 8.0, 8.8, 17.7, 18.9, 17.0, 8.0, -1.0, -0.116, -1.1, 4.1, -0.5, 8.7, 8.1, 4.1, 4.7, -0.6, 7.1, 2.1, 2.1, -0.7, 6.9, 2.6, 2.6, 6.1, 4.4, 5.8, 6.5, 6.6, 2.7, 4.9, 3.1, 0.2, 3.3, 5.2, 5.6, -0.5, -0.2, 5.4, 4.6, 5.6, 3.2, -0.2, 2.6, -1.9, 4.6, 7.3, 4.2, 3.5, 3.5, 4.2, 3.7, 1.9, -0.1, 3.6, 2.7, 4.0, 2.7, 3.8, 4.5, 4.5, 4.7, 4.1, 1.0, 1.8, 2.8, 3.8, 3.3, 2.7, 1.8, -0.3, -2.8, 2.5, 1.6, 2.2, 1.7, 2.6, 2.9, 1.5, 2.3];
export = [25940, 26403, 27722, 29620, 33341, 35285, 38926, 41333, 45543, 49220, 56640, 59677, 67222, 91242, 120897, 132585, 142716, 152301, 178428, 224131, 271834, 294398, 275236, 266106, 291094, 289070, 310033, 348869, 431149, 487003, 535233, 578344, 616882, 642863, 703254, 794387, 851602, 934453, 933174, 969867, 1075321, 1005653, 978705, 1020419, 1161549, 1286023, 1457644, 1653547, 1841611, 1583051, 1853603, 2127020, 2218989, 2293457, 2375905, 2263907, 2208072, 2331599];
import = [22432, 22208, 24352, 25410, 27319, 30621, 35987, 38729, 45293, 49129, 54386, 60979, 72665, 89342, 125190, 120181, 148798, 179547, 208191, 248696, 291241, 310570, 299391, 323874, 400166, 410950, 448572, 500552, 545715, 580144, 616097, 609479, 656094, 713174, 801747, 890771, 955667, 1042726, 1099314, 1228485, 1447837, 1367162, 1397659, 1514309, 1771434, 2000270, 2219358, 2358922, 2550339, 1966827, 2348265, 2675646, 2755762, 2755334, 2866241, 2764352, 2712866, 2900041];
employ_rate = [56.1,55.4,55.5,55.4,55.7,56.2,56.9,57.3,57.5,58.0,57.4,56.6,57.0,57.8,57.8,56.1,56.8,57.9,59.3,59.9,59.2,59.0,57.8,57.9,59.5,60.1,60.7,61.5,62.3,63.0,62.8,61.7,61.5,61.7,62.5,62.9,63.2,63.8,64.1,64.3,64.4,63.7,62.7,62.3,62.3,62.7,63.1,63.0,62.2,59.3,58.5,58.4,58.6,58.6,59.0,59.3,59.7,60.1];
% delete the former 31 elements
gdp(1:31) = [];
gdp_growth(1:31) = [];

export = export*1e-4/9;
import = import*1e-4/8;

y = [gdp;gdp_growth];

if sensor_number == 3
    sensor = [export;import;employ_rate];
end

if sensor_number == 2
    sensor = [export;import];
end

% Q matrix 
%Q = cov(y(1,:),y(2,:));
Q = [1,0;0,1]; % 3*3 [X,1,2;1,Y,3;2,3,Z];
% R matrix
% % problem is how to set the R covariance, only with the number of y
% % variables

if sensor_number == 3
 R = [2,0.1,0.2;0.1,3,0.3;0.2,0.3,4];
end

if sensor_number == 2
    R = [4, 0;0 ,4];
end

w = mvnrnd([0;0], Q, length(gdp));
w = w';
v = mvnrnd(zeros(sensor_number,1), R, length(gdp));
v = v';

H = (sensor - v)/y; %observe model
F = (y - w)/y; % transition model
P = [1,1;1,1];
z = H*y + v; %measure

y_predict(:,1) = [1,1];
y_temp(:,1) = y(:,1);
residual = 0;
I = eye(2);
% iteration 
for t = 2:length(y(1,:))
    
    y_temp(:,t) = F*y(:,t-1);
    P = F*P*F' + Q;
    residual = z(:,t) - H*y(:,t-1);
    S = R + H*P*H';
    K = (P*H')/S;    %kalman gain
    y_predict(:,t) = y_temp(:,t) + K*residual;
    P = (I - K*H)*P*(1-K*H)'* + K*R*K';
    residual = z(:,t) - H*y_predict(:,t);
    
end

figure(1)
n = 1960:2017;
plot(n,y_predict(1,:),'b');
hold on 
plot(n,y(1,:),'g');
hold on 
scatter(n,z(1,:),'r')
hold on
legend('Kalman Estimate','Ground Truth','Measure Value')
title('Kalman Filter')

%% Probability Distribution
figure(2)

predict_mean = mean(y_predict(1,:));
predict_var = std(y_predict(1,:));
measure_mean = mean(z(1,:));
measure_var = std(z(1,:));

x = -20:0.1:20;
%transition
trans = normpdf(x,0,predict_var)*0.9818;  
plot(x,trans,'r')
hold on 

%SENSOR 
sensor = normpdf(x,0,1.1);
plot(x,sensor,'m')
hold on 


xt = normpdf(x,predict_mean,predict_var);
xt_1 = normpdf(x,measure_mean-8,1.1);
plot(x,xt,'b')
hold on 
plot(x,xt_1,'c')
hold on 
legend('Transition','Sensor','x(t)','x(t+1)')
title('Probability Distribution')

cov = cov(y(1,:),y_predict(1,:));
coeff = cov(1,2)/sqrt(cov(1,1))/sqrt(cov(2,2));
variance = var(y_predict(1,:));
gt_var = var(y(1,:));
coeff
variance
gt_var

