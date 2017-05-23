%% Parameters
    %scaling
    s_x = 1;
    s_y = 1;
    s_z = 1;

    %rotate
    theta_y = 90;

    %translation
    d_x = 39.9;
    d_y = 0.05;
    d_z = 38.1;

    %%Processing
    S = [s_x, 0,   0,   0;
         0,   s_y, 0 ,  0;
         0,   0,   s_z, 0;
         0,   0,   0,   1];

    R = [cosd(theta_y),  0,   sind(theta_y), 0;
         0,             1,   0 ,           0;
         -sind(theta_y), 0,   cosd(theta_y), 0;
         0,   0,   0,   1];

    D = [1, 0, 0, d_x;
         0, 1, 0, d_y;
         0, 0, 1, d_z;
         0,   0,   0,   1];

    T = D * R * S;

    for i=1:3
        fprintf('%f %f %f %f\n', T(i,:))
    end


