%% Bouncing ball
% Simulation and animation of a bouncing ball.
%
% Reference
% https://www.mathworks.com/help/matlab/math/ode-event-location.html
% Mark W. Reichelt and Lawrence F. Shampine, 1/3/95
%
%%

clear ; close all ; clc

courtWidth = 8.23;
courtLength = 23.77;
courtWidthDiv2 = courtWidth/2;
courtLengthDiv2 = courtLength/2;
netHeight = .106;
buffer = 5;
maxX = courtWidthDiv2 + buffer;
minX = -courtWidthDiv2 - buffer;
maxY = courtLengthDiv2 + buffer;
minY = -courtLengthDiv2 - buffer;

%% Parameters

% Video
tf  = 30;                   % Final time                    [s]
fR  = 100;                   % Frame rate                  [fps]
dt  = 1/fR;                 % Time resolution               [s]
t   = linspace(0,tf,tf*fR); % Time                          [s]

%% Simulation

% VERTICAL DYNAMICS
% Hit the ground event.
options = odeset('Events',@hit_the_ground);

% Initial conditions [height speed]
zp = 3;            % Initial height    [m]
zv = -6;            % Initial speed     [m/s]
z0 = [zp zv];

% Time span for simulation
TSPAN = t;

% Cumulative output initialization
t_ac = [];
z = [];

% One bounce per loop
for i = 1:2
    % Integration until hit the ground
    [tout,zout] = ode45(@(t,z) ball_vertical_dynamics(t,z),TSPAN,z0,options);
    
    % Update next iteration
    % Initial conditions [position speed]
    z0 = [0 -.7*zout(end,2)];   
    % Time
    TSPAN = tout(end) + t;
    
    % Acumulate output
    t_ac = [t_ac ; tout];
    z = [z ; zout(:,1)];
end

% LONGITUDINAL DYNAMICS
x0  = -courtWidthDiv2 + 1;
vx  = 5;                % Horizontal speed      [m/s]
x   = (vx*t_ac) + x0;   % Horizontal position   [m]
y0  = -courtLengthDiv2 + .5;
vy  = 60;               % Horizontal speed      [m/s]
y   = (vy*t_ac) + y0;   % Horizontal position   [m]

%% Animation
c = cool(6); % Colormap
figure
set(gcf,'Position',[50 50 640 640])     % Social
hold on ; grid off ; axis equal
set(gca,'xlim',[(-courtWidthDiv2 - buffer) (courtWidthDiv2 + buffer)],'ylim',[(-courtLengthDiv2 - buffer)  (courtLengthDiv2 + buffer)])

b0 = [(-courtWidthDiv2 - buffer) (-courtLengthDiv2 - buffer) (courtWidth + (2*buffer)) (courtLength + (2*buffer))];
b1 = [-courtWidthDiv2 -courtLengthDiv2 8.23 23.77];
b2 = [-courtWidthDiv2 (-courtLengthDiv2 + 5.48) 4.11 6.4];
b3 = [(-courtWidthDiv2 + 4.11) (-courtLengthDiv2 + 5.48) 4.11 6.4];
b4 = [-courtWidthDiv2 (-courtLengthDiv2 + 11.88) 4.11 6.4];
b5 = [(-courtWidthDiv2 + 4.11) (-courtLengthDiv2 + 11.88) 4.11 6.4];

for i=1:length(t_ac)
    cla 
    plot3(x(1:i) , y(1:i),  z(1:i)  ,'-','Color',c(5,:),'LineWidth',3)
    plot3(x(i),y(i)   ,z(i)    ,'o','Color',c(4,:),'MarkerFaceColor',c(1,:),'MarkerSize',10)
    view(45,20)
    rectangle('Position',b0,'FaceColor',[.7 .7 .7])  
    rectangle('Position',b1,'FaceColor','g')  
    rectangle('Position',b2)  
    rectangle('Position',b3) 
    rectangle('Position',b4)  
    rectangle('Position',b5) 
    xlabel('x [m]');
    ylabel('y [m]');
    title('Tennis Simulation');
    frame = getframe(gcf);
end

indices = find(x < minX);
if ~isempty(indices)
    x(indices) = minX;
    yVal = y(indices(1));
    zVal = z(indices(1));
    y(indices) = yVal;
    z(indices) = zVal;
end

indices = find(x > maxX);
if ~isempty(indices)
    x(indices) = maxX;
    yVal = y(indices(1));
    zVal = z(indices(1));
    y(indices) = yVal;
    z(indices) = zVal;
end

indices = find(y < minY);
if ~isempty(indices)
    y(indices) = minY;
    xVal = x(indices(1));
    zVal = z(indices(1));
    x(indices) = xVal;
    z(indices) = zVal;
end

indices = find(y > maxY);
if ~isempty(indices)
    y(indices) = maxY;
    xVal = x(indices(1));
    zVal = z(indices(1));
    x(indices) = xVal;
    z(indices) = zVal;
end

% Net check
numSamples = length(y);
for index = 1:numSamples
    if y(index) < 0
        continue
    else
        if (z(index) > netHeight)
            disp("passed net check")
        else
            disp("hit in net")
        end
        break
    end
end

% x = round(x,4);
% y = round((y + .1),4);
% z = round(z,4);
% trajectory = [x z y];
% writematrix(trajectory,'myData.dat','Delimiter',' ')  

function dz = ball_vertical_dynamics(~,z)
    % Constant
    g = -9.81;      % Gravity [m/s]
    % Dynamics
    dz(1,1) = z(2);
    dz(2,1) = g;
end

function [value,isterminal,direction] = hit_the_ground(~,y)
    value       = y(1);     % height = 0
    isterminal  = 1;        % stop the integration
    direction   = -1;       % negative direction
end